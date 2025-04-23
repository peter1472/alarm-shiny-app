import sqlite3
import os

# 데이터베이스 연결
db_path = os.path.join('db', 'alarm_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"데이터베이스 파일 경로: {os.path.abspath(db_path)}")
print(f"데이터베이스 파일 크기: {os.path.getsize(db_path) / 1024:.2f} KB")

# 테이블 목록 확인
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\n데이터베이스 테이블 목록:")
for i, table in enumerate(tables, 1):
    print(f"{i}. {table[0]}")

# 각 테이블의 레코드 수 확인
print("\n각 테이블의 레코드 수:")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"- {table_name}: {count}개")

# 테이블 스키마 확인
print("\n각 테이블의 스키마:")
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"\n{table_name} 테이블:")
    for col in columns:
        col_id, col_name, col_type, not_null, default_val, pk = col
        print(f"  - {col_name} ({col_type})" + (" [PK]" if pk else ""))

# 데이터 샘플 확인
print("\n각 테이블의 데이터 샘플 (최대 3개):")
for table in tables:
    table_name = table[0]
    if table_name == 'sqlite_sequence':
        continue  # sqlite 내부 테이블 건너뛰기
    
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
    rows = cursor.fetchall()
    
    print(f"\n{table_name} 테이블 샘플:")
    if rows:
        # 칼럼명 가져오기
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # 칼럼명 출력
        print("  " + " | ".join(columns))
        print("  " + "-" * (len(" | ".join(columns)) + 5))
        
        # 데이터 출력
        for row in rows:
            print("  " + " | ".join(str(val) for val in row))
    else:
        print("  데이터 없음")

# 연결 종료
conn.close()

print("\n데이터베이스 확인 완료") 