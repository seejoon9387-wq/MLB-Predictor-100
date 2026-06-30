import os

# 프로젝트 루트 경로 확보
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "data")

SCHEMA = {
    'woba_value': {'min': 0, 'max': 1.5, 'median': 0.320},
    'launch_speed': {'min': 0, 'max': 125, 'median': 88.0},
    'temp_f': {'min': 30, 'max': 110, 'median': 70.0}
}
