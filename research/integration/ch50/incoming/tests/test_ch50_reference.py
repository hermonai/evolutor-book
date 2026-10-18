import importlib.util
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch50/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_quality_optimum(): assert r.quality((1,0),(1,0))==1
def test_step_moves_to_target(): assert r.step((0,0),(1,0),.5)[0]>.0
def test_matrix_shape(): A,_=r.accuracy_matrix([(1,0),(0,1)]); assert len(A)==2 and all(len(x)==2 for x in A)
def test_forgetting_nonnegative_fixture(): A,_=r.accuracy_matrix([(1,0),(0,1)]); assert all(x>=0 for x in r.forgetting(A))
def test_naive_forgets_old(): A,_=r.accuracy_matrix([(1,0),(0,1)],lam=0); assert r.forgetting(A)[0]>0
def test_ewc_changes_trajectory(): a,_=r.accuracy_matrix([(1,0),(0,1)],lam=0);b,_=r.accuracy_matrix([(1,0),(0,1)],lam=1);assert a!=b
def test_ewc_fixture_reduces_old_forgetting(): a,_=r.accuracy_matrix([(1,0),(0,1)],lam=0);b,_=r.accuracy_matrix([(1,0),(0,1)],lam=1);assert r.forgetting(b)[0]<r.forgetting(a)[0]
def test_population_size(): assert len(r.population_step([(0,0),(1,0)],[(1,0)]))==3
def test_population_keeps_elite(): p=r.population_step([(0,0),(1,0)],[(1,0)]);assert p[0]==(1,0)
def test_quality_bounded(): assert 0<=r.quality((99,99),(0,0))<=1
def test_zero_lambda_anchor_equivalent(): assert r.step((.2,.3),(1,0),anchor=(0,0),importance=(1,1),lam=0)==r.step((.2,.3),(1,0))
def test_results_serializable(): import json; json.dumps(r.results())
