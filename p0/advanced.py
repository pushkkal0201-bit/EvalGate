import math

def cosine_similarity(a,b):
    if not a or len(a)!=len(b):
        raise ValueError("Embedding dimensions must match")
    if not all(math.isfinite(x) for x in [*a,*b]):
        raise ValueError("Non-finite embedding")
    scale_a = max(map(abs, a))
    scale_b = max(map(abs, b))
    if not scale_a or not scale_b:
        raise ValueError("Zero embedding")
    scaled_a = [value / scale_a for value in a]
    scaled_b = [value / scale_b for value in b]
    norm = math.hypot(*scaled_a) * math.hypot(*scaled_b)
    similarity = math.fsum(x * y for x, y in zip(scaled_a, scaled_b)) / norm
    return max(-1.0, min(1.0, similarity))


def regression(baseline,candidate,tolerance=0.0):
    if not all(math.isfinite(x) and 0<=x<=1 for x in (baseline,candidate,tolerance)):
        raise ValueError("Expected scores in [0,1]")
    return {"delta":candidate-baseline,"passed":candidate+tolerance>=baseline}
