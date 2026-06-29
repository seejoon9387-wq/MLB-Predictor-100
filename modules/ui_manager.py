import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)

        if 'current_page' not in st.session_state or st.session_state.current_page >= total_pages:
            st.session_state.current_page = 0

        # 버튼 영역
        c1, c2, c3 = st.columns([1, 10, 1])
        with c1:
            if st.button("◀ 이전"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with c3:
            if st.button("다음 ▶"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

        start = st.session_state.get('current_page', 0) * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    
                    # app.py에서 계산한 값 가져오기
                    date_val = game.get('display_date', '확인중')
                    time_val = game.get('display_time', '확인중')
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:10px; padding:10px; text-align:center; height:180px;">
                            <div style="font-size:12px; font-weight:bold; color:#4b5563;">{date_val}</div>
                            <div style="font-size:14px; font-weight:bold; color:#dc2626; margin-bottom:10px;">{time_val}</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('away_name', 'AWAY')}: {game.get('away_score', 0)}</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('home_name', 'HOME')}: {game.get('home_score', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("")
