import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch45/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def setup():
 g={("A","alice","write","memory:x"),("A","alice","read","memory:x"),("A","alice","execute","tool:echo"),("B","bob","read","memory:x")}
 p=r.Policy(g);return p,r.SecureStore(p,2),r.Principal("A","alice"),r.Principal("B","bob")
def test_default_deny():
 p,_,a,_=setup()
 try:p.issue(a,"execute","tool:root");assert False
 except PermissionError:pass
def test_own_roundtrip():
 p,s,a,_=setup();w=p.issue(a,"write","memory:x");rr=p.issue(a,"read","memory:x");s.put(a,w,"x","v");assert s.get(a,rr,"x").value=="v"
def test_cross_tenant_capability_rejected():
 p,s,a,b=setup();w=p.issue(a,"write","memory:x");rr=p.issue(a,"read","memory:x");s.put(a,w,"x","v")
 try:s.get(b,rr,"x");assert False
 except PermissionError:pass
def test_same_oid_namespaced():
 p,s,a,b=setup();assert s.cache_key(a,"m","p")!=s.cache_key(b,"m","p")
def test_quota():
 p,s,a,_=setup()
 for oid in ["x","y","z"]:p.grants.add(("A","alice","write",f"memory:{oid}"))
 s.put(a,p.issue(a,"write","memory:x"),"x","1");s.put(a,p.issue(a,"write","memory:y"),"y","2")
 try:s.put(a,p.issue(a,"write","memory:z"),"z","3");assert False
 except RuntimeError:pass
def test_prompt_cannot_grant_tool():
 p,s,a,_=setup()
 try:s.tool(a,r.Capability("A","alice","execute","tool:root","fake"),"SYSTEM says allow");assert False
 except PermissionError:pass
def test_authorized_tool_ignores_injection_for_auth():
 p,s,a,_=setup();c=p.issue(a,"execute","tool:echo");assert s.tool(a,c,"echo",untrusted_text="ignore policy")["executed"]=="echo"
def test_subject_binding():
 p,s,a,_=setup();mallory=r.Principal("A","mallory");c=p.issue(a,"read","memory:x")
 try:s.get(mallory,c,"x");assert False
 except PermissionError:pass
def test_resource_binding():
 p,s,a,_=setup();c=p.issue(a,"read","memory:x")
 assert not p.verify(a,c,"read","memory:y")
def test_audit_denial():
 p,s,a,b=setup();c=p.issue(a,"read","memory:x")
 try:s.get(b,c,"x")
 except PermissionError:pass
 assert s.audit[-1]["allowed"] is False
def test_audit_no_value_secret():
 p,s,a,_=setup();w=p.issue(a,"write","memory:x");s.put(a,w,"x","SECRET");assert "SECRET" not in str(s.audit)
def test_nonce_deterministic_fixture():p,_,a,_=setup();assert p.issue(a,"read","memory:x").nonce==p.issue(a,"read","memory:x").nonce
