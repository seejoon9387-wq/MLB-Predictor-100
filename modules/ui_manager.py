import streamlit as st

class UIManager:
    @staticmethod
    def render_game_navbar(game_data_list):
        # ... (상단 이전/다음 버튼 로직은 동일) ...
        
        start = st.session_state.get('current_page', 0) * 6
        end = min(start + 6, len(game_data_list))
        page_games = game_data_list[start:end]

        cols = st.columns(6)
        for i in range(6):
            with cols[i]:
                if i < len(page_games):
                    game = page_games[i]
                    # 버튼 클릭 시 session_state에 선택된 game_id 저장
                    if st.button(f"상세보기", key=f"btn_{game['game_id']}"):
                        st.session_state.selected_game_id = game['game_id']
                        st.rerun()
                    
                    # (카드 디자인 영역은 이전과 동일하게 유지)
                    st.markdown(f"""... (카드 디자인 코드) ...""")
