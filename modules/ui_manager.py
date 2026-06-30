# [파일: ui_manager.py]
class UIManager:
    def get_input(self):
        print("\n=== ⚾ 야구 경기 분석기 ===")
        home_team = input("홈 팀 이름을 입력하세요: ")
        away_team = input("원정 팀 이름을 입력하세요: ")
        return {"home": home_team, "away": away_team}

    def display_briefing(self, result):
        print("\n--- 📋 분석 결과 브리핑 ---")
        print(f"승리 예측 확률: {result.get('win_prob', '데이터 없음')}%")
        print(f"핵심 변수: {result.get('key_factor', '없음')}")
        print("--------------------------\n")
