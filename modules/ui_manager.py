import streamlit as st

class UIManager:
    @staticmethod
    def render_scoreboard(data):
        # 디자인 틀: 점수판
        st.markdown(f"""
            <div style="background:#1e2025; padding:20px; border-radius:15px; border:1px solid #333; text-align:center;">
                <h2 style="color:#ffffff;">{data.get('away_team')} {data.get('away_score')} : {data.get('home_score')} {data.get('home_team')}</h2>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_data_table(stats):
        # 디자인 틀: 통계 표
        st.write("---")
        st.subheader("📋 분석 상세 지표")
        st.table(stats) # 엔진 결과가 자동으로 여기에 예쁘게 표시됨
