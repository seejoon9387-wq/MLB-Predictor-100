import pandas as pd
import os

class DataManager:
    GAME_DB = "mlb_games.csv"
    PLAYER_DB = "mlb_players.csv"

    @staticmethod
    def save_game(game_data):
        df = pd.DataFrame([game_data])
        df.to_csv(DataManager.GAME_DB, mode='a', header=not os.path.exists(DataManager.GAME_DB), index=False)

    @staticmethod
    def save_player_stats(player_list):
        if not player_list: return
        df = pd.DataFrame(player_list)
        df.to_csv(DataManager.PLAYER_DB, mode='a', header=not os.path.exists(DataManager.PLAYER_DB), index=False)

    @staticmethod
    def get_player_stats():
        return pd.read_csv(DataManager.PLAYER_DB) if os.path.exists(DataManager.PLAYER_DB) else pd.DataFrame()
