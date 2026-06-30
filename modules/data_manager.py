import pandas as pd
import os
from modules.config import SCHEMA, DB_DIR

class DataManager:
    GAME_DB = os.path.join(DB_DIR, "mlb_games.csv")
    PLAYER_DB = os.path.join(DB_DIR, "mlb_players.csv")

    @staticmethod
    def validate_data(df):
        """데이터 품질을 SCHEMA 기준으로 검증"""
        for col, rules in SCHEMA.items():
            if col in df.columns:
                # 범위 밖의 데이터는 중앙값(median)으로 보정
                df[col] = df[col].clip(lower=rules['min'], upper=rules['max'])
        return df

    @staticmethod
    def load_latest_stats():
        if not os.path.exists(DataManager.PLAYER_DB):
            return pd.DataFrame()
        df = pd.read_csv(DataManager.PLAYER_DB)
        return DataManager.validate_data(df)

    @staticmethod
    def save_game(game_data):
        df = pd.DataFrame([game_data])
        os.makedirs(DB_DIR, exist_ok=True)
        df.to_csv(DataManager.GAME_DB, mode='a', header=not os.path.exists(DataManager.GAME_DB), index=False)
