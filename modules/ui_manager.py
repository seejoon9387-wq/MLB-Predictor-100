import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        total_pages = max(1, (len(game_data_list) + items_per_page - 1) // items_per_page)

        if 'current_page' not in st.session_state or st.session_state.current_page >= total_pages:
            st.session_state.current_page = 0

        # [고정 디자인] 화살표 버튼 영역
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            if st.button("◀"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with col3:
            if st.button("▶"):
                if st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

        # [고정 디자인] 카드 배치 영역 (CSS Grid 사용)
        start = st.session_state.current_page * items_per_page
        end = min(start + items_per_page, len(game_data_list))
        page_games = game_data_list[start:end]

        # 6개 카드를 수평으로 고정 배치하는 HTML/CSS
        card_html = '<div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-top: 20px;">'
        
        for game in page_games:
            card_html += f"""
                <div style="border: 1px solid #d1d5db; border-radius: 10px; padding: 10px; text-align: center; background: white; height: 160px;">
                    <div style="font-size: 11px; color: #6b7280; font-weight: bold;">{game.get('display_date', '')}</div>
                    <div style="font-size: 14px; font-weight: bold; color: #dc2626; margin-bottom: 8px;">{game.get('display_time', '')}</div>
                    <div style="font-size: 12px; font-weight: bold; margin-bottom: 5px;">{game.get('away_name', 'AWAY')} ({game.get('away_score', 0)})</div>
                    <div style="font-size: 12px; font-weight: bold;">{game.get('home_name', 'HOME')} ({game.get('home_score', 0)})</div>
                </div>
            """
        card_html += '</div>'
        
        st.markdown(card_html, unsafe_allow_html=True)
