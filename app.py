import streamlit as st
import joblib
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="MLB 정밀 예측 시스템", layout="centered")
st.title("⚾ MLB 정밀 예측 분석 엔진")

# 2. 모델 로드
@st.cache_resource
def load_model():
    if os.path.exists('mlb_model.pkl'):
        return joblib.load('mlb_model.pkl')
    return None

model = load_model()

# 3. 분석 데이터 정의 (팀별 평균 지표)
# 향후 여기에 모든 팀 데이터를 추가하면 됩니다.
team_stats = {
    "LAD": {"launch_angle": 18.5, "bat_speed": 75.2, "release_speed": 92.1, "plate_x": 0.1, "plate_z": 1.6, "spin_axis": 210},
    "SF": {"launch_angle": 16.2, "bat_speed": 72.8, "release_speed": 91.5, "plate_x": -0.2, "plate_z": 1.4, "spin_axis": 190}
}

# 4. 인터페이스
if model is None:
    st.error("⚠️ 모델 파일(mlb_model.pkl)이 없습니다.")
else:
    st.success("✅ 시스템 상태: 정상 (모델 버전 v2.4.1)")
    
    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_date = st.date_input("🗓️ 날짜 선택")
        with col2:
            team_input = st.text_input("팀 이름 입력 (예: LAD, SF)").upper()
        
        submitted = st.form_submit_button("🚀 분석 실행")

    # 5. 분석 로직
    if submitted:
        if team_input in team_stats:
            stats = team_stats[team_input]
            input_df = pd.DataFrame([stats])
            
            # 예측
            prob = model.predict_proba(input_df)[0][1]
            
            st.write("---")
            st.subheader(f"🎯 {team_input} 분석 결과 ({selected_date})")
            st.metric("예상 안타 확률", f"{prob*100:.2f}%")
            
            # 피드백
            if prob > 0.4:
                st.write("🔥 **안타 생산 확률이 매우 높습니다.**")
            else:
                st.write("📉 **범타 가능성이 높습니다.**")
        else:
            st.error(f"데이터에 '{team_input}' 팀이 없습니다. 데이터를 확인하세요.")

st.write("---")
st.caption("통합 관리 시스템 | Predictive Analytics Engine")
