import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list, on_card_click):
        st.markdown("""
            <style>
                /* 투명 버튼 처리: 카드 전체를 클릭 가능하게 함 */
                div[data-testid="stButton"] button {
                    background: transparent !important;
                    border: none !important;
                    padding: 0 !important;
                    width: 100% !important;
                    height: 180px !important;
                    position: absolute !important;
                    z-index: 10 !important;
                }
                .custom-card { width: 100% !important; height: 180px !important; border: 2px solid #d9ded5 !important; border-radius: 12px !important; background-color: #fcfcf8; display: flex !important; flex-direction: column !important; justify-content: space-around !important; align-items: center !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important; padding: 10px 0 !important; }
                .card-wrapper { position: relative; padding: 5px; }
                .text-row { display: flex !important; justify-content: center !important; align-items: center !important; width: 100% !important; height: 30px !important; text-align: center !important; }
                .text-date { font-size: 12px !important; color: #697465 !important; font-weight: 500; }
                .text-team { font-weight: 800 !important; font-size: 14px !important; color: #111827; }
                .text-score { font-weight: 900 !important; font-size: 18px !important; color: #fe7701; }
            </style>
        """, unsafe_allow_html=True)

        # ... (상단 버튼 및 페이지네이션 로직은 동일) ...
        
        card_cols = st.columns(6)
        # ... (생략) ...
        
        for i, col in enumerate(card_cols):
            with col:
                if i < len(page_games):
                    game = page_games[i]
                    # 카드Wrapper 안에 투명 버튼 삽입
                    st.markdown('<div class="card-wrapper">', unsafe_allow_html=True)
                    if st.button(" ", key=f"click_{i}"):
                        on_card_click(game)
                    st.markdown(f"""
                        <div class="custom-card">
                            <div class="text-row text-date">{game.get('display_date', '')} {game.get('display_time', '')}</div>
                            <div class="text-row text-team">{game.get('away_name', 'AWY')}</div>
                            <div class="text-row text-score">{game.get('away_score', 0)} : {game.get('home_score', 0)}</div>
                            <div class="text-row text-team">{game.get('home_name', 'HOM')}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
