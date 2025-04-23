"""
최소화된 테스트 Shiny 앱 - 데이터프레임 표시 테스트
"""
from shiny import App, ui, render
import pandas as pd

# 앱 UI 정의 - 매우 간단한 구조
app_ui = ui.page_fluid(
    ui.h1("간단한 데이터 테스트"),
    ui.hr(),
    
    # 기본 테이블 출력
    ui.h3("기본 테이블"),
    ui.output_table("basic_table"),
    
    # 데이터프레임 출력
    ui.h3("데이터프레임"),
    ui.output_data_frame("test_df"),
    
    # 정보 메시지
    ui.output_text("info_text")
)

# 서버 로직 정의
def server(input, output, session):
    # 기본 테이블 출력
    @output
    @render.table
    def basic_table():
        print("basic_table 렌더링 호출")
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': ['가', '나', '다', '라', '마'],
            'C': [True, False, True, False, True]
        }
        return pd.DataFrame(data)
    
    # 데이터프레임 렌더링
    @output
    @render.data_frame
    def test_df():
        print("test_df 렌더링 호출")
        data = {
            'ID': [1, 2, 3, 4, 5],
            '설비명': ['설비1', '설비2', '설비3', '설비4', '설비5'],
            '공정': ['P1', 'P2', 'P1', 'P3', 'P2'],
            '룸': ['R1', 'R2', 'R3', 'R1', 'R2']
        }
        df = pd.DataFrame(data)
        print(f"테스트 데이터 생성: {len(df)}행")
        return df
    
    # 정보 메시지
    @output
    @render.text
    def info_text():
        return "총 5개 데이터 표시 중"

# 앱 생성 및 실행
app = App(app_ui, server)

if __name__ == "__main__":
    app.run(debug=True) 