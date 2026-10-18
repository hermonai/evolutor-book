import importlib.util
from pathlib import Path
import sys
from itertools import permutations
import pytest

spec=importlib.util.spec_from_file_location("evod47",Path(__file__).parents[1]/"drafts/ch47/reference.py")
r=importlib.util.module_from_spec(spec);sys.modules[spec.name]=r;spec.loader.exec_module(r)


def test_incoming_trace_exact_metrics():
    m=r.results()["metrics"]
    assert m==dict(requests=3,output_tokens=11,p50_ttft=60,p95_ttft=130,p95_itl=30,
                  output_tokens_per_s=44,goodput_req_per_s=8,slo_attainment=2/3)


@pytest.mark.parametrize("q,expected",[(.01,1),(.5,2),(.95,100),(1,100)])
def test_order_statistic(q,expected):
    for xs in permutations([1,2,3,100]):assert r.percentile(xs,q)==expected


@pytest.mark.parametrize("q",[0,-.1,1.01,float("nan"),float("inf")])
def test_invalid_quantile(q):
    with pytest.raises(ValueError):r.percentile([1],q)


@pytest.mark.parametrize("times",[(0,-1,()),(10,5,()),(0,10,(9,)),
    (0,float("nan"),()),(0,None,(1,)),(0,10,[20])])
def test_invalid_trace(times):
    with pytest.raises(ValueError):r.Request(*times).validate()


def test_failed_zero_output_in_denominator():
    reqs=[r.Request(0,None,(),False,20),r.Request(0,10)]
    m=r.metrics(reqs,0,1000,100,20)
    assert m["output_tokens"]==1 and m["slo_attainment"]==.5
    assert m["p95_itl"] is None


def test_no_token_is_not_zero_latency_success():
    with pytest.raises(ValueError):r.Request(0,None).validate()
    m=r.metrics([r.Request(0,None,(),False,20)],0,1000,100,20)
    assert m["p95_ttft"] is None and m["goodput_req_per_s"]==0


def test_terminal_timestamp_is_inside_cohort_and_after_outputs():
    with pytest.raises(ValueError):r.Request(0,None,(),False).validate()
    with pytest.raises(ValueError):r.Request(0,10,(20,),False,19).validate()
    with pytest.raises(ValueError):r.metrics([r.Request(0,None,(),False,1001)],0,1000,100,20)


@pytest.mark.parametrize("start,end",[(0,0),(5,10),(0,9)])
def test_invalid_observation_window(start,end):
    with pytest.raises(ValueError):r.metrics([r.Request(0,10)],start,end,100,20)


def test_all_gap_gate_differs_from_mean_tpot():
    q=r.Request(0,10,(11,110))
    assert sum(q.itls())/2==50
    assert r.metrics([q],0,1000,20,60)["goodput_req_per_s"]==0


def test_higher_raw_throughput_can_have_lower_goodput():
    fast=r.metrics([r.Request(0,10,(20,))],0,1000,30,20)
    overloaded=r.metrics([r.Request(0,100,(200,300))]*3,0,1000,30,20)
    assert overloaded["output_tokens_per_s"]>fast["output_tokens_per_s"]
    assert overloaded["goodput_req_per_s"]<fast["goodput_req_per_s"]


def test_critical_path_not_sum_of_parallel_spans():
    spans=[("q",10,()),("p",40,("q",)),("fetch",30,("q",)),("d",20,("p","fetch"))]
    assert r.critical_path(spans)==70
    assert sum(s[1] for s in spans)==100


def test_unordered_or_cyclic_dag_rejected():
    with pytest.raises(ValueError):r.critical_path([("a",1,("b",)),("b",1,("a",))])


@pytest.mark.parametrize("flops,nbytes,peak,bw,expected",[(2e12,1e12,100e12,2e12,4e12),
    (100,1,50,10,50),(0,1,50,10,0)])
def test_roofline_units(flops,nbytes,peak,bw,expected):
    assert r.roofline_bound(flops,nbytes,peak,bw)==expected


@pytest.mark.parametrize("value",[-1,0,float("nan"),float("inf")])
def test_invalid_bytes_and_bandwidth(value):
    with pytest.raises(ValueError):r.roofline_bound(1,value,1,1)
    with pytest.raises(ValueError):r.roofline_bound(1,1,1,value)


def test_costs_match_prior_geometry_without_running_backend():
    a=r.attention_cost(24,8,128,4096,2)
    assert a=={"flops":402653184,"bytes":402653184}
    n=r.native_cost(8,64,4,8);s=r.native_cost(8,64,4,8,True)
    assert n=={"flops":6144,"bytes":12544}
    assert s["bytes"]-n["bytes"]==16384
    assert r.results()["real_backend_measurements"]==[]


def test_speedup_amdahl_and_matched_runs():
    assert r.speedup(100,80)==1.25
    assert r.amdahl(.2,2)==pytest.approx(1/.9)
    ratios=r.paired_ratio([100,120,80],[80,100,64])
    assert ratios["n"]==3 and ratios["minimum"]==1.2 and ratios["maximum"]==1.25
    with pytest.raises(ValueError):r.paired_ratio([1],[1])
