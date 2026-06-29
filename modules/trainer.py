import joblib
from data_loader import load_data
from modules.cv_engine import perform_time_series_cv
from modules.feature_selector import remove_collinear_features
from xgboost import XGBClassifier

class MLBUnifiedTrainer:
    def __init__(self):
        self.data = load_data()

    def run(self):
        # 1. 데이터 전처리 및 공선성 제거
        df = self.data.sort_values('date').reset_index(drop=True)
        X = remove_collinear_features(df.drop(columns=['is_home_win', 'date', 'game_pk']))
        y = df['is_home_win']
        
        # 2. 모델 설정
        model = XGBClassifier(
            n_estimators=500, 
            learning_rate=0.05, 
            max_depth=5, 
            n_jobs=-1
        )
        
        # 3. 교차 검증을 통한 오버피팅 방지 검증
        print("시계열 교차 검증 시작...")
        perform_time_series_cv(model, X, y, n_splits=5)
        
        # 4. 최종 학습
        model.fit(X, y)
        joblib.dump(model, 'final_robust_model.pkl')
        print("교차 검증이 완료된 최종 모델 저장 완료.")

if __name__ == "__main__":
    trainer = MLBUnifiedTrainer()
    trainer.run()
