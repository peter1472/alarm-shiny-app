import sqlite3
import os

# db 폴더 생성 (없는 경우)
db_folder = 'db'
if not os.path.exists(db_folder):
    os.makedirs(db_folder)
    print(f"'{db_folder}' 폴더가 생성되었습니다.")
else:
    print(f"'{db_folder}' 폴더가 이미 존재합니다.")

# 데이터베이스 파일 생성 경로 설정
db_path = os.path.join(db_folder, 'alarm_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 기존 테이블이 있다면 삭제
cursor.execute("DROP TABLE IF EXISTS code_master")
cursor.execute("DROP TABLE IF EXISTS equipment_master")
cursor.execute("DROP TABLE IF EXISTS coded_attribute")
cursor.execute("DROP TABLE IF EXISTS alarm_master")

# 테이블 생성
# 1. 코드 마스터 테이블
cursor.execute('''
CREATE TABLE code_master (
    code_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50),
    code VARCHAR(20),
    value VARCHAR(100),
    category VARCHAR(50),
    eng_category VARCHAR(50)
)
''')

# 2. 설비 마스터 테이블
cursor.execute('''
CREATE TABLE equipment_master (
    eq_id INTEGER PRIMARY KEY AUTOINCREMENT,
    machinename VARCHAR(20),
    process_c VARCHAR(10),
    room_c VARCHAR(10),
    equipment_c VARCHAR(10),
    eq_group_c VARCHAR(10),
    eq_class_c VARCHAR(10),
    logistics_c VARCHAR(10),
    floor_c VARCHAR(10),
    polarity_c VARCHAR(10),
    eq_detail VARCHAR(100),
    mcs_source VARCHAR(50),
    mcs_name VARCHAR(100),
    is_virtual BOOLEAN,
    is_excluded BOOLEAN,
    upper_cim VARCHAR(50),
    alarm_group VARCHAR(50),
    supplier VARCHAR(50),
    remarks TEXT
)
''')

# 3. 코드화 속성 테이블
cursor.execute('''
CREATE TABLE coded_attribute (
    attr_id INTEGER PRIMARY KEY AUTOINCREMENT,
    column_name VARCHAR(50),
    is_coded BOOLEAN,
    code_category VARCHAR(50),
    code_source VARCHAR(100)
)
''')

# 4. 알람 마스터 테이블
cursor.execute('''
CREATE TABLE alarm_master (
    alarm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alarmid INTEGER,
    alarmcode INTEGER,
    category VARCHAR(50),
    description TEXT,
    severity INTEGER,
    alarm_cause VARCHAR(50),
    severity_desc TEXT,
    severity_ratio REAL
)
''')

# 코드화 속성 정보 삽입
coded_columns = [
    ('PROCESS_C', 1, '공정', 'code_master.txt'),
    ('ROOM_C', 1, 'Room', 'code_master.txt'),
    ('EQUIPMENT_C', 1, '설비', 'code_master.txt'),
    ('EQ_GROUP_C', 1, '설비그룹', 'code_master.txt'),
    ('EQ_CLASS_C', 1, '설비구분', 'code_master.txt'),
    ('LOGISTICS_C', 1, '물류', 'code_master.txt'),
    ('FLOOR_C', 1, '층', 'code_master.txt'),
    ('POLARITY_C', 1, '극성', 'code_master.txt'),
    ('MACHINENAME', 0, '', ''),
    ('설비명 상세', 0, '', ''),
    ('MCS 설비명 출처', 0, '', ''),
    ('MCS 설비명', 0, '', ''),
    ('가상', 0, '', ''),
    ('제외', 0, '', ''),
    ('상위CIM', 0, '', ''),
    ('알람그룹', 0, '', ''),
    ('공급업체', 0, '', ''),
    ('비고', 0, '', '')
]

cursor.executemany(
    "INSERT INTO coded_attribute (column_name, is_coded, code_category, code_source) VALUES (?, ?, ?, ?)",
    coded_columns
)

# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()

print(f"데이터베이스가 성공적으로 생성되었습니다: {os.path.abspath(db_path)}")
print("생성된 테이블:")
print("1. code_master: 코드 체계 관리")
print("2. equipment_master: 설비 정보 관리")
print("3. coded_attribute: 코드화 속성 관리")
print("4. alarm_master: 알람 정보 관리") 