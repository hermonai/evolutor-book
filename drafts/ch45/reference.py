"""Authority model for trusted serialized callers; no cryptographic tokens."""
from dataclasses import dataclass
import hashlib
import json


def name(value):
    if type(value) is not str or not 1 <= len(value) <= 128:
        raise ValueError("bounded nonempty name")


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str
    session: str = "s1"

    def validate(self):
        for x in (self.tenant, self.subject, self.session):
            name(x)


@dataclass(frozen=True)
class Capability:
    principal: Principal
    action: str
    resource: str
    epoch: int
    expires: int
    serial: int


class Policy:
    def __init__(self, grants=()):
        self.grants = frozenset(grants)
        self.epoch, self.next_serial = 0, 0
        self.issued = {}

    def replace(self, grants):
        self.grants = frozenset(grants)
        self.epoch += 1
        self.issued.clear()

    def issue(self, p, action, resource, *, now=0, ttl=10):
        p.validate()
        name(action)
        name(resource)
        if type(now) is not int or now < 0 or type(ttl) is not int or ttl < 1:
            raise ValueError("integer time and positive TTL")
        if (p.tenant, p.subject, action, resource) not in self.grants:
            raise PermissionError("deny default")
        c = Capability(p, action, resource, self.epoch, now + ttl, self.next_serial)
        self.issued[c.serial] = c
        self.next_serial += 1
        return c

    def verify(self, p, c, action, resource, *, now=0):
        p.validate()
        if type(now) is not int or now < 0:
            raise ValueError("integer time")
        return (type(c) is Capability and self.issued.get(c.serial) is c
                and c.principal == p and c.action == action
                and c.resource == resource and c.epoch == self.epoch
                and now < c.expires
                and (p.tenant, p.subject, action, resource) in self.grants)


def cache_key(p, artifact, policy_domain, prefix_digest):
    p.validate()
    fields = (p.tenant, artifact, policy_domain, prefix_digest)
    for v in fields:
        name(v)
    # JSON array is unambiguous even when names contain separators.
    return hashlib.sha256(json.dumps(fields, ensure_ascii=True,
                                    separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class Reservation:
    tenant: str
    request: str
    slots: int
    bytes: int


class Quota:
    def __init__(self, limits, global_limit):
        self.limits, self.global_limit = dict(limits), tuple(global_limit)
        for lim in [*self.limits.values(), self.global_limit]:
            if len(lim) != 2 or any(type(x) is not int or x < 0 for x in lim):
                raise ValueError("nonnegative slot/byte limits")
        self.held = {}

    def used(self, tenant=None):
        rs = [r for r in self.held.values() if tenant is None or r.tenant == tenant]
        return sum(r.slots for r in rs), sum(r.bytes for r in rs)

    def reserve(self, tenant, request, slots, nbytes):
        name(tenant)
        name(request)
        if any(type(v) is not int or v < 0 for v in (slots, nbytes)):
            raise ValueError("nonnegative integer resource vector")
        if tenant not in self.limits or (tenant, request) in self.held:
            raise RuntimeError("unknown tenant/duplicate reservation")
        want = (slots, nbytes)
        for used, limit in ((self.used(tenant), self.limits[tenant]),
                            (self.used(), self.global_limit)):
            if any(u + w > cap for u, w, cap in zip(used, want, limit)):
                raise RuntimeError("quota before allocation")
        r = Reservation(tenant, request, slots, nbytes)
        self.held[(tenant, request)] = r
        return r

    def release(self, reservation):
        key = (reservation.tenant, reservation.request)
        if self.held.get(key) is not reservation:
            raise RuntimeError("unissued/already released reservation")
        del self.held[key]


class SecureStore:
    def __init__(self, policy, quota=2):
        if type(quota) is not int or quota < 0:
            raise ValueError("nonnegative object quota")
        self.policy, self.quota = policy, quota
        self.objects, self.audit = {}, []

    def authorize(self, p, c, action, resource, now):
        ok = self.policy.verify(p, c, action, resource, now=now)
        self.audit.append(dict(seq=len(self.audit), tenant=p.tenant,
                               subject=p.subject, session=p.session,
                               action=action, resource_class=resource.split(":")[0],
                               policy_epoch=self.policy.epoch, allowed=ok,
                               reason="grant" if ok else "authority"))
        if not ok:
            raise PermissionError("authority")

    def put(self, p, c, oid, value, now=0):
        name(oid)
        self.authorize(p, c, "write", "memory:" + oid, now)
        if type(value) is not str or len(value.encode()) > 1024:
            raise ValueError("bounded text payload")
        key = p.tenant, oid
        owned = sum(t == p.tenant for t, _ in self.objects)
        if key not in self.objects and owned >= self.quota:
            raise RuntimeError("object quota")
        self.objects[key] = value

    def get(self, p, c, oid, now=0):
        name(oid)
        self.authorize(p, c, "read", "memory:" + oid, now)
        return self.objects[(p.tenant, oid)]

    def tool(self, p, c, tool, args, untrusted_text="", now=0):
        # Only an in-memory echo operation exists. Never invokes a real tool.
        self.authorize(p, c, "execute", "tool:" + tool, now)
        if tool != "echo" or type(args) is not dict or set(args) != {"text"}:
            raise ValueError("closed tool/schema")
        if type(args["text"]) is not str or len(args["text"]) > 80:
            raise ValueError("bounded echo argument")
        return dict(executed="echo", tenant=p.tenant, text=args["text"])


def results():
    a, b = Principal("A", "alice"), Principal("B", "bob")
    pol = Policy({("A", "alice", x, "memory:x") for x in ("read", "write")}
                 | {("A", "alice", "execute", "tool:echo")})
    s = SecureStore(pol)
    w, rr = (pol.issue(a, x, "memory:x") for x in ("write", "read"))
    s.put(a, w, "x", "private fixture")
    denied = False
    try:
        s.get(b, rr, "x")
    except PermissionError:
        denied = True
    q = Quota({"A": (2, 100), "B": (2, 100)}, (4, 180))
    q.reserve("A", "r1", 1, 80)
    q.reserve("B", "r2", 1, 80)
    return dict(cross_denied=denied, quota=[dict(tenant=t, slots=q.used(t)[0],
                 nbytes=q.used(t)[1]) for t in ("A", "B")],
                 cache_partitioned=cache_key(a,"m","p","x") !=
                 cache_key(b,"m","p","x"), source="serialized authority model")


TABLES = [("quota", ["Tenant", "Held slots", "Held bytes"],
           ["tenant", "slots", "nbytes"], "lrr")]
PLOTS = []
LISTINGS = ["Policy.issue", "Policy.verify", "cache_key", "Quota.reserve",
            "SecureStore.authorize", "SecureStore.tool"]
