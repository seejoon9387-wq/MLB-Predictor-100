import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 디자인 고정 CSS (초기 디자인의 핵심인 깔끔한 박스 스타일)
        st.markdown("""
            <style>
                .navbar-wrapper { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px; }
                .card-frame { 
                    border: 1px solid #d1d5db; border-radius: 12px; padding: 12px; 
                    background: white; width: 140px; height: 100px;
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .text-date { font-size: 10px; color: #6b7280; font-weight: bold; }
                .text-team { font-size: 13px; font-weight: 700; display: flex; justify-content: space-between; }
                .button-container { display: flex; gap: 5px; justify-content: center; }
            </style>
        """, unsafe_allow_html=True)

        # 2. 업데이트 버튼 및 페이지 관리
        st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)
        
        if st.button("🔄 업데이트"): st.rerun()
        
        if st.button("◀ 이전"):
            if st.session_state.get('current_page', 0) > 0:
                st.session_state.current_page -= 1
                st.rerun()

        # 3. 카드 6개 가로 배치 (HTML로 강제 고정)
        start = st.session_state.get('current_page', 0) * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="card-frame">
                    <div class="text-date">{game.get('display_date', '날짜 정보 없음')}</div>
                    <div class="text-team"><span>{game.get('away_name', 'AWAY')}</span><span>{game.get('away_score', 0)}</span></div>
                    <div class="text-team"><span>{game.get('home_name', 'HOME')}</span><span>{game.get('home_score', 0)}</span></div>
                </div>
            """, unsafe_allow_html=True)
            # 상세보기 버튼은 카드 아래에 작게 배치 (레이아웃 보호)
            if st.button("상세보기", key=f"btn_{game.get('game_id')}"):
                st.session_state.selected_game_id = game.get('game_id')
                st.rerun()

        if st.button("다음 ▶"):
            st.session_state.current_page = st.session_state.get('current_page', 0) + 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
