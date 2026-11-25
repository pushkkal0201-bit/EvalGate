import math

def cosine_similarity(a,b):
    if not a or len(a)!=len(b):
        raise ValueError("Embedding dimensions must match")
    if not all(math.isfinite(x) for x in [*a,*b]):
        raise ValueError("Non-finite embedding")
    na=math.hypot(*a)
    nb=math.hypot(*b)
    if not na or not nb:
        raise ValueError("Zero embedding")
    return max(-1.0,min(1.0,sum((x/na)*(y/nb) for x,y in zip(a,b))))

def regression(baseline,candidate,tolerance=0.0):
    if not all(math.isfinite(x) and 0<=x<=1 for x in (baseline,candidate,tolerance)):
        raise ValueError("Expected scores in [0,1]")
    return {"delta":candidate-baseline,"passed":candidate+tolerance>=baseline}
