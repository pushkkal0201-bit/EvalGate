import random

def paired_bootstrap(baseline,candidate, samples=2000,seed=42):
    if len(baseline)!=len(candidate) or not baseline or samples<100 or samples>10000:
        raise ValueError("Invalid paired dataset")
    if not all(0<=x<=1 for x in [*baseline,*candidate]):
        raise ValueError("Scores must be in [0,1]")
    delta=[b-a for a,b in zip(baseline,candidate)]
    rng=random.Random(seed)
    means=sorted(sum(rng.choices(delta,k=len(delta)))/len(delta) for _ in range(samples))
    return {"delta":sum(delta)/len(delta),"lower":means[int(.025*samples)],"upper":means[int(.975*samples)],"method":"paired percentile bootstrap"}
