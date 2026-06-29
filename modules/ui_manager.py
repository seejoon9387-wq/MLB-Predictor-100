import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """좌우 화살표 클릭 시 페이지가 넘어가는 내비게이션"""
        items_per_page = 6
        total_pages = (len(game_data_list) + items_per_page - 1) // items_per_page

        # 세션 상태가 없으면 초기화
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        # 버튼 로직: 버튼이 눌릴 때마다 세션 상태 업데이트
        cols = st.columns([1, 10, 1])
        
        with cols[0]:
            if st.button("◀ 이전"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
        
        with cols[2]:
            if st.button("다음 ▶"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1

        # 현재 페이지 데이터 슬라이싱
        start = st.session_state.current_page * items_per_page
        end = start + items_per_page
        page_games = game_data_list[start:end]

        # 경기 카드 렌더링
        with cols[1]:
            game_cols = st.columns(len(page_games))
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
