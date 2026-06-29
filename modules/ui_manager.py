import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        """경기 내비게이션 바 컴포넌트"""
        st.markdown("""
            <style>
                .game-card { 
                    background: #262730; border: 1px solid #454545; border-radius: 10px; 
                    padding: 10px; width: 150px; text-align: center; color: white;
                    display: inline-block; margin: 5px; cursor: pointer;
                }
            </style>
        """, unsafe_allow_html=True)

        if not game_data_list:
            st.write("데이터가 없습니다.")
            return

        cols = st.columns(len(game_data_list))
        for i, game in enumerate(game_data_list):
            with cols[i]:
                st.markdown(f"""
                    <div class="game-card">
                        <div style="font-size:10px;">종료</div>
                        <div>{game['away_name']} {game['away_score']}</div>
                        <div>{game['home_name']} {game['home_score']}</div>
                    </div>
                """, unsafe_allow_html=True)

    @staticmethod
    def render_main_dashboard(result):
        """메인 대시보드 컴포넌트"""
        st.subheader("⚾ AI 분석 대시보드")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("예측 승자", result.get('winner', 'N/A'))
        with col2:
            st.metric("확신도", f"{result.get('confidence', 0)}%")
