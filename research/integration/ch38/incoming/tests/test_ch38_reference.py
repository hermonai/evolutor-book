import importlib.util,numpy as np
from pathlib import Path
p=Path(__file__).parents[1]/"drafts/ch38/reference.py";s=importlib.util.spec_from_file_location("r",p);r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
def test_marginal(): p=[.55,.25,.15,.05];q=[.45,.35,.15,.05];np.testing.assert_allclose(r.output_distribution(p,q),p,atol=1e-15)
def test_equal(): np.testing.assert_allclose(r.output_distribution([.2,.3,.5],[.2,.3,.5]),[.2,.3,.5])
def test_tv(): p=r.normalize([.7,.2,.1]);q=r.normalize([.4,.4,.2]);assert abs(np.minimum(p,q).sum()-(1-.5*np.abs(p-q).sum()))<1e-15
def test_residual(): x=r.correction_distribution([.7,.2,.1],[.4,.4,.2]);assert np.all(x>=0) and abs(x.sum()-1)<1e-15
def test_support_gap(): np.testing.assert_allclose(r.output_distribution([.5,.5],[1,0]),[.5,.5])
def test_seed(): p=[.6,.4];q=[.5,.5];assert r.speculative_block([p]*4,[q]*4,9)==r.speculative_block([p]*4,[q]*4,9)
def test_attention():
 g=np.random.default_rng(1);q=g.normal(size=8);K=g.normal(size=(23,8));V=g.normal(size=(23,5));a=r.dense_attention(q,K,V)
 for t in [1,2,4,7,64]:np.testing.assert_allclose(r.tiled_online_attention(q,K,V,t),a,rtol=1e-12,atol=1e-12)
def test_stable(): q=np.array([1e3,0.]);K=np.array([[1e3,0.],[999.,0.]]);V=np.eye(2);assert np.isfinite(r.tiled_online_attention(q,K,V,1)).all()
def test_traffic(): assert r.traffic_model(1024,64,64,tiled=True)["total"]<r.traffic_model(1024,64,64,tiled=False)["total"]
def test_bad_prob():
 try:r.normalize([-1,2]);assert False
 except ValueError:pass
def test_bad_shape():
 try:r.dense_attention(np.zeros(3),np.zeros((2,4)),np.zeros((2,5)));assert False
 except ValueError:pass
