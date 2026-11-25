from intelligence import paired_bootstrap

def test_paired():
    assert paired_bootstrap([0,0],[1,1])["lower"]==1
