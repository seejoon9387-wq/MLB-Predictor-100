import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)
        
        # ... (이전 페이지 로직 동일) ...
        start = st.session_state.get('current_page', 0) * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 시간 포맷 정제 (시간만 추출하거나 가독성 높임)
                    time_val = str(game.get('game_time', 'TBA')).split(' ')[-1] # 'HH:MM' 형태 추출 시도
                    away = game.get('away_name', 'AWAY')
                    home = game.get('home_name', 'HOME')
                    a_score = game.get('away_score', 0)
                    h_score = game.get('home_score', 0)
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:15px; text-align:center; box-shadow: 0 3px 6px rgba(0,0,0,0.1); height:160px;">
                            <div style="color:#4b5563; font-size:14px; font-weight:bold; margin-bottom:10px;">⏰ {time_val}</div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:16px; margin-bottom:8px;">
                                <span>{away}</span> <span style="color:{'#ef4444' if a_score > h_score else '#374151'};">{a_score}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:16px;">
                                <span>{home}</span> <span style="color:{'#ef4444' if h_score > a_score else '#374151'};">{h_score}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
