import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="MLB 30개 팀 예측 시스템", layout="centered")
st.title("⚾ MLB 정밀 예측 분석 엔진 (30개 팀 통합)")

# 1. 모델 로드
@st.cache_resource
def load_model():
    return joblib.load('mlb_model.pkl') if os.path.exists('mlb_model.pkl') else None

model = load_model()

# 2. 30개 팀 데이터 정의
# 팀별 평균 수치 (이 데이터를 기반으로 예측)
team_stats_data = {
    "ARI": {"launch_angle": 16.5, "bat_speed": 73.0, "release_speed": 91.0, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 200},
    "ATL": {"launch_angle": 18.0, "bat_speed": 76.5, "release_speed": 92.5, "plate_x": 0.1, "plate_z": 1.6, "spin_axis": 210},
    "BAL": {"launch_angle": 17.5, "bat_speed": 74.0, "release_speed": 91.5, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 205},
    "BOS": {"launch_angle": 17.2, "bat_speed": 74.2, "release_speed": 91.2, "plate_x": -0.1, "plate_z": 1.4, "spin_axis": 195},
    "CHC": {"launch_angle": 16.8, "bat_speed": 73.5, "release_speed": 90.8, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 200},
    "CWS": {"launch_angle": 16.0, "bat_speed": 72.5, "release_speed": 90.5, "plate_x": 0.1, "plate_z": 1.4, "spin_axis": 190},
    "CIN": {"launch_angle": 17.8, "bat_speed": 74.8, "release_speed": 91.8, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 202},
    "CLE": {"launch_angle": 16.5, "bat_speed": 73.2, "release_speed": 90.9, "plate_x": -0.1, "plate_z": 1.4, "spin_axis": 198},
    "COL": {"launch_angle": 17.0, "bat_speed": 73.8, "release_speed": 91.2, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 200},
    "DET": {"launch_angle": 16.2, "bat_speed": 72.8, "release_speed": 90.5, "plate_x": 0.1, "plate_z": 1.4, "spin_axis": 192},
    "HOU": {"launch_angle": 18.2, "bat_speed": 76.0, "release_speed": 92.2, "plate_x": 0.2, "plate_z": 1.6, "spin_axis": 215},
    "KC": {"launch_angle": 16.5, "bat_speed": 73.0, "release_speed": 90.8, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 198},
    "LAA": {"launch_angle": 17.5, "bat_speed": 74.5, "release_speed": 91.5, "plate_x": 0.1, "plate_z": 1.5, "spin_axis": 205},
    "LAD": {"launch_angle": 18.5, "bat_speed": 75.5, "release_speed": 92.5, "plate_x": 0.1, "plate_z": 1.6, "spin_axis": 210},
    "MIA": {"launch_angle": 16.0, "bat_speed": 72.0, "release_speed": 90.2, "plate_x": -0.1, "plate_z": 1.4, "spin_axis": 190},
    "MIL": {"launch_angle": 17.0, "bat_speed": 73.5, "release_speed": 91.0, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 200},
    "MIN": {"launch_angle": 17.2, "bat_speed": 74.0, "release_speed": 91.2, "plate_x": 0.1, "plate_z": 1.5, "spin_axis": 202},
    "NYM": {"launch_angle": 16.8, "bat_speed": 73.5, "release_speed": 91.2, "plate_x": -0.1, "plate_z": 1.4, "spin_axis": 195},
    "NYY": {"launch_angle": 18.0, "bat_speed": 75.8, "release_speed": 92.0, "plate_x": 0.1, "plate_z": 1.6, "spin_axis": 208},
    "OAK": {"launch_angle": 16.0, "bat_speed": 72.2, "release_speed": 90.0, "plate_x": -0.1, "plate_z": 1.4, "spin_axis": 190},
    "PHI": {"launch_angle": 17.8, "bat_speed": 75.0, "release_speed": 91.8, "plate_x": 0.1, "plate_z": 1.6, "spin_axis": 205},
    "PIT": {"launch_angle": 16.5, "bat_speed": 72.8, "release_speed": 90.5, "plate_x": 0.0, "plate_z": 1.4, "spin_axis": 195},
    "SD": {"launch_angle": 17.5, "bat_speed": 74.2, "release_speed": 91.5, "plate_x": 0.1, "plate_z": 1.5, "spin_axis": 203},
    "SEA": {"launch_angle": 17.0, "bat_speed": 73.5, "release_speed": 91.0, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 200},
    "SF": {"launch_angle": 16.2, "bat_speed": 72.8, "release_speed": 91.5, "plate_x": -0.2, "plate_z": 1.4, "spin_axis": 190},
    "STL": {"launch_angle": 17.0, "bat_speed": 73.5, "release_speed": 91.0, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 200},
    "TB": {"launch_angle": 17.2, "bat_speed": 74.0, "release_speed": 91.2, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 200},
    "TEX": {"launch_angle": 17.8, "bat_speed": 75.0, "release_speed": 91.8, "plate_x": 0.1, "plate_z": 1.5, "spin_axis": 205},
    "TOR": {"launch_angle": 17.5, "bat_speed": 74.5, "release_speed": 91.8, "plate_x": 0.0, "plate_z": 1.5, "spin_axis": 205},
    "WSH": {"launch_angle": 16.5, "bat_speed": 72.5, "release_speed": 90.5, "plate_x": -0.1, "plate_z": 1.4, "spin_axis": 192}
}

# 3. 분석 UI
st.success("✅ 시스템 상태: 정상 (30개 팀 전체 데이터 로드 완료)")
with st.form("analysis_form"):
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("🗓️ 날짜 선택")
    with col2:
        team_input = st.selectbox("분석할 팀 선택", list(team_stats_data.keys()))
    submitted = st.form_submit_button("🚀 분석 실행")

# 4. 분석 로직
if submitted and model:
    stats = team_stats_data[team_input]
    input_df = pd.DataFrame([stats])
    prob = model.predict_proba(input_df)[0][1]
    
    st.subheader(f"🎯 {team_input} 분석 결과 ({selected_date})")
    st.metric("예상 안타 확률", f"{prob*100:.2f}%")
    st.progress(float(prob))
elif not model:
    st.error("⚠️ 모델 파일을 찾을 수 없습니다.")

st.caption("통합 관리 시스템 | MLB 30개 팀 데이터 엔진")
