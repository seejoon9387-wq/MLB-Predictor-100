import streamlit as st
from modules.ui_manager import UIManager

def main():
    st.set_page_config(layout="wide")
    
    # 예시: 30개 팀 경기 (15개 매치 생성)
    # 실제로는 load_data() 등을 통해 CSV나 API에서 데이터를 받아오세요.
    all_games = [
        {'away_name': f'AW{i}', 'away_score': 0, 'home_name': f'HO{i}', 'home_score': 0} 
        for i in range(1, 16)
    ]
    
    st.title("⚾ MLB 실시간 경기 센터")
    
    # 6개씩 끊어서 보여주는 내비게이션 바
    UIManager.render_game_navbar(all_games)
    
    st.divider()
    st.write("분석 엔진 결과가 여기에 표시됩니다.")

if __name__ == "__main__":
    main()
