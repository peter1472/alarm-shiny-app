from shiny import ui, reactive, render, req

# 인라인 SVG 로고 정의 - 알람과 데이터 분석을 결합한 디자인
LOGO_SVG = """
<svg width="80" height="80" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
  <!-- 배경 원 -->
  <circle cx="20" cy="20" r="19" fill="#ffffff" stroke="#3498db" stroke-width="1.5" />
  
  <!-- 그래프/차트 막대 -->
  <rect x="8" y="25" width="4" height="6" fill="#3498db" rx="1" />
  <rect x="14" y="20" width="4" height="11" fill="#3498db" rx="1" />
  <rect x="20" y="22" width="4" height="9" fill="#3498db" rx="1" />
  <rect x="26" y="16" width="4" height="15" fill="#3498db" rx="1" />
  
  <!-- 알람 아이콘 -->
  <circle cx="20" cy="10" r="5" fill="#e74c3c" />
  <rect x="18" y="9" width="4" height="2" fill="#ffffff" />
  <rect x="18" y="12" width="4" height="2" fill="#ffffff" />
  
  <!-- 실시간 신호 파형 -->
  <path d="M5,15 L8,15 L10,12 L14,18 L16,15 L19,15 L22,13 L26,17 L29,15 L32,15" 
        fill="none" stroke="#2ecc71" stroke-width="1.5" />
</svg>
"""

# 다크모드 토글 아이콘
LIGHT_MODE_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
  <path d="M8 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
</svg>
"""

DARK_MODE_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
  <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278z"/>
</svg>
"""

# 헤더 UI 정의
ui = ui.div(
    ui.tags.head(
        ui.tags.style("""
            .theme-toggle-btn {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                padding: 0;
                margin-left: 10px;
            }
            .theme-toggle-btn svg {
                margin: 0;
                padding: 0;
            }
        """)
    ),
    ui.div(
        ui.div(
            ui.HTML(LOGO_SVG),
            class_="d-flex align-items-center me-3"
        ),
        ui.h1("알람 분석 애플리케이션", class_="my-0 flex-grow-1 fs-2"),
        ui.div(
            ui.div(
                ui.output_text("current_time"),
                class_="me-3"
            ),
            ui.input_action_button(
                "toggle_theme", 
                label="",
                class_="btn btn-outline-light theme-toggle-btn"
            ),
            ui.HTML("""
                <div id="theme_icon_container">
                    <span id="dark_icon" style="display:none;">""" + DARK_MODE_ICON + """</span>
                    <span id="light_icon" style="display:none;">""" + LIGHT_MODE_ICON + """</span>
                </div>
            """),
            class_="d-flex align-items-center"
        ),
        class_="d-flex justify-content-between align-items-center p-3 bg-info text-white"
    ),
    
    # 테마 토글 스크립트
    ui.tags.script("""
    $(document).ready(function() {
        // 다크모드 상태 로컬 스토리지에서 불러오기
        var darkMode = localStorage.getItem('darkMode') === 'true';
        
        // 테마 적용 함수
        function applyTheme(dark) {
            if (dark) {
                $('html').attr('data-bs-theme', 'dark');
                $('#dark_icon').show();
                $('#light_icon').hide();
                $('#toggle_theme').html($('#light_icon').html());
            } else {
                $('html').attr('data-bs-theme', 'light');
                $('#dark_icon').hide();
                $('#light_icon').show();
                $('#toggle_theme').html($('#dark_icon').html());
            }
            localStorage.setItem('darkMode', dark);
        }
        
        // 초기 테마 적용
        applyTheme(darkMode);
        
        // 테마 토글 버튼 이벤트
        $(document).on('click', '#toggle_theme', function() {
            darkMode = !darkMode;
            applyTheme(darkMode);
        });
    });
    """)
)

# 헤더 서버 로직
def server(input, output, session):
    # 현재 시간 표시
    @render.text
    @reactive.event(input.interval)
    def current_time():
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"현재 시간: {current_time}"
    
    # 출력 함수 등록
    output.current_time = current_time 