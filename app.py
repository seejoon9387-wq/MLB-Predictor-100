import streamlit as st
import pandas as pd
import requests
from modules.main_trainer import MLBUnifiedTrainer

st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")

@st.cache_data(ttl=300)
def get_mlb_schedule():
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate=2026-06-29&endDate=2026-06-29"
    try:
        data = requests.get(url).json()
        games = [{'Time': g.get('gameDate', '')[11:16], 'Away': g['teams']['away']['team']['name'], 
                  'Home': g['teams']['home']['team']['name'], 'game_pk': g['gamePk']} 
                 for d in data.get('dates', []) for g in d.get('games', [])]
        return pd.DataFrame(games)
    except: return pd.DataFrame()

def main():
    st.title("⚾ MLB AI 전문 분석 대시보드")
    df = get_mlb_schedule()
    
    if not df.empty:
        event = st.dataframe(df[['Time', 'Away', 'Home']], use_container_width=True, height=400, 
                             hide_index=True, selection_mode="single-row", on_select="rerun")
        
        if event.selection.rows:
            selected_game = df.iloc[event.selection.rows[0]]
            st.divider()
            st.subheader(f"🔍 {selected_game['Away']} vs {selected_game['Home']} 정밀 분석")
            
            if st.button("🚀 엔진 가동"):
                with st.spinner('AI 분석 중...'):
                    result = MLBUnifiedTrainer().analyze({'game_pk': selected_game['game_pk']})
                    
                    col1, col2 = st.columns(2)
                    col1.metric("예측 승자", result['winner'])
                    col2.metric("확신도", f"{result['confidence']}%")
                    
                    st.markdown("### 📈 승리 확률 분석")
                    # 승률 바 시각화 (Home 기준)
                    prog = result['score'] if result['winner'] == 'Home' else 1 - result['score']
                    st.progress(prog)
                    
                    st.markdown("---")
                    st.markdown(result['detailed_report'])
    else:
        st.warning("일정 데이터를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
