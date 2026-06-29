import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. CSS로 모든 배치 고정 (Flexbox)
        st.markdown("""
            <style>
                .main-row { 
                    display: flex !important; 
                    flex-direction: row !important; 
                    align-items: center !important; 
                    justify-content: center !important; 
                    gap: 10px !important; 
                    width: 100% !important;
                }
                .card { 
                    width: 130px !important; 
                    height: 90px !important; 
                    border: 1px solid #ccc !important; 
                    border-radius: 8px !important; 
                    padding: 5px !important; 
                    background: white !important; 
                    text-align: center !important;
                    flex-shrink: 0 !important; 
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 2. 버튼 클릭 시 상태 업데이트 (이벤트 분리)
        # 폼(form)을 사용하지 않고 상태값만 변경하여 재실행
        def go_prev():
            if st.session_state.current_page > 0: st.session_state.current_page -= 1
        
        def go_next():
            st.session_state.current_page += 1

        # 3. HTML 레이아웃 (줄바꿈 방지)
        st.markdown('<div class="main-row">', unsafe_allow_html=True)
        
        # 버튼을 st.button이 아닌 CSS 버튼으로 대체하는 게 정석이지만, 
        # 스트림릿 버튼을 써야 한다면 버튼을 column으로 묶지 말고 직접 나열
        if st.button("◀"): go_prev(); st.rerun()
        
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]
        
        for game in page_games:
            st.markdown(f"""
                <div class="card">
                    <div style="font-size:9px;">{game.get('display_date', '')}</div>
                    <div style="font-weight:bold; font-size:12px;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                    <div style="font-size:12px;">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
            
        if st.button("▶"): go_next(); st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
