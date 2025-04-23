# Shiny 시각화 가이드

## 개요
Python for Shiny는 다양한 시각화 라이브러리와 통합하여 인터랙티브한 데이터 시각화를 쉽게 구현할 수 있습니다. 본 가이드에서는 알람 데이터 분석 애플리케이션에 적합한 시각화 방법을 소개합니다.

## 지원 시각화 라이브러리

Python for Shiny는 다음과 같은, 파이썬에서 널리 사용되는 시각화 라이브러리들과 통합됩니다:

1. **Matplotlib**: 기본적인 시각화
2. **Plotly**: 인터랙티브 시각화
3. **Altair**: 선언적 시각화
4. **Bokeh**: 인터랙티브 웹 시각화
5. **seaborn**: 통계 시각화
6. **plotnine**: ggplot2 스타일 시각화

## 주요 시각화 유형 및 예제

### 1. 시계열 차트 (알람 발생 추이)

```python
from shiny import App, ui, render
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def get_connection():
    return sqlite3.connect('alarms.db')

app_ui = ui.page_fluid(
    ui.h1("알람 발생 추이"),
    ui.input_date_range("date_range", "날짜 범위 선택:"),
    ui.output_plot("time_series_plot")
)

def server(input, output, session):
    @render.plot
    def time_series_plot():
        conn = get_connection()
        query = """
        SELECT 
            DATE(timestamp) as date, 
            COUNT(*) as count 
        FROM alarm_events 
        GROUP BY DATE(timestamp)
        ORDER BY date
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['count'], marker='o', linestyle='-')
        plt.title('일별 알람 발생 건수')
        plt.xlabel('날짜')
        plt.ylabel('알람 수')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt
```

### 2. 파이 차트 (알람 유형별 분포)

```python
from shiny import App, ui, render
import pandas as pd
import plotly.express as px
import sqlite3

def get_connection():
    return sqlite3.connect('alarms.db')

app_ui = ui.page_fluid(
    ui.h1("알람 유형별 분포"),
    ui.output_plot("pie_chart")
)

def server(input, output, session):
    @render.plot
    def pie_chart():
        conn = get_connection()
        query = """
        SELECT 
            a.alarm_name, 
            COUNT(*) as count 
        FROM alarm_events e
        JOIN alarm_master a ON e.alarm_code = a.alarm_code
        GROUP BY a.alarm_name
        ORDER BY count DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        fig = px.pie(df, values='count', names='alarm_name', 
                     title='알람 유형별 분포')
        return fig
```

### 3. 히트맵 (시간대별/요일별 알람 발생 패턴)

```python
from shiny import App, ui, render
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect('alarms.db')

app_ui = ui.page_fluid(
    ui.h1("시간대별/요일별 알람 발생 패턴"),
    ui.output_plot("heatmap")
)

def server(input, output, session):
    @render.plot
    def heatmap():
        conn = get_connection()
        query = "SELECT timestamp FROM alarm_events"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # 타임스탬프 변환
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['weekday'] = df['timestamp'].dt.day_name()
        
        # 요일별/시간별 집계
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = pd.crosstab(df['weekday'], df['hour'])
        heatmap_data = heatmap_data.reindex(weekday_order)
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='d')
        plt.title('시간대별/요일별 알람 발생 패턴')
        plt.xlabel('시간 (Hour)')
        plt.ylabel('요일')
        plt.tight_layout()
        return plt
```

### 4. 바 차트 (설비별 알람 발생 빈도)

```python
from shiny import App, ui, render
import pandas as pd
import plotly.express as px
import sqlite3

def get_connection():
    return sqlite3.connect('alarms.db')

app_ui = ui.page_fluid(
    ui.h1("설비별 알람 발생 빈도"),
    ui.input_select("n_equipments", "표시할 설비 수:",
                   choices=[5, 10, 15, 20], selected=10),
    ui.output_plot("bar_chart")
)

def server(input, output, session):
    @render.plot
    def bar_chart():
        conn = get_connection()
        query = """
        SELECT 
            e.equipment_name, 
            COUNT(*) as count 
        FROM alarm_events a
        JOIN equipment_master e ON a.equipment_id = e.equipment_id
        GROUP BY e.equipment_name
        ORDER BY count DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # 상위 N개 설비만 선택
        top_n = int(input.n_equipments())
        df = df.head(top_n)
        
        fig = px.bar(df, x='equipment_name', y='count', 
                     title=f'상위 {top_n}개 설비별 알람 발생 빈도')
        fig.update_xaxes(title='설비명')
        fig.update_yaxes(title='알람 수')
        return fig
```

### 5. 대시보드 구성 예시

```python
from shiny import App, ui, render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

def get_connection():
    return sqlite3.connect('alarms.db')

app_ui = ui.page_fluid(
    ui.h1("알람 모니터링 대시보드"),
    
    # 필터 영역
    ui.row(
        ui.column(3, ui.input_date_range("date_range", "날짜 범위:")),
        ui.column(3, ui.input_select("severity", "심각도:",
                  choices=["전체", "HIGH", "MEDIUM", "LOW"], selected="전체")),
        ui.column(3, ui.input_select("status", "상태:",
                  choices=["전체", "ACTIVE", "RESOLVED"], selected="전체")),
        ui.column(3, ui.input_action_button("refresh", "새로고침"))
    ),
    
    # 요약 통계 영역
    ui.row(
        ui.column(3, ui.value_box("total_alarms", "총 알람 수", theme="primary")),
        ui.column(3, ui.value_box("active_alarms", "활성 알람 수", theme="danger")),
        ui.column(3, ui.value_box("resolved_alarms", "해결된 알람 수", theme="success")),
        ui.column(3, ui.value_box("avg_resolution_time", "평균 해결 시간", theme="info"))
    ),
    
    # 차트 영역 1
    ui.row(
        ui.column(6, ui.output_plot("time_series")),
        ui.column(6, ui.output_plot("severity_pie"))
    ),
    
    # 차트 영역 2
    ui.row(
        ui.column(6, ui.output_plot("equipment_bar")),
        ui.column(6, ui.output_plot("hourly_heatmap"))
    ),
    
    # 테이블 영역
    ui.row(
        ui.column(12, ui.output_table("alarm_table"))
    )
)

def server(input, output, session):
    # ... 각 출력 컴포넌트에 대한 렌더링 함수 구현 ...
    
    # 예: 시계열 차트
    @render.plot
    def time_series():
        # ... 시계열 차트 구현 ...
        
    # 예: 심각도별 파이 차트
    @render.plot
    def severity_pie():
        # ... 파이 차트 구현 ...
        
    # ... 기타 차트 및 테이블 구현 ...

app = App(app_ui, server)
```

## 시각화 디자인 원칙

1. **일관성**: 색상, 스타일, 레이아웃의 일관성 유지
2. **간결성**: 불필요한 요소 최소화, 데이터-잉크 비율 최적화
3. **의미성**: 색상, 크기, 위치 등이 데이터의 의미를 잘 전달하도록 설계
4. **상호작용성**: 필터, 드릴다운, 호버 등 사용자 상호작용 제공
5. **반응성**: 다양한 화면 크기에 적응하는 반응형 디자인 구현

## 시각화 색상 가이드

알람 시각화에 적합한 색상 체계:

- **심각도 색상**: 
  - `HIGH`: #FF4136 (빨강)
  - `MEDIUM`: #FF851B (주황)
  - `LOW`: #FFDC00 (노랑)
- **상태 색상**:
  - `ACTIVE`: #FF4136 (빨강)
  - `ACKNOWLEDGED`: #0074D9 (파랑)
  - `RESOLVED`: #2ECC40 (초록)
- **차트 기본 색상**: #0074D9 (파랑)
- **배경 색상**: #FFFFFF (흰색) 또는 #F8F9FA (연한 회색)

## 시각화 최적화 팁

1. **대용량 데이터 처리**:
   - 데이터 집계를 DB 쿼리 단계에서 수행
   - 시각화 시 필요한 데이터만 로드
   - 대규모 시계열 데이터는 리샘플링/다운샘플링 적용

2. **인터랙티브 성능 향상**:
   - 초기 로딩 시 필요한 데이터만 표시
   - 사용자 액션에 따라 추가 데이터 로드
   - 복잡한 계산은 캐싱 적용

3. **UI/UX 개선**:
   - 로딩 인디케이터 추가
   - 에러 처리 및 사용자 피드백 제공
   - 직관적인 컨트롤과 명확한 레이블 사용

## 참고 자료
- Plotly 문서: [https://plotly.com/python/](https://plotly.com/python/)
- Matplotlib 문서: [https://matplotlib.org/](https://matplotlib.org/)
- Seaborn 문서: [https://seaborn.pydata.org/](https://seaborn.pydata.org/)
- 데이터 시각화 모범 사례: [https://www.tableau.com/learn/articles/data-visualization-tips](https://www.tableau.com/learn/articles/data-visualization-tips) 