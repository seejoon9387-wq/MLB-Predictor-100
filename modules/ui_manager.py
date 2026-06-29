import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        st.markdown("""
            <style>
                /* 전체 컨테이너를 강제로 화면 100%로 설정 */
                .main-layout { width: 100% !important; }
                
                /* 버튼들을 강제로 양옆으로 밀어냄 */
                .arrow-box { 
                    display: flex !important; 
                    justify-content: space-between !important; 
                    width: 100% !important; 
                    padding: 0 50px !important; 
                    margin-bottom: 20px;
                }
                
                /* 스트림릿 기본 버튼 강제 스타일 제거 */
                div.stButton > button { 
                    border: 2px solid #ccc !important;
                    background-color: white !important;
                    color: black !important;
                    padding: 10px 20px !important;
                    font-weight: bold !important;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # [중요] 버튼을 컬럼 안에 넣지 말고 직접 div로 감싸야 CSS가 먹힙니다.
        st.markdown('<div class="arrow-box">', unsafe_allow_html=True)
        
        # 버튼을 렌더링
        if st.button("◀", key="prev"):
            st.session_state.current_page = max(0, st.session_state.current_page - 1)
            st.rerun()
            
        if st.button("▶", key="next"):
            st.session_state.current_page += 1
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
