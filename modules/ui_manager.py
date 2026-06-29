# ... (앞부분 동일)
# UI 출력 부분만 아래처럼 수정
                    # app.py에서 계산한 시간 사용
                    date_val = game.get('display_date', '확인중')
                    time_val = game.get('display_time', '확인중')
                    
                    st.markdown(f"""
                        <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:10px; padding:10px; text-align:center; height:180px;">
                            <div style="font-size:12px; font-weight:bold; color:#4b5563;">{date_val}</div>
                            <div style="font-size:14px; font-weight:bold; color:#dc2626; margin-bottom:10px;">{time_val}</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('away_name', 'AWAY')}: {game.get('away_score', 0)}</div>
                            <div style="font-size:13px; font-weight:bold;">{game.get('home_name', 'HOME')}: {game.get('home_score', 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)
# ...
