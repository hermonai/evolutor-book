import importlib.util,numpy as np
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch37/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)

def test_scheduler_respects_token_budget():
 q=[r.Req("a",0,10,1),r.Req("b",0,10,1)]
 w=r.schedule_iteration(q,0,3,2);assert sum(n for _,_,n in w)<=3

def test_chunked_prefill_bound():
 q=[r.Req("a",0,10,1)];w=r.schedule_iteration(q,0,9,2);assert w[0][2]==2

def test_decode_priority_over_new_prefill():
 a=r.Req("a",0,1,2,prefilled=1);b=r.Req("b",0,10,1)
 w=r.schedule_iteration([a,b],0,1,4);assert w[0][0] is a and w[0][1]=="decode"

def test_not_yet_arrived_not_scheduled():
 q=[r.Req("a",5,1,1)];assert r.schedule_iteration(q,0,4,2)==[]

def test_simulation_finishes_and_ordered_tokens():
 q=[r.Req("a",0,3,3),r.Req("b",1,1,2)];r.simulate(q,3,2);assert all(x.done for x in q)
 assert all(all(b>a for a,b in zip(x.token_ticks,x.token_ticks[1:])) for x in q)

def test_ttft_nonnegative():
 q=[r.Req("a",2,2,1)];r.simulate(q,2,1);assert r.metrics(q[0])["ttft"]>=0

def test_fp16_finite_small_error():
 x=np.array([.1,-.2,3.4],dtype=np.float32);y=r.fp16_round(x);assert np.isfinite(y).all() and np.max(np.abs(x-y))<.01

def test_bf16_zero_exact():
 x=np.zeros(8,dtype=np.float32);np.testing.assert_array_equal(r.bf16_round(x),x)

def test_int8_roundtrip_bounded_by_scale_halfish():
 x=np.array([-2.,-.3,.1,2.],dtype=np.float32);q,s=r.int8_symmetric(x);y=r.dequant_int8(q,s)
 assert np.max(np.abs(x-y))<=s/2+1e-6

def test_int8_zero_tensor():
 x=np.zeros(4,dtype=np.float32);q,s=r.int8_symmetric(x);assert s==1 and not q.any()

def test_quality_detects_argmax_flip():
 a=np.array([1.,.99]);b=np.array([.98,1.01]);z=r.quality(a,b);assert not z["argmax_equal"]

def test_gate_rejects_argmax_flip_even_smallish_error():
 a=np.array([1.,.99]);b=np.array([.98,1.01]);z=r.quality(a,b);assert not r.gate(z,.1,.1,True)

def test_gate_accepts_identical():
 z=r.quality(np.array([1.,2.]),np.array([1.,2.]));assert r.gate(z,0,0)

def test_long_prefill_does_not_block_existing_decode_in_policy():
 a=r.Req("decode",0,1,3,prefilled=1);b=r.Req("long",0,100,1)
 w=r.schedule_iteration([a,b],0,4,4);assert w[0][1]=="decode"
