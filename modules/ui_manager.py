import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """상단 경기 내비게이션 바 전체 컴포넌트"""
        st.markdown("""
            <style>
                .game-card { 
                    background: #262730; border: 1px solid #454545; border-radius: 10px; 
                    padding: 10px; width: 150px; text-align: center; color: white;
                    display: inline-block; margin: 5px; cursor: pointer;
                }
                .game-card:hover { border: 1px solid #ff4b4b; }
                .score-text { font-weight: bold; font-family: monospace; }
            </style>
        """, unsafe_allow_html=True)

        cols = st.columns(len(game_data_list))
        for i, game in enumerate(game_data_list):
            with cols[i]:
                st.markdown(f"""
                    <div class="game-card">
                        <div style="font-size:10px; color:#888;">종료</div>
                        <div style="display:flex; justify-content:space-between;">
                            <span>{game['away_name']}</span> <span class="score-text">{game['away_score']}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between;">
                            <span>{game['home_name']}</span> <span class="score-text">{game['home_score']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    @staticmethod
    def render_main_dashboard(result):
        """메인 분석 화면 전체 컴포넌트"""
        st.subheader("⚾ AI 분석 대시보드")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("예측 승자", result.get('winner', 'N/A'))
        with col2:
            st.metric("확신도", f"{result.get('confidence', 0)}%")
        st.progress(result.get('score', 0))
