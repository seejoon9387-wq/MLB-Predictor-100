import pandas as pd
import os

class DataManager:
    # 경로를 하드코딩하지 않고 관리하기 위해 config를 나중에 연동할 예정입니다.
    GAME_DB = "data/mlb_games.csv"
    PLAYER_DB = "data/mlb_players.csv"

    @staticmethod
    def load_latest_stats():
        """분석에 필요한 전체 데이터를 로드하고 검증합니다."""
        if not os.path.exists(DataManager.PLAYER_DB):
            return pd.DataFrame()
        
        df = pd.read_csv(DataManager.PLAYER_DB)
        # 데이터 정제: 결측치 처리 및 분석 필수 컬럼 존재 확인
        df = df.fillna(0) 
        return df

    @staticmethod
    def get_player_data(player_name):
        """특정 선수의 데이터만 추출 (엔진 호출용)"""
        df = DataManager.load_latest_stats()
        if player_name in df['player_name'].values:
            return df[df['player_name'] == player_name].iloc[0].to_dict()
        return None

    @staticmethod
    def save_game(game_data):
        """경기 결과 저장"""
        df = pd.DataFrame([game_data])
        # 폴더가 없으면 자동 생성
        os.makedirs(os.path.dirname(DataManager.GAME_DB), exist_ok=True)
        df.to_csv(DataManager.GAME_DB, mode='a', header=not os.path.exists(DataManager.GAME_DB), index=False)

    @staticmethod
    def save_player_stats(player_list):
        """통계 업데이트"""
        if not player_list: return
        df = pd.DataFrame(player_list)
        os.makedirs(os.path.dirname(DataManager.PLAYER_DB), exist_ok=True)
        df.to_csv(DataManager.PLAYER_DB, mode='a', header=not os.path.exists(DataManager.PLAYER_DB), index=False)
