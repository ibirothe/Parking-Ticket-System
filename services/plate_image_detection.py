import simplelpr

setup_params = simplelpr.EngineSetupParms()
engine = simplelpr.SimpleLPR(setup_params)

engine.set_countryWeight(34, 1.0)
engine.realizeCountryWeights()

processor = engine.createProcessor()

candidates = processor.analyze("../images/car_1.jpg")

for candidate in candidates:
    for match in candidate.matches:
        print(f"Plate: {match.text}")
        print(f"Confidence: {match.confidence:.3f}")
