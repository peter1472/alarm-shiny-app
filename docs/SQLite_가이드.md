# SQLite 가이드

## 개요
SQLite는 서버리스(Serverless), 설정이 필요 없는 자체 완결형(Self-contained) 데이터베이스 엔진입니다. 파일 기반으로 동작하므로 별도의 서버 설정이 필요 없고, 가볍고 빠르게 사용할 수 있어 소규모 애플리케이션에 적합합니다.

## SQLite의 주요 특징

### 1. 서버리스(Serverless)
- 클라이언트-서버 아키텍처 불필요
- 데이터베이스 서버 프로세스 없음
- 애플리케이션에 직접 통합됨

### 2. 자체 완결형(Self-contained)
- 외부 의존성 최소화
- 하나의 파일에 모든 데이터베이스 내용 저장
- 쉬운 백업 및 이동

### 3. 제로 설정(Zero-configuration)
- 설치 및 설정 과정 불필요
- 즉시 사용 가능
- 관리 부담 감소

### 4. 트랜잭션 지원
- ACID(원자성, 일관성, 고립성, 지속성) 속성 준수
- 안정적인 데이터 관리
- 데이터 무결성 보장

## 파이썬에서의 SQLite 사용

### 1. 기본 사용법
```python
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('alarms.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS alarm_events (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    equipment_id TEXT,
    alarm_code TEXT,
    severity TEXT,
    status TEXT
)
''')

# 데이터 삽입
cursor.execute('''
INSERT INTO alarm_events (timestamp, equipment_id, alarm_code, severity, status)
VALUES (?, ?, ?, ?, ?)
''', ('2023-07-01 08:30:00', 'EQ001', 'AL001', 'HIGH', 'ACTIVE'))

# 변경사항 저장
conn.commit()

# 데이터 조회
cursor.execute('SELECT * FROM alarm_events')
rows = cursor.fetchall()
for row in rows:
    print(row)

# 연결 종료
conn.close()
```

### 2. 파이썬 Shiny에서의 사용
```python
from shiny import App, ui, render
import sqlite3
import pandas as pd

# 데이터베이스 연결 함수
def get_connection():
    return sqlite3.connect('alarms.db')

app_ui = ui.page_fluid(
    ui.h1("알람 데이터 분석"),
    ui.output_table("alarm_data")
)

def server(input, output, session):
    @render.table
    def alarm_data():
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM alarm_events LIMIT 10", conn)
        conn.close()
        return df

app = App(app_ui, server)
```

## 우리 프로젝트의 데이터베이스 구조

### 1. 알람 이벤트 테이블 (alarm_events)
```sql
CREATE TABLE alarm_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    alarm_code TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT,
    resolved_timestamp TEXT,
    resolved_by TEXT,
    FOREIGN KEY (equipment_id) REFERENCES equipment_master(equipment_id),
    FOREIGN KEY (alarm_code) REFERENCES alarm_master(alarm_code)
);
```

### 2. 설비 마스터 테이블 (equipment_master)
```sql
CREATE TABLE equipment_master (
    equipment_id TEXT PRIMARY KEY,
    equipment_name TEXT NOT NULL,
    equipment_type TEXT NOT NULL,
    location TEXT,
    person_in_charge TEXT
);
```

### 3. 알람 마스터 테이블 (alarm_master)
```sql
CREATE TABLE alarm_master (
    alarm_code TEXT PRIMARY KEY,
    alarm_name TEXT NOT NULL,
    description TEXT,
    resolution_steps TEXT
);
```

### 4. 코드 테이블 (code_tables)
```sql
CREATE TABLE code_tables (
    code_type TEXT NOT NULL,
    code_value TEXT NOT NULL,
    code_description TEXT NOT NULL,
    PRIMARY KEY (code_type, code_value)
);
```

## 인덱스 설계
성능 최적화를 위한 인덱스 추가:

```sql
-- 시간별 검색 최적화
CREATE INDEX idx_alarm_events_timestamp ON alarm_events(timestamp);

-- 설비별 검색 최적화
CREATE INDEX idx_alarm_events_equipment ON alarm_events(equipment_id);

-- 알람 코드별 검색 최적화
CREATE INDEX idx_alarm_events_alarm_code ON alarm_events(alarm_code);

-- 심각도별 검색 최적화
CREATE INDEX idx_alarm_events_severity ON alarm_events(severity);

-- 상태별 검색 최적화
CREATE INDEX idx_alarm_events_status ON alarm_events(status);
```

## 주의사항
- SQLite는 동시 접근에 제한이 있으므로 대규모 다중 사용자 환경에는 적합하지 않음
- 복잡한 트랜잭션이 많은 경우 성능이 저하될 수 있음
- 데이터베이스 파일 백업 관리 필요

## 참고 자료
- SQLite 공식 웹사이트: [https://www.sqlite.org/](https://www.sqlite.org/)
- 파이썬 SQLite 문서: [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html) 