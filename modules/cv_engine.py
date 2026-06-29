# modules/cv_engine.py
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

def perform_time_series_cv(model, X, y, n_splits=5):
    """
    시간순으로 분할하는 교차 검증 수행
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    scores = []
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        model.fit(X_train, y_train)
        score = model.score(X_val, y_val)
        scores.append(score)
        print(f"Fold {fold+1} Accuracy: {score:.4f}")
        
    print(f"평균 교차 검증 정확도: {np.mean(scores):.4f}")
    return scores
