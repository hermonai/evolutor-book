import importlib.util
from pathlib import Path
import sys
import itertools
import numpy as np
import pytest
import torch

S=importlib.util.spec_from_file_location("evod_batch_a_38",Path(__file__).parents[1]/"drafts/ch38/reference.py")
r=importlib.util.module_from_spec(S);sys.modules[S.name]=r;S.loader.exec_module(r)
torch.set_num_threads(1)


@pytest.mark.parametrize("p,q",[([.55,.25,.15,.05],[.45,.35,.15,.05]),([.2,.3,.5],[.2,.3,.5]),([.5,.5],[1,0]),([0,1],[1,0]),([1e308,1e308],[1,2])])
def test_marginal_tv_and_support(p,q):
    p,q=r.pair(p,q)
    np.testing.assert_allclose(r.output_distribution(p,q),p,atol=1e-15)
    assert abs(np.minimum(p,q).sum()-(1-.5*np.abs(p-q).sum()))<1e-15
    assert abs(r.correction_distribution(p,q).sum()-1)<1e-15


def test_wrong_correction_negative_control():
    p,q=np.array([.8,.2]),np.array([.2,.8])
    wrong=np.minimum(p,q)+(1-np.minimum(p,q).sum())*p
    assert np.max(np.abs(wrong-p))>.1


def test_history_conditional_joint_distribution_exact_enumeration():
    # Enumerate proposal/acceptance/residual paths for blocks of two, then
    # complete any rejected length-one block with target-only sampling.
    target=lambda prefix:np.array([.7,.3]) if not prefix else np.array([.2,.8]) if prefix[-1]==0 else np.array([.9,.1])
    draft=lambda prefix:np.array([.4,.6]) if not prefix else np.array([.8,.2])
    joint=np.zeros((2,2))
    for x in range(2):
        p,q=target(()),draft(())
        a=min(p[x],q[x])
        # First accepted: second rejection correction produces target law.
        joint[x,:]+=a*r.output_distribution(target((x,)),draft((x,)))
    residual=np.maximum(target(())-draft(()),0)
    for y in range(2):joint[y,:]+=residual[y]*target((y,))
    expected=np.array([target(())[x]*target((x,)) for x in range(2)])
    np.testing.assert_allclose(joint,expected,atol=1e-15)


def test_seeded_conditional_sampling_statistical_control():
    target=lambda prefix:[.8,.2] if not prefix or prefix[-1]==0 else [.1,.9]
    draft=lambda prefix:[.3,.7]
    rng=np.random.default_rng(38);counts=np.zeros((2,2))
    for _ in range(20000):
        prefix=()
        while len(prefix)<2:
            block,_=r.speculative_block(target,draft,prefix,2-len(prefix),rng)
            prefix+=block
        counts[prefix]+=1
    expected=np.array([[.64,.16],[.02,.18]])
    assert np.max(np.abs(counts/counts.sum()-expected))<.015


@pytest.mark.parametrize("seed",range(10))
def test_native_speculative_commit_and_rollback(seed):
    m=r.native.tiny_model();pool=r.paging.PagedKV(m,16,2);o=("t","live")
    h=pool.empty(o);pool.consume(h,o,(0,1,2))
    committed,n=r.native_speculative(pool,h,o,lambda prefix:[1.,0.,0.,0.],3,np.random.default_rng(seed))
    state=pool.flatten(h,o)
    assert state.tokens==(0,1,2)+committed
    _,oracle=r.native.prefill(m,o,state.tokens)
    for x,y in zip(state.layers,oracle.layers):
        torch.testing.assert_close(x.k,y.k,atol=2e-12,rtol=2e-12)
        torch.testing.assert_close(x.v,y.v,atol=2e-12,rtol=2e-12)
    assert len(pool._states)==1 and pool.audit()["references"]==len(pool.state(h,o).pages)


def test_native_speculative_oom_releases_branch():
    m=r.native.tiny_model();p=r.paging.PagedKV(m,2,2);o=("t","live")
    h=p.empty(o);p.consume(h,o,(0,1,2))
    before=p.flatten(h,o).seal,p.audit()
    with pytest.raises(MemoryError):r.native_speculative(p,h,o,lambda prefix:[1,0,0,0],2,np.random.default_rng(1))
    assert before==(p.flatten(h,o).seal,p.audit())


@pytest.mark.parametrize("tile",[1,2,3,7,64])
@pytest.mark.parametrize("past,count",[(0,6),(3,2),(5,1)])
def test_online_dense_sdpa_offset_and_allmasked(tile,past,count):
    g=torch.Generator().manual_seed(38)
    q=torch.randn(2,count,4,generator=g,dtype=torch.float64)
    k=torch.randn(2,past+count,4,generator=g,dtype=torch.float64)
    v=torch.randn(2,past+count,5,generator=g,dtype=torch.float64)
    mask=r.native.allowed_mask(past,count)
    dense=r.dense_attention(q,k,v,mask)
    online=r.online_attention(q,((k[:,i:i+tile],v[:,i:i+tile],mask[:,i:i+tile]) for i in range(0,past+count,tile)))
    sdpa=torch.nn.functional.scaled_dot_product_attention(q,k,v,attn_mask=mask,dropout_p=0.)
    torch.testing.assert_close(online,dense,atol=2e-12,rtol=2e-12)
    torch.testing.assert_close(online,sdpa,atol=2e-12,rtol=2e-12)
    zero=r.online_attention(q,[(k,v,torch.zeros_like(mask))])
    assert torch.equal(zero,torch.zeros_like(zero))


@pytest.mark.parametrize("tile",[1,2,4,32])
def test_complete_layered_native_online_parity(tile):
    m=r.native.tiny_model();o=("t","online");tokens=(0,1,2,3,0,2)
    for split in range(1,6):
        _,c=r.native.prefill(m,o,tokens[:split])
        y,c=r.online_consume(m,c,o,tokens[split:],tile)
        torch.testing.assert_close(y,r.native.full_oracle(m,tokens)[split:],atol=2e-12,rtol=2e-12)
        _,full=r.native.prefill(m,o,tokens)
        for x,z in zip(c.layers,full.layers):
            torch.testing.assert_close(x.k,z.k,atol=2e-12,rtol=2e-12)
            torch.testing.assert_close(x.v,z.v,atol=2e-12,rtol=2e-12)


def test_paged_attention_visits_logical_blocks_and_wrong_offset_control():
    m=r.native.tiny_model();p=r.paging.PagedKV(m,8,2);o=("t","p")
    h=p.empty(o);p.consume(h,o,(0,1))
    junk=p.empty(("t","junk"));p.consume(junk,("t","junk"),(3,3))
    p.consume(h,o,(2,3,0))
    q=torch.tensor([[[1.,0,0,0],[0,1.,0,0]]]*2,dtype=torch.float64)
    c=p.flatten(h,o);mask=r.native.allowed_mask(3,2)
    for layer in range(2):
        got=r.paged_attention(p,h,o,layer,q,[3,4])
        expected=r.dense_attention(q,c.layers[layer].k,c.layers[layer].v,mask)
        torch.testing.assert_close(got,expected,atol=2e-12,rtol=2e-12)
        wrong=r.dense_attention(q,c.layers[layer].k,c.layers[layer].v,torch.ones(2,5,dtype=torch.bool).tril())
        assert (got-wrong).abs().max()>.001


def test_extreme_scores_first_empty_tile_and_traffic():
    q=torch.tensor([[[1000.,0]]],dtype=torch.float64)
    k=torch.tensor([[[1000.,0],[999.,0]]],dtype=torch.float64)
    v=torch.eye(2,dtype=torch.float64)[None]
    tiles=[(k[:,:1],v[:,:1],torch.zeros(1,1,dtype=torch.bool)),(k[:,1:],v[:,1:],torch.ones(1,1,dtype=torch.bool))]
    torch.testing.assert_close(r.online_attention(q,tiles),v[:,1:])
    assert r.traffic_model(4096,128,128)["total"]-r.traffic_model(4096,128,128,tiled=True)["total"]==16384


@pytest.mark.parametrize("bad",[[-1,2],[0,0],[np.nan,1],[np.inf,1],[]])
def test_invalid_probabilities(bad):
    with pytest.raises(ValueError):r.normalize(bad)


def test_invalid_contracts():
    with pytest.raises(ValueError):r.pair([1,0],[1,0,0])
    with pytest.raises(ValueError):r.verify((0,),[[1,0]],[[0,1]],np.random.default_rng())
    with pytest.raises(ValueError):r.online_attention(torch.ones(1,1,2,dtype=torch.float64),[])


def test_online_worked_summary_and_tile_permutation():
    q=torch.ones(1,1,1,dtype=torch.float64)
    k=torch.tensor([0.,np.log(2),np.log(4)],dtype=torch.float64).reshape(1,3,1)
    v=torch.tensor([2.,4.,8.],dtype=torch.float64).reshape(1,3,1)
    mask=torch.ones(1,3,dtype=torch.bool)
    for order in itertools.permutations(range(3)):
        tiles=[(k[:,i:i+1],v[:,i:i+1],mask[:,i:i+1]) for i in order]
        torch.testing.assert_close(r.online_attention(q,tiles),torch.tensor([[[6.]]],dtype=torch.float64))
    wrong_accumulator=(5+8)/1.75
    assert abs(wrong_accumulator-6)>1
