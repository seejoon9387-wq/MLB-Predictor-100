import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # 1. 카드 크기 고정 스타일 (가장 중요)
        st.markdown("""
            <style>
                .fixed-card { 
                    width: 160px !important; 
                    height: 120px !important; 
                    min-width: 160px !important;
                    border: 1px solid #ccc; 
                    border-radius: 8px; 
                    padding: 10px; 
                    background: white; 
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    overflow: hidden; /* 글자가 넘쳐도 카드 크기 유지 */
                }
                /* 텍스트 넘침 방지 */
                .card-text { 
                    white-space: nowrap; 
                    overflow: hidden; 
                    text-overflow: ellipsis;
                    font-size: 11px;
                }
            </style>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state: st.session_state.current_page = 0
        
        # 8개 컬럼 배치는 유지 (레이아웃 틀 고정)
        cols = st.columns([0.5, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 0.5])
        
        start = st.session_state.current_page * 6
        page_games = game_data_list[start:start + 6]

        with cols[0]:
            if st.button("◀", key="prev"):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1; st.rerun()

        for i in range(6):
            with cols[i+1]:
                if i < len(page_games):
                    game = page_games[i]
                    # 고정된 크기의 fixed-card 클래스 적용
                    st.markdown(f"""
                        <div class="fixed-card">
                            <div class="card-text" style="color:gray;">{game.get('display_date', '')}</div>
                            <div class="card-text" style="font-weight:bold; margin-top:5px;">{game.get('away_name', 'AWY')} {game.get('away_score', 0)}</div>
                            <div class="card-text">{game.get('home_name', 'HOM')} {game.get('home_score', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("") 

        with cols[7]:
            if st.button("▶", key="next"):
                st.session_state.current_page += 1; st.rerun()
