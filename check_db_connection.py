"""
데이터베이스 연결 및 테이블 상태를 확인하는 스크립트
"""
import os
import sys
from alarm_app.utils import db

# DB 경로 출력
print(f"데이터베이스 경로: {db.DB_PATH}")
print(f"데이터베이스 파일 존재 여부: {os.path.exists(db.DB_PATH)}")

# 데이터베이스 상태 확인
db_status = db.check_database()
print("\n데이터베이스 상태:")
print(f"연결 성공: {db_status.get('connected', False)}")

if db_status.get('connected', False):
    print(f"\n테이블 목록:")
    for table in db_status.get('tables', []):
        count = db_status.get('table_counts', {}).get(table, 0)
        print(f"- {table}: {count}개 레코드")
    
    # 설비 마스터 데이터 샘플 조회
    print("\n설비 마스터 데이터 샘플:")
    try:
        equipment_df = db.query_to_df("SELECT * FROM equipment_master LIMIT 5")
        if not equipment_df.empty:
            print(equipment_df)
        else:
            print("데이터가 없습니다.")
    except Exception as e:
        print(f"설비 마스터 데이터 조회 중 오류 발생: {str(e)}")
    
    # 코드 마스터 데이터 샘플 조회
    print("\n코드 마스터 데이터 샘플:")
    try:
        code_df = db.query_to_df("SELECT * FROM code_master LIMIT 5")
        if not code_df.empty:
            print(code_df)
        else:
            print("데이터가 없습니다.")
    except Exception as e:
        print(f"코드 마스터 데이터 조회 중 오류 발생: {str(e)}")
else:
    print(f"오류: {db_status.get('error', '알 수 없는 오류')}")

print("\n스크립트 실행 완료") 