import importlib.util,math
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch47/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_percentile():assert r.percentile([1,2,3,100],.95)==100
def test_ai():assert r.arithmetic_intensity(100,20)==5
def test_ai_reject_zero():
 try:r.arithmetic_intensity(1,0);assert False
 except ValueError:pass
def test_roofline_memory_bound():assert r.roofline_bound(1,1,100,10)==10
def test_roofline_compute_bound():assert r.roofline_bound(100,1,50,10)==50
def test_classify_memory():assert r.classify(2,100,10)=="memory-bound-region"
def test_classify_compute():assert r.classify(20,100,10)=="compute-bound-region"
def test_ttft():q=r.Request(10,35,(50,));assert q.ttft()==25
def test_itl():q=r.Request(0,10,(25,40));assert q.itls()==(15,15)
def test_metrics_goodput():
 qs=[r.Request(0,20,(30,40)),r.Request(0,200,(220,))]
 m=r.metrics(qs,1000,100,20);assert m["goodput_req_per_s"]==1 and m["slo_attainment"]==.5
def test_throughput_counts_tokens():
 q=[r.Request(0,10,(20,30))];assert r.metrics(q,1000,100,20)["output_tokens_per_s"]==3
def test_speedup():assert r.speedup(20,10)==2
def test_speedup_not_percent_reduction():assert r.speedup(100,80)==1.25
