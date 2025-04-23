import os
from shiny import App, ui, reactive
from shinyswatch import theme  # 부트스트랩 테마 모듈 가져오기
from alarm_app.components import footer, header

# 모듈 임포트 - UI 및 서버 컴포넌트
from alarm_app.modules.dashboard import ui as dashboard_ui, server as dashboard_server, load_dashboard_data
from alarm_app.modules.master_data import ui as master_data_ui, server as master_data_server, load_master_data
from alarm_app.modules.data_extraction import ui as data_extraction_ui, server as data_extraction_server, load_extraction_data
from alarm_app.modules.analysis import ui as analysis_ui, server as analysis_server, load_analysis_data
from alarm_app.modules.report_generator import ui as report_generator_ui, server as report_generator_server, load_report_data

# 정적 파일 경로 설정 (절대 경로)
current_dir = os.path.dirname(os.path.abspath(__file__))
www_dir = os.path.join(current_dir, "alarm_app", "www")

# 탭 아이콘 정의
DASHBOARD_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-speedometer2 me-1" viewBox="0 0 16 16">
  <path d="M8 4a.5.5 0 0 1 .5.5V6a.5.5 0 0 1-1 0V4.5A.5.5 0 0 1 8 4zM3.732 5.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707zM2 10a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 10zm9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5zm.754-4.246a.389.389 0 0 0-.527-.02L7.547 9.31a.91.91 0 1 0 1.302 1.258l3.434-4.297a.389.389 0 0 0-.029-.518z"/>
  <path fill-rule="evenodd" d="M0 10a8 8 0 1 1 15.547 2.661c-.442 1.253-1.845 1.602-2.932 1.25C11.309 13.488 9.475 13 8 13c-1.474 0-3.31.488-4.615.911-1.087.352-2.49.003-2.932-1.25A7.988 7.988 0 0 1 0 10zm8-7a7 7 0 0 0-6.603 9.329c.203.575.923.876 1.68.63C4.397 12.533 6.358 12 8 12s3.604.532 4.923.96c.757.245 1.477-.056 1.68-.631A7 7 0 0 0 8 3z"/>
</svg>"""

MASTER_DATA_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-database-gear me-1" viewBox="0 0 16 16">
  <path d="M12.096 6.223A4.92 4.92 0 0 0 13 5.698V7c0 .289-.213.654-.753 1.007a4.493 4.493 0 0 1 1.753.25V4c0-1.007-.875-1.755-1.904-2.223C11.022 1.289 9.573 1 8 1s-3.022.289-4.096.777C2.875 2.245 2 2.993 2 4v9c0 1.007.875 1.755 1.904 2.223C4.978 15.71 6.427 16 8 16c.536 0 1.058-.034 1.555-.097a4.525 4.525 0 0 1-.813-.927C8.5 14.992 8.252 15 8 15c-1.464 0-2.766-.27-3.682-.687C3.356 13.875 3 13.373 3 13v-1.302c.271.202.58.378.904.525C4.978 12.71 6.427 13 8 13h.027a4.552 4.552 0 0 1 0-1H8c-1.464 0-2.766-.27-3.682-.687C3.356 10.875 3 10.373 3 10V8.698c.271.202.58.378.904.525C4.978 9.71 6.427 10 8 10c.262 0 .52-.008.774-.024a4.525 4.525 0 0 1 1.102-1.132C9.298 8.944 8.666 9 8 9c-1.464 0-2.766-.27-3.682-.687C3.356 7.875 3 7.373 3 7V5.698c.271.202.58.378.904.525C4.978 6.711 6.427 7 8 7s3.022-.289 4.096-.777ZM3 4c0-.374.356-.875 1.318-1.313C5.234 2.271 6.536 2 8 2s2.766.27 3.682.687C12.644 3.125 13 3.627 13 4c0 .374-.356.875-1.318 1.313C10.766 5.729 9.464 6 8 6s-2.766-.27-3.682-.687C3.356 4.875 3 4.373 3 4Z"/>
  <path d="M11.886 9.46c.18-.613 1.048-.613 1.229 0l.043.148a.64.64 0 0 0 .921.382l.136-.074c.561-.306 1.175.308.87.869l-.075.136a.64.64 0 0 0 .382.92l.149.045c.612.18.612 1.048 0 1.229l-.15.043a.64.64 0 0 0-.38.921l.074.136c.305.561-.309 1.175-.87.87l-.136-.075a.64.64 0 0 0-.92.382l-.045.149c-.18.612-1.048.612-1.229 0l-.043-.15a.64.64 0 0 0-.921-.38l-.136.074c-.561.305-1.175-.309-.87-.87l.075-.136a.64.64 0 0 0-.382-.92l-.148-.045c-.613-.18-.613-1.048 0-1.229l.148-.043a.64.64 0 0 0 .382-.921l-.074-.136c-.306-.561.308-1.175.869-.87l.136.075a.64.64 0 0 0 .92-.382l.045-.148ZM14 12.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0Z"/>
</svg>"""

DATA_EXTRACTION_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download me-1" viewBox="0 0 16 16">
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
</svg>"""

ANALYSIS_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-graph-up me-1" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M0 0h1v15h15v1H0V0Zm14.817 3.113a.5.5 0 0 1 .07.704l-4.5 5.5a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61 4.15-5.073a.5.5 0 0 1 .704-.07Z"/>
</svg>"""

REPORT_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-text me-1" viewBox="0 0 16 16">
  <path d="M5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zM5 9.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5z"/>
  <path d="M9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.5L9.5 0zm0 1v2A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5z"/>
</svg>"""

# 애플리케이션 UI 정의
app_ui = ui.page_fluid(
    # 헤더 추가
    header.ui,
    
    # 네비게이션 패널
    ui.page_navbar(
        # 기본 페이지
        ui.nav_panel(
            ui.HTML(f"{DASHBOARD_ICON} 대시보드"), 
            dashboard_ui
        ),
        
        # 기준정보 관리 페이지
        ui.nav_panel(
            ui.HTML(f"{MASTER_DATA_ICON} 기준정보관리"),
            master_data_ui
        ),
        
        # 데이터 추출 페이지
        ui.nav_panel(
            ui.HTML(f"{DATA_EXTRACTION_ICON} 데이터 추출"),
            data_extraction_ui
        ),
        
        # 알람 분석 페이지
        ui.nav_panel(
            ui.HTML(f"{ANALYSIS_ICON} 분석"),
            analysis_ui
        ),
        
        # 리포트 생성 페이지
        ui.nav_panel(
            ui.HTML(f"{REPORT_ICON} 리포트 생성"),
            report_generator_ui
        ),
        
        # 애플리케이션 제목
        title="",  # 헤더가 제목을 포함하므로 여기서는 비워둠
        
        # 푸터 설정
        footer=footer.ui
    ),
    
    # 타이머 설정 (1초마다 갱신 - 현재 시간 표시용)
    ui.input_action_button("interval", "", style="display:none;"),
    ui.tags.script("""
    $(function() {
      setInterval(function() { Shiny.setInputValue('interval', Date.now()); }, 1000);
    });
    """),
    
    # 테마 적용
    theme=theme.flatly
)

# 서버 로직 정의
def server(input, output, session):
    # 헤더 서버 로직
    header.server(input, output, session)
    
    # 모듈 서버 로직 연결
    dashboard_server("dashboard")
    master_data_server("master_data")
    data_extraction_server("data_extraction")
    analysis_server("analysis")
    report_generator_server("report_generator")
    
    # 모듈 초기화를 위한 반응형 이벤트
    @reactive.Effect
    def initialize_app():
        try:
            # 각 모듈의 데이터 로드 함수 호출
            load_dashboard_data()
            load_master_data()
            load_extraction_data()
            load_analysis_data()
            load_report_data()
        except Exception:
            pass

# Shiny 앱 생성 (정적 파일 디렉토리 지정 - 절대 경로 사용)
app = App(app_ui, server, static_assets=www_dir)

# 직접 실행 시 앱 구동
if __name__ == "__main__":
    app.run()

