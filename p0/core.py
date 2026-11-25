def evaluate(cases):
    if not cases:
        raise ValueError("Golden dataset cannot be empty")
    results = []
    for case in cases:
        expected = case["expected"].strip().casefold()
        actual = case["actual"].strip().casefold()
        results.append(expected == actual)
    return {"exact_match": sum(results)/len(results), "count": len(results), "results": results}
