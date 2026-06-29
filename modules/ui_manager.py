import streamlit as st
import pandas as pd

class UIManager:
    # 이 레이아웃 구조는 고정됩니다.
    @staticmethod
    def display_dashboard(result):
        """UI의 뼈대. 어떤 데이터를 넣어도 이 틀 안에서 작동합니다."""
        
        # 1. 스코어보드 (상단 고정)
        UIManager._render_scoreboard(result.get('teams', ('Home', 'Away')))
        
        # 2. 분석 결과 영역 (중앙 고정)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("예측 승자", result.get('winner', 'N/A'))
        with col2:
            st.metric("확신도", f"{result.get('confidence', 0)}%")
        st.progress(result.get('score', 0))
        
        # 3. 상세 지표 테이블 (하단 고정)
        UIManager._render_stats_table(result.get('stats', {}))

    @staticmethod
    def _render_scoreboard(teams):
        st.markdown(f"### 🏟️ {teams[0]} vs {teams[1]}")

    @staticmethod
    def _render_stats_table(stats):
        st.markdown("---")
        st.subheader("📊 상세 분석 지표")
        # 여기서 통계 키를 추가/삭제해도 레이아웃은 변하지 않습니다.
        data = [{"지표": k.upper(), "값": v} for k, v in stats.items()]
        st.table(pd.DataFrame(data))
