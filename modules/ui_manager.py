import streamlit as st
import pandas as pd

class UIManager:
    @staticmethod
    def render_scoreboard(home_name, home_score, away_name, away_score):
        st.markdown(f"""
            <div style="background:#1e2025; padding:20px; border-radius:10px; text-align:center;">
                <h3>{away_name} {away_score} : {home_score} {home_name}</h3>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_stats_table(stats):
        st.subheader("📋 상세 분석 지표")
        df = pd.DataFrame([
            {"지표": key.upper(), "Home": stats.get(f"h_{key}"), "Away": stats.get(f"a_{key}")}
            for key in ['win_rate', 'era', 'ops', 'avg']
        ])
        st.table(df)
