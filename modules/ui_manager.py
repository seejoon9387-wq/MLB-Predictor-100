import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 1. 화살표 버튼 배치
        c1, c2, c3 = st.columns([1, 10, 1])
        with c1:
            if st.button("◀", key="prev"):
                if st.session_state.get('current_page', 0) > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
        with c3:
            if st.button("▶", key="next"):
                st.session_state.current_page = st.session_state.get('current_page', 0) + 1
                st.rerun()

        # 2. 카드 배치 (6개 칼럼 강제 고정)
        if page_games:
            cols = st.columns(6) 
            for i in range(6):
                with cols[i]:
                    if i < len(page_games):
                        game = page_games[i]
                        # 카드 디자인
                        st.markdown(f"""
                            <div style="border: 1px solid #d1d5db; border-radius: 10px; padding: 10px; text-align: center; background: white; height: 160px; margin-bottom: 10px;">
                                <div style="font-size: 11px; color: #6b7280; font-weight: bold;">{game.get('display_date', '')}</div>
                                <div style="font-size: 14px; font-weight: bold; color: #dc2626; margin-bottom: 8px;">{game.get('display_time', '')}</div>
                                <div style="font-size: 12px; font-weight: bold; margin-bottom: 5px;">{game.get('away_name', 'AWAY')[:15]}</div>
                                <div style="font-size: 12px; font-weight: bold;">{game.get('home_name', 'HOME')[:15]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        # 상세 버튼
                        if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                            st.session_state.selected_game_id = game.get('game_id')
                            st.rerun()
                    else:
                        st.write("") # 빈 공간 유지
        else:
            st.write("표시할 경기가 없습니다.")
