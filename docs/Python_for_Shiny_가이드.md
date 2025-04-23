# Python for Shiny 가이드

## 개요
Python for Shiny는 파이썬을 사용하여 반응형 웹 애플리케이션을 만들 수 있는 프레임워크입니다. 원래 R 언어를 위해 개발된 Shiny가 파이썬으로 포팅된 버전으로, 데이터 시각화 및 대시보드 구축에 적합합니다.

## Shiny 문법 - Core vs Express

Python for Shiny는 두 가지 문법 스타일을 제공합니다:

### Core 문법 (우리 프로젝트 사용)
- 더 세밀한 제어가 가능한 객체 지향적 접근방식
- 복잡한 애플리케이션 구축에 적합
- 명시적인 UI 구성과 서버 로직 분리
- 모듈화 및 확장에 용이

### Express 문법
- 간결하고 직관적인 데코레이터 기반 접근방식
- 간단한 애플리케이션 빠르게 구축 가능
- Python 데코레이터를 활용한 간소화된 구문
- 작은 규모의 앱에 적합

**Note**: 우리 프로젝트는 확장성과 유지보수성을 고려하여 **Core 문법**을 사용합니다.

## 주요 특징

### 반응형(Reactive)
- 수동 상태 관리가 필요 없음
- 콜백 함수와 상태 변수 대신 자동으로 최적의 실행 경로 결정
- 개발자는 인사이트 전달에 집중할 수 있음

### 효율적(Efficient)
- 반응형 실행 엔진을 사용하여 애플리케이션 재렌더링 최소화
- 출력은 필요할 때만 렌더링되며 업스트림 컴포넌트가 변경될 때만 업데이트
- 간단한 대시보드부터 복잡한 웹 앱까지 지원 가능

### 견고함(Robust)
- 현대적인 파이썬 웹 스택(Starlette, asyncio)을 기반으로 구축
- CSS 및 JavaScript 커스터마이징 완벽 지원
- 풍부하고 인터랙티브한 사용자 경험 제공

## 설치 및 시작하기

1. 설치:
```bash
pip install shiny
```

2. 템플릿 생성:
```bash
shiny create --template dashboard-tips
```

3. 자신의 데이터로 수정하고 레이아웃 커스터마이징

## Shiny 애플리케이션 구조

### 1. UI 구성요소
- **Inputs**: 사용자로부터 입력 받는 요소 (슬라이더, 드롭다운, 체크박스 등)
- **Outputs**: 결과 표시 요소 (플롯, 테이블, 텍스트 등)
- **Layouts**: UI 배치 방법 (사이드바, 탭, 패널 등)

### 2. 서버 로직
- 입력값 처리
- 데이터 분석 및 가공
- 출력 생성

### 3. 반응성(Reactivity)
- **반응형 값(Reactive Values)**: 변경 가능한 상태 저장
- **반응형 계산(Reactive Calculations)**: 입력에 따라 계산 결과 업데이트
- **반응형 효과(Reactive Effects)**: 부수 효과 처리

## 아이콘 사용 가이드

Python for Shiny는 [Bootstrap 아이콘](https://icons.getbootstrap.com/)과 [Font Awesome](https://fontawesome.com/) 아이콘을 지원합니다.

### 아이콘 사용법

```python
# Bootstrap 아이콘 사용
ui.tags.i(class_="bi bi-alarm")

# Font Awesome 아이콘 사용
ui.tags.i(class_="fa fa-chart-bar")

# 텍스트와 함께 아이콘 사용
ui.div(
    ui.tags.i(class_="bi bi-bell"), 
    "알람 알림",
    class_="d-flex align-items-center"
)

# 버튼에 아이콘 추가
ui.input_action_button(
    "refresh_btn", 
    ui.div(ui.tags.i(class_="bi bi-arrow-clockwise"), "새로고침", class_="d-flex align-items-center gap-1")
)
```

### 프로젝트 아이콘 표준

일관성을 위해 프로젝트에서는 다음 아이콘을 표준으로 사용합니다:

| 기능 | 아이콘 | 클래스 |
|------|--------|--------|
| 새로고침 | ![refresh](https://icons.getbootstrap.com/assets/icons/arrow-clockwise.svg) | `bi bi-arrow-clockwise` |
| 추가 | ![add](https://icons.getbootstrap.com/assets/icons/plus-circle.svg) | `bi bi-plus-circle` |
| 삭제 | ![delete](https://icons.getbootstrap.com/assets/icons/trash.svg) | `bi bi-trash` |
| 편집 | ![edit](https://icons.getbootstrap.com/assets/icons/pencil-square.svg) | `bi bi-pencil-square` |
| 알람 | ![alarm](https://icons.getbootstrap.com/assets/icons/bell.svg) | `bi bi-bell` |
| 다운로드 | ![download](https://icons.getbootstrap.com/assets/icons/download.svg) | `bi bi-download` |
| 차트 | ![chart](https://icons.getbootstrap.com/assets/icons/bar-chart.svg) | `bi bi-bar-chart` |
| 설정 | ![settings](https://icons.getbootstrap.com/assets/icons/gear.svg) | `bi bi-gear` |

## 멀티 페이지 네비게이션 구조

### 네비게이션 바(Navigation Bar) 기반 구조

Python for Shiny는 `ui.page_navbar`를 통해 직관적인 멀티 페이지 애플리케이션을 구성할 수 있습니다. 이는 복잡한 애플리케이션을 기능별로 분리하여 사용자 경험을 향상시키는 데 적합합니다.

```python
from shiny import App, ui, render

app_ui = ui.page_navbar(
    # 애플리케이션 제목
    title="알람 분석 애플리케이션",
    
    # 대시보드 페이지
    ui.nav_panel("대시보드", 
        ui.layout_sidebar(
            ui.sidebar(
                ui.h4("필터"),
                ui.input_date_range("date_range", "기간 선택"),
                ui.input_selectize("alarm_type", "알람 유형", ["유형1", "유형2", "유형3"], multiple=True),
                ui.hr(),
                ui.input_action_button("refresh", "새로고침", class_="btn-primary")
            ),
            # 메인 컨텐츠 영역 - 직접 카드 사용
            ui.card(
                ui.card_header("알람 추이"),
                ui.output_plot("trend_plot")
            ),
            ui.card(
                ui.card_header("알람 목록"),
                ui.output_table("alarm_table")
            )
        )
    ),
    
    # 알람 관리 페이지
    ui.nav_panel("알람 관리",
        ui.layout_sidebar(
            ui.sidebar(
                ui.h4("알람 필터"),
                ui.input_text("alarm_code_filter", "알람 코드"),
                ui.input_select("severity_filter", "심각도", 
                               choices=["전체", "HIGH", "MEDIUM", "LOW"]),
                ui.hr(),
                ui.input_action_button("add_alarm", "알람 추가", class_="btn-success")
            ),
            # 메인 컨텐츠 영역 - 직접 카드 사용
            ui.card(
                ui.card_header("알람 마스터 데이터"),
                ui.output_data_frame("alarm_master_table")
            )
        )
    ),
    
    # 데이터 추출 페이지
    ui.nav_panel("데이터 추출",
        ui.layout_sidebar(
            ui.sidebar(
                ui.h4("파일 업로드"),
                ui.input_file("upload", "로그 파일 선택", multiple=True),
                ui.hr(),
                ui.input_action_button("extract", "데이터 추출", class_="btn-primary")
            ),
            # 메인 컨텐츠 영역 - 직접 카드 사용
            ui.card(
                ui.card_header("추출 결과"),
                ui.output_ui("extraction_result")
            )
        )
    ),
    
    # 분석 페이지
    ui.nav_panel("분석",
        ui.navset_tab(
            ui.nav("시간별 분석", 
                ui.card(
                    ui.card_header("시간별 알람 패턴"),
                    ui.output_plot("time_analysis_plot")
                )
            ),
            ui.nav("설비별 분석", 
                ui.card(
                    ui.card_header("설비별 알람 분포"),
                    ui.output_plot("equipment_analysis_plot")
                )
            ),
            ui.nav("유형별 분석", 
                ui.card(
                    ui.card_header("알람 유형별 분포"),
                    ui.output_plot("type_analysis_plot")
                )
            )
        )
    ),
    
    # 리포트 생성 페이지
    ui.nav_panel("리포트 생성",
        ui.layout_sidebar(
            ui.sidebar(
                ui.h4("리포트 설정"),
                ui.input_date_range("report_date_range", "기간 선택"),
                ui.input_select("report_type", "리포트 유형", 
                               choices=["일별 요약", "설비별 요약", "알람 유형별 요약"]),
                ui.hr(),
                ui.input_action_button("generate_report", "리포트 생성", class_="btn-success")
            ),
            # 메인 컨텐츠 영역 - 직접 카드 사용
            ui.card(
                ui.card_header("리포트 미리보기"),
                ui.output_ui("report_preview")
            )
        )
    ),
    
    # 기타 설정
    footer=ui.div(
        "© 2023 알람 분석 애플리케이션",
        style="text-align: center; padding: 10px;"
    )
)

def server(input, output, session):
    # 서버 로직 구현
    # ...

app = App(app_ui, server)
```

### 모듈화된 멀티 페이지 구현

대규모 애플리케이션의 경우, 각 페이지를 별도의 모듈로 구현하여 코드 유지보수성을 높일 수 있습니다:

```python
# app/modules/dashboard/ui.py
from shiny import ui

# 대시보드 UI 정의
ui = ui.layout_sidebar(
    ui.sidebar(
        ui.h4("필터"),
        ui.input_date_range("date_range", "기간 선택"),
        ui.input_selectize("alarm_type", "알람 유형", ["유형1", "유형2", "유형3"], multiple=True),
        ui.hr(),
        ui.input_action_button("refresh", "새로고침", class_="btn-primary")
    ),
    # 메인 컨텐츠 영역 - 직접 카드 사용
    ui.card(
        ui.card_header("알람 추이"),
        ui.output_plot("trend_plot")
    ),
    ui.card(
        ui.card_header("알람 목록"),
        ui.output_table("alarm_table")
    )
)

# app.py
from shiny import App, ui
from app.modules.dashboard.ui import dashboard_ui
from app.modules.alarm_management.ui import alarm_management_ui
# ... 다른 모듈 임포트

app_ui = ui.page_navbar(
    title="알람 분석 애플리케이션",
    ui.nav_panel("대시보드", dashboard_ui),
    ui.nav_panel("알람 관리", alarm_management_ui),
    # ... 다른 페이지
    footer=ui.div(
        "© 2023 알람 분석 애플리케이션",
        style="text-align: center; padding: 10px;"
    )
)
```

### 카드(Card) 컴포넌트 활용

Shiny의 카드 컴포넌트는 대시보드 구성에 매우 유용하며, 정보를 구조화된 방식으로 표현할 수 있습니다:

```python
ui.card(
    ui.card_header("알람 요약 통계"),
    ui.div(
        ui.row(
            ui.column(3, ui.value_box("total_alarms", "총 알람 수", theme="primary")),
            ui.column(3, ui.value_box("active_alarms", "활성 알람 수", theme="danger")),
            ui.column(3, ui.value_box("resolved_alarms", "해결된 알람 수", theme="success")),
            ui.column(3, ui.value_box("avg_resolution_time", "평균 해결 시간", theme="info"))
        ),
        class_="p-3"
    ),
    full_screen=True
)
```

## 우리 프로젝트에 적용 방안

### 1. 멀티 페이지 구조 구현
```python
from shiny import App, ui, render

app_ui = ui.page_navbar(
    title="알람 분석 애플리케이션",
    ui.nav_panel("대시보드", dashboard_ui),
    ui.nav_panel("알람 관리", alarm_management_ui),
    ui.nav_panel("데이터 추출", data_extraction_ui),
    ui.nav_panel("분석", analysis_ui),
    ui.nav_panel("리포트 생성", report_generator_ui)
)

def server(input, output, session):
    # 각 모듈의 서버 로직 통합
    dashboard_server(input, output, session)
    alarm_management_server(input, output, session)
    data_extraction_server(input, output, session)
    analysis_server(input, output, session)
    report_generator_server(input, output, session)

app = App(app_ui, server)
```

## 참고 자료
- 공식 웹사이트: [https://shiny.posit.co/py/](https://shiny.posit.co/py/)
- 튜토리얼: [https://shiny.posit.co/py/docs/overview.html](https://shiny.posit.co/py/docs/overview.html)
- 갤러리: [https://shiny.posit.co/py/gallery/](https://shiny.posit.co/py/gallery/) 