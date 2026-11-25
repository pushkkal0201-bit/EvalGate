from advanced import cosine_similarity, regression

def test_similarity():
    assert cosine_similarity([1,0],[1,0])==1
    assert cosine_similarity([1,0],[0,1])==0

def test_regression():
    assert not regression(.9,.8)["passed"]
