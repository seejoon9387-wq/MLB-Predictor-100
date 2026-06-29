import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """시간순 정렬된 데이터를 6개씩 페이지 단위로 렌더링"""
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
                away_color = "red" if game['away_score'] > game['home_score'] else "#333333"
                home_color = "red" if game['home_score'] > game['away_score'] else "#333333"
                
                with game_cols[i]:
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:12px; text-align:center; color:#333333; font-size:14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div style="color:#6b7280; font-size:12px; margin-bottom:6px; font-weight:bold;">{game['match_time']}</div>
                            <div style="display:flex; justify-content:space-between; padding:2px 0;">
                                <span>{game['away_name']}</span> <b style="color:{away_color};">{game['away_score']}</b>
                            </div>
                            <div style="display:flex; justify-content:space-between; padding:2px 0;">
                                <span>{game['home_name']}</span> <b style="color:{home_color};">{game['home_score']}</b>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            for _ in range(items_per_page - len(page_games)):
                st.empty()
