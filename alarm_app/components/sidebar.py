from shiny import ui, reactive

# 사이드바 UI 정의
ui = ui.div(
    ui.card(
        ui.card_header("필터 옵션"),
        ui.div(
            ui.h4("기간 설정"),
            ui.input_date_range("date_range", "조회 기간", start="2023-01-01", end="2023-12-31"),
            ui.hr(),
            ui.h4("알람 설정"),
            ui.input_selectize(
                "alarm_severity", 
                "심각도", 
                choices=["높음", "중간", "낮음"], 
                multiple=True,
                selected=["높음", "중간", "낮음"]
            ),
            ui.input_selectize(
                "alarm_status", 
                "상태", 
                choices=["활성", "인지됨", "해결됨"], 
                multiple=True,
                selected=["활성", "인지됨", "해결됨"]
            ),
            ui.hr(),
            ui.h4("설비 설정"),
            ui.input_selectize(
                "equipment", 
                "설비", 
                choices=["설비 A", "설비 B", "설비 C", "설비 D"], 
                multiple=True
            ),
            ui.hr(),
            ui.div(
                ui.input_action_button("apply_filter", "필터 적용", class_="btn-primary"),
                ui.input_action_button("reset_filter", "초기화", class_="btn-outline-secondary ms-2"),
                style="display: flex; justify-content: space-between; margin-top: 20px;"
            ),
            style="padding: 15px;"
        ),
        style="width: 100%; max-width: 300px;"
    ),
    style="padding: 15px; border-right: 1px solid #ddd; background-color: #f8f9fa;"
)

# 사이드바 서버 로직
def server(input, output, session):
    # 필터 초기화 이벤트 처리
    @reactive.Effect
    @reactive.event(input.reset_filter)
    def _():
        from datetime import date, timedelta
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        # 필터 초기화
        ui.update_date_range("date_range", start=start_date.isoformat(), end=end_date.isoformat())
        ui.update_selectize("alarm_severity", selected=["높음", "중간", "낮음"])
        ui.update_selectize("alarm_status", selected=["활성", "인지됨", "해결됨"])
        ui.update_selectize("equipment", selected=[]) 