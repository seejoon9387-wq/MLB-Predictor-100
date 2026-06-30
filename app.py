import streamlit as st
import joblib
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="MLB 예측 엔진", layout="centered")
st.title("🛡️ MLB 정밀 예측 분석 엔진")
st.subheader("모델 버전: v2.4.1 (모델 단독 운용 모드)")

# 2. 모델 로드 (파일이 없으면 바로 알려줌)
@st.cache_resource
def load_model():
    if os.path.exists('mlb_model.pkl'):
        return joblib.load('mlb_model.pkl')
    else:
        return None

model = load_model()

# 3. 메인 인터페이스
if model is None:
    st.error("⚠️ 모델 파일('mlb_model.pkl')을 찾을 수 없습니다. 깃허브 폴더를 확인하세요.")
else:
    st.success("✅ 엔진 가동 중: 실시간 분석 가능")
    
    with st.form("input_form"):
        st.write("### ⚾ 타구 및 투구 데이터 입력")
        col1, col2 = st.columns(2)
        
        with col1:
            launch_angle = st.number_input("발사 각도 (Launch Angle)", value=15.0)
            bat_speed = st.number_input("타구 속도 (Bat Speed)", value=70.0)
            release_speed = st.number_input("투구 속도 (Release Speed)", value=90.0)
        
        with col2:
            plate_x = st.number_input("투구 위치 X (Plate X)", value=0.0)
            plate_z = st.number_input("투구 위치 Z (Plate Z)", value=1.5)
            spin_axis = st.number_input("회전 축 (Spin Axis)", value=200.0)
            
        submitted = st.form_submit_button("🚀 안타 확률 분석 실행")

    # 4. 분석 로직
    if submitted:
        input_df = pd.DataFrame([[launch_angle, bat_speed, release_speed, plate_x, plate_z, spin_axis]], 
                                columns=['launch_angle', 'bat_speed', 'release_speed', 'plate_x', 'plate_z', 'spin_axis'])
        
        # 확률 계산
        prob = model.predict_proba(input_df)[0][1]
        
        # 결과 표시
        st.write("---")
        st.subheader("🎯 분석 결과")
        st.metric(label="예상 안타 확률", value=f"{prob*100:.2f}%")
        
        # 시각화 효과
        st.progress(float(prob))
        
        if prob > 0.4:
            st.balloons()
            st.write("🔥 **강력한 안타성 타구입니다!**")
        elif prob > 0.2:
            st.write("🧐 **평범한 타구로 예상됩니다.**")
        else:
            st.write("📉 **범타 가능성이 높습니다.**")

# 시스템 상태 하단 바
st.write("---")
st.caption("시스템 상태: 정상 | 데이터 엔진: 모델 전용 모드")
