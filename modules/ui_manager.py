import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """항상 일정한 크기의 카드를 유지하는 내비게이션 바"""
        items_per_page = 6
        total_pages = (len(game_data_list) + items_per_page - 1) // items_per_page

        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0

        cols = st.columns([0.5, 10, 0.5])
        
        with cols[0]:
            if st.button("◀ 이전"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        
        with cols[2]:
            if st.button("다음 ▶"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

        # 현재 페이지 데이터 가져오기
        start = st.session_state.current_page * items_per_page
        end = start + items_per_page
        page_games = game_data_list[start:end]

        # 6칸을 고정으로 가지는 그리드 레이아웃
        with cols[1]:
            # html로 6개 그리드 컨테이너 생성
            grid_html = """
            <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px;">
            """
            for game in page_games:
                away_color = "red" if game['away_score'] > game['home_score'] else "#333333"
                home_color = "red" if game['home_score'] > game['away_score'] else "#333333"
                
                grid_html += f"""
                    <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:12px; padding:12px; text-align:center; color:#333333; font-size:14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="color:#6b7280; font-size:12px; margin-bottom:6px; font-weight:bold;">{game['match_time']}</div>
                        <div style="display:flex; justify-content:space-between; padding:2px 0;">
                            <span>{game['away_name']}</span> <b style="color:{away_color};">{game['away_score']}</b>
                        </div>
                        <div style="display:flex; justify-content:space-between; padding:2px 0;">
                            <span>{game['home_name']}</span> <b style="color:{home_color};">{game['home_score']}</b>
                        </div>
                    </div>
                """
            grid_html += "</div>"
            st.markdown(grid_html, unsafe_allow_html=True)
