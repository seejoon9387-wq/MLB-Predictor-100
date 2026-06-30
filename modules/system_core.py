from mlb_engine.data_engine import DataEngine
from mlb_engine.feature_engine import FeatureEngine
from mlb_engine.inference_engine import InferenceEngine
from mlb_engine.validation_engine import ValidationEngine
from mlb_engine.tactical_engine import TacticalEngine

class SystemCore:
    def __init__(self):
        self.data = DataEngine()
        self.feature = FeatureEngine()
        self.inference = InferenceEngine()
        self.validation = ValidationEngine()
        self.tactical = TacticalEngine()

    def run_full_analysis(self, raw_data):
        # 통합된 전체 워크플로우 실행
        data = self.data.process(raw_data)
        features = self.feature.generate(data)
        pred = self.inference.run_inference(features)
        tactical = self.tactical.simulate_tactics(features)
        return self.validation.audit({"pred": pred, "tactical": tactical})
