import streamlit as st
from datetime import datetime
import pytz
# statsapi가 설치되어 있어야 합니다. (pip install mlb-statsapi)
import statsapi 

class UIManager:
    @staticmethod
    def get_kst_time(utc_iso_string):
        """UTC 시간을 한국 시간(KST)으로 변환"""
        try:
            # API에서 오는 시간 형식에 맞춰 파싱 (예: 2026-06-30T18:30:00Z)
            dt = datetime.strptime(utc_iso_string, "%Y-%m-%dT%H:%M:%SZ")
            dt = dt.replace(tzinfo=pytz.utc)
            return dt.astimezone(pytz.timezone('Asia/Seoul')).strftime("%H:%M")
        except:
            return "진행중"

    @staticmethod
    def fetch_mlb_data():
        """오늘 날짜의 MLB 경기 데이터를 가져오고 가공"""
        games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'))
        game_list = []
        for g in games:
            game_list.append({
                "display_date": g['game_date'],
                "display_time": UIManager.get_kst_time(g['game_datetime']),
                "away_name": g['away_name'],
                "away_score": g.get('away_score', 0),
                "home_name": g['home_name'],
                "home_score": g.get('home_score', 0)
            })
        return game_list

    @staticmethod
    def render_game_navbar():
        # CSS는 레이아웃 고정을 위해 유지
        st.markdown("""
            <style>
                .custom-card { width: 100% !important; height: 180px !important; border: 2px solid #d9ded5 !important; border-radius: 12px !important; background-color: #fcfcf8; display: flex !important; flex-direction: column !important; justify-content: space-around !important; align-items: center !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important; padding: 10px 0 !important; }
                .card-wrapper { padding: 5px; }
                .text-row { display: flex !important; justify-content: center !important; align-items: center !important; width: 100% !important; height: 30px !important; text-align: center !important; }
                .text-date { font-size: 12px !important; color: #697465 !important; font-weight: 500; }
                .text-team { font-weight: 800 !important; font-size: 14px !important; color: #111827; }
                .text-score { font-weight: 900 !important; font-size: 18px !important; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        game_data_list = UIManager.fetch_mlb_data()

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            if st.button("◀", key="p"):
                if st.session_state.current_page > 0: st.session_state.current_page -= 1
        with col3:
            if st.button("▶", key="n"):
                st.session_state.current_page += 1

        card_cols = st.columns(6)
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    st.markdown(f"""
                        <div class="card-wrapper">
                            <div class="custom-card">
                                <div class="text-row text-date">{game['display_date']} {game['display_time']}</div>
                                <div class="text-row text-team">{game['away_name']}</div>
                                <div class="text-row text-score">{game['away_score']} : {game['home_score']}</div>
                                <div class="text-row text-team">{game['home_name']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
