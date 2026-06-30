import numpy as np
from sklearn.model_selection import TimeSeriesSplit

class TimeSeriesValidator:
    def __init__(self, n_splits=5):
        # 시간을 고려한 5단계 교차 검증 객체
        self.tscv = TimeSeriesSplit(n_splits=n_splits)

    def get_split_indices(self, X):
        """
        데이터셋의 인덱스를 시계열 순서에 따라 분할합니다.
        반환값: (train_index, test_index) 리스트
        """
        splits = []
        for train_index, test_index in self.tscv.split(X):
            splits.append((train_index, test_index))
        return splits

# 모듈 사용 예시 (결과 확인용)
if __name__ == "__main__":
    # 20일간의 가상 일별 데이터 인덱스 생성
    X = np.zeros((20, 1)) 
    
    validator = TimeSeriesValidator(n_splits=3)
    splits = validator.get_split_indices(X)
    
    for i, (train, test) in enumerate(splits):
        print(f"Fold {i+1}: 학습 인덱스 수={len(train)}, 검증 인덱스 수={len(test)}")
        print(f"  검증 기간: {test[0]} ~ {test[-1]}")
