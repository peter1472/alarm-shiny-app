import sqlite3
import os

# 데이터베이스 연결
db_path = os.path.join('db', 'alarm_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 테이블 목록 확인
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"데이터베이스 경로: {os.path.abspath(db_path)}")
print("\n데이터베이스 내 테이블 목록:")
for table in tables:
    print(f"- {table[0]}")

# coded_attribute 테이블 내용 확인
cursor.execute("SELECT COUNT(*) FROM coded_attribute")
count = cursor.fetchone()[0]
print(f"\ncoded_attribute 테이블 레코드 수: {count}")

print("\ncoded_attribute 테이블 내용:")
cursor.execute("SELECT column_name, is_coded, code_category, code_source FROM coded_attribute")
rows = cursor.fetchall()
for row in rows:
    column_name, is_coded, code_category, code_source = row
    coded_status = "코드화됨" if is_coded else "코드화되지 않음"
    category_info = f", 카테고리: {code_category}" if code_category else ""
    source_info = f", 소스: {code_source}" if code_source else ""
    print(f"- {column_name}: {coded_status}{category_info}{source_info}")

# 연결 종료
conn.close() 