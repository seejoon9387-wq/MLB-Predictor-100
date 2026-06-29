import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """흰색 바탕 테두리 디자인 및 승리팀 점수 빨간색 표시"""
        items_per_page = 6
        total_pages = (len(game_data_list) + items_per_page - 1) // items_per_page

        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        cols = st.columns([0.5, 10, 0.5])
        
        with cols[0]:
            if st.button("◀"):
                st.session_state.current_page = max(0, st.session_state.current_page - 1)
        
        with cols[2]:
            if st.button("▶"):
                st.session_state.current_page = min(total_pages - 1, st.session_state.current_page + 1)

        start = st.session_state.current_page * items_per_page
        end = start + items_per_page
        page_games = game_data_list[start:end]

        with cols[1]:
            game_cols = st.columns(items_per_page)
            for i, game in enumerate(page_games):
                # 승리 팀 점수 빨간색 결정 로직
                away_color = "red" if game['away_score'] > game['home_score'] else "black"
                home_color = "red" if game['home_score'] > game['away_score'] else "black"
                
                with game_cols[i]:
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #dddddd; border-radius:8px; padding:6px; text-align:center; color:black; font-size:10px; box-shadow: 1px 1px 3px #eee;">
                            <div style="color:#888; margin-bottom:4px;">종료</div>
                            <div style="display:flex; justify-content:space-between; padding:0 2px;">
                                <span>{game['away_name']}</span> <b style="color:{away_color};">{game['away_score']}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; padding:0 2px;">
                                <span>{game['home_name']}</span> <b style="color:{home_color};">{game['home_score']}</b>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # 빈 공간 채우기
            for _ in range(items_per_page - len(page_games)):
                st.empty()
