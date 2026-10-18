import importlib.util
from pathlib import Path
import sys
import pytest
import torch

S=importlib.util.spec_from_file_location("evod_batch_a_37",Path(__file__).parents[1]/"drafts/ch37/reference.py")
r=importlib.util.module_from_spec(S);sys.modules[S.name]=r;S.loader.exec_module(r)
torch.set_num_threads(1)


def oracle(model,prompt,n):
    seq=list(prompt);out=[]
    for _ in range(n):
        token=int(r.native.full_oracle(model,tuple(seq))[-1].argmax())
        out.append(token);seq.append(token)
    return out


@pytest.mark.parametrize("budget,chunk",[(1,1),(2,1),(3,2),(5,4),(8,8)])
@pytest.mark.parametrize("page",[1,2,4])
def test_schedule_budget_native_parity_and_page_conservation(budget,chunk,page):
    model=r.native.tiny_model()
    s=r.Scheduler(model,32,page,budget,chunk)
    reqs=[s.submit("A",0,(0,1,2),3),s.submit("B",1,(2,),2),s.submit("C",2,(3,2,1,0),1)]
    s.run()
    for rr in reqs:
        assert rr.generated == oracle(model,rr.prompt,rr.output)
        assert len(rr.token_ticks) == rr.output
        assert all(b>a for a,b in zip(rr.token_ticks,rr.token_ticks[1:]))
    for row in s.trace:
        assert sum(n for _,_,n,_ in row["work"]) <= budget
        assert all(n<=chunk for _,phase,n,_ in row["work"] if phase=="prefill")
        assert row["used_pages"] <= row["reserved_pages"] <= s.pool.capacity
    assert s.audit()["used_pages"] == 0


def test_first_output_is_final_prefill_not_extra_decode():
    s=r.Scheduler(r.native.tiny_model(),4,2,4,4)
    a=s.submit("a",0,(0,1),1)
    assert s.step()==[("a","prefill",2,1)]
    assert a.phase=="done" and a.token_ticks==[1] and r.metrics(a)["ttft"]==1
    assert r.metrics(a)["itl_max"] is None


def test_reservation_wait_and_readmission():
    s=r.Scheduler(r.native.tiny_model(),2,2,4,4)
    a=s.submit("a",0,(0,1,2),2)
    b=s.submit("b",0,(3,2),1)
    s.step();assert a.phase=="decode" and b.phase=="waiting"
    s.step();assert a.phase=="done" and b.phase=="waiting"
    s.step();assert b.phase=="done" and s.audit()["used_pages"]==0


def test_decode_priority_arrivals_idle_and_cancellation():
    s=r.Scheduler(r.native.tiny_model(),12,2,1,1)
    a=s.submit("a",0,(0,),3)
    b=s.submit("b",1,(1,2,3),1)
    s.step();assert a.phase=="decode"
    assert s.step()[0][:2]==("a","decode")
    s.cancel("a");assert a.phase=="cancelled"
    s.cancel("a")
    s.cancel("b");assert s.audit()["used_pages"]==0
    c=s.submit("c",5,(2,),1)
    while s.tick<5: assert s.step()==[]
    s.step();assert c.token_ticks==[6]


@pytest.mark.parametrize("arrival,prompt,out",[(-1,(0,),1),(True,(0,),1),(0,(),1),(0,(0,),0),(0,(4,),1),(0,(0,)*16,2)])
def test_bad_requests(arrival,prompt,out):
    s=r.Scheduler(r.native.tiny_model(),16,2)
    with pytest.raises(ValueError): s.submit("x",arrival,prompt,out)
    assert not s.requests and s.audit()["used_pages"]==0


def test_impossible_admission_and_duplicate_identity():
    s=r.Scheduler(r.native.tiny_model(),1,1)
    with pytest.raises(MemoryError): s.submit("a",0,(0,1),1)
    s.submit("a",0,(0,),1)
    with pytest.raises(ValueError):s.submit("a",0,(0,),1)


@pytest.mark.parametrize("mode",["fp64","fp16","bf16","int8"])
def test_representation_zero_and_actual_continuation(mode):
    assert torch.equal(r.represent(torch.zeros(4),mode),torch.zeros(4).double())
    m=r.native.tiny_model();t=(0,1,2,3,0,2)
    z=r.precision_rollout(m,t,mode)
    assert torch.isfinite(z).all() and z.shape==(6,4)
    if mode=="fp64": torch.testing.assert_close(z,r.native.full_oracle(m,t),atol=2e-12,rtol=2e-12)


@pytest.mark.parametrize("scale",[None,.1,1.0])
def test_int8_nearest_bound_without_saturation(scale):
    x=torch.tensor([-.2,-.1,0,.07,.2],dtype=torch.float64)
    q,s=r.int8_symmetric(x,scale)
    assert q.dtype==torch.int8 and (x-q.double()*s).abs().max() <= s/2+1e-15


def test_outlier_saturation_argmax_and_nonfinite_controls():
    q,s=r.int8_symmetric(torch.tensor([1.,.99,1000.]))
    assert q[0]==q[1]==0
    q,s=r.int8_symmetric(torch.tensor([10.]),.01)
    assert q.item()==127 and abs(10-q.item()*s)>s/2
    ref=torch.tensor([1.,.99]);other=torch.tensor([.98,1.01])
    report=r.quality(ref,other)
    assert report["argmax_fraction"]==0 and not r.gate(report,.1,.1)
    assert not r.gate({**report,"max_abs":float("nan")},1,1,0)
    with pytest.raises(ValueError):r.represent(torch.tensor([1e10]),"fp16")
    for bad in [torch.tensor([float("nan")]),torch.tensor([float("inf")]),torch.empty(0)]:
        with pytest.raises(ValueError):r.int8_symmetric(bad)
        with pytest.raises(ValueError):r.quality(bad,bad)


def test_margin_sufficient_condition_and_identical_gate():
    a=torch.tensor([2.,1.,0.],dtype=torch.float64)
    b=a+torch.tensor([-.2,.2,.2])
    assert 1>2*r.quality(a,b)["max_abs"] and b.argmax()==a.argmax()
    assert r.gate(r.quality(a,a),0,0)


@pytest.mark.parametrize("seed",range(10))
def test_independent_fixed_query_error_bound(seed):
    g=torch.Generator().manual_seed(seed)
    q=torch.randn(4,generator=g,dtype=torch.float64)
    k=torch.randn(7,4,generator=g,dtype=torch.float64)
    v=torch.randn(7,3,generator=g,dtype=torch.float64)
    dk=torch.randn(7,4,generator=g,dtype=torch.float64)*.003
    dv=torch.randn(7,3,generator=g,dtype=torch.float64)*.004
    p=(k@q/2).softmax(0);p2=((k+dk)@q/2).softmax(0)
    epsk=dk.norm(dim=1).max();epsv=dv.norm(dim=1).max()
    delta=q.norm()*epsk/2
    assert (p-p2).abs().sum() <= 2*delta+1e-15
    bound=epsv+2*v.norm(dim=1).max()*delta
    assert (p@v-p2@(v+dv)).norm() <= bound+1e-15


def test_fp16_small_representation_error():
    x=torch.tensor([.1,-.2,3.4],dtype=torch.float64)
    assert (r.represent(x,"fp16")-x).abs().max()<.001


def test_bf16_nearest_even_halfway_cases():
    x=torch.tensor([1+1/256,1+3/256],dtype=torch.float64)
    expected=torch.tensor([1.,1+2/128],dtype=torch.float64)
    assert torch.equal(r.represent(x,"bf16"),expected)


def test_underflow_and_range_are_separate():
    small=torch.tensor([1e-10],dtype=torch.float64)
    assert r.represent(small,"fp16").item()==0
    assert r.represent(small,"bf16").item()>0
    large=torch.tensor([1e6],dtype=torch.float64)
    with pytest.raises(ValueError):r.represent(large,"fp16")
    assert torch.isfinite(r.represent(large,"bf16")).all()
