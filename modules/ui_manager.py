import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        items_per_page = 6
        start = st.session_state.get('current_page', 0) * items_per_page
        page_games = game_data_list[start:start + items_per_page]

        # 1. 상단 정렬 및 화살표 버튼 (가운데 영역 확보)
        st.markdown("<div style='display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        if st.button("◀ 이전"):
            if st.session_state.get('current_page', 0) > 0:
                st.session_state.current_page -= 1
                st.rerun()
        st.write("경기 목록")
        if st.button("다음 ▶"):
            st.session_state.current_page = st.session_state.get('current_page', 0) + 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # 2. 카드 배치 (화면 가운데 기준, 가로로 넓게)
        # 전체 화면을 100% 활용하면서 카드가 서로 겹치지 않게 간격 유지
        if page_games:
            # 6개의 카드를 넓게 배치
            cols = st.columns([1]*6) 
            for i in range(6):
                with cols[i]:
                    if i < len(page_games):
                        game = page_games[i]
                        # 카드 가로 폭 확장 및 간격 조정
                        st.markdown(f"""
                            <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 15px; text-align: center; background: white; height: 180px; margin: 0 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                                <div style="font-size: 12px; color: #6b7280; font-weight: bold; margin-bottom: 5px;">{game.get('display_date', '')}</div>
                                <div style="font-size: 16px; font-weight: 800; color: #dc2626; margin-bottom: 12px;">{game.get('display_time', '')}</div>
                                <div style="font-size: 13px; font-weight: 700; margin-bottom: 6px;">{game.get('away_name', 'AWAY')[:12]}</div>
                                <div style="font-size: 13px; font-weight: 700;">{game.get('home_name', 'HOME')[:12]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # 상세보기 버튼 (카드 아래 정렬)
                        if st.button("상세보기", key=f"btn_{game.get('game_id', i)}"):
                            st.session_state.selected_game_id = game.get('game_id')
                            st.rerun()
                    else:
                        st.write("") 
        else:
            st.info("해당 페이지에 경기가 없습니다.")
