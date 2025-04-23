import sqlite3
import pandas as pd
import os
from typing import List, Dict, Any, Optional, Union, Tuple

# 데이터베이스 파일 경로
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db', 'alarm_database.db')

def get_connection():
    """
    SQLite 데이터베이스 연결을 반환합니다.
    
    Returns:
        sqlite3.Connection: 데이터베이스 연결 객체
    """
    return sqlite3.connect(DB_PATH)

def query_to_df(query: str, params: Optional[List] = None) -> pd.DataFrame:
    """
    SQL 쿼리를 실행하고 결과를 DataFrame으로 반환합니다.
    
    Args:
        query (str): 실행할 SQL 쿼리
        params (Optional[List], optional): 쿼리 파라미터. 기본값은 None.
        
    Returns:
        pd.DataFrame: 쿼리 결과가 담긴 DataFrame
    """
    try:
        conn = get_connection()
        # 디버깅용 출력 추가
        print(f"Executing query: {query}")
        if params:
            print(f"With parameters: {params}")
            
        df = pd.read_sql_query(query, conn, params=params if params else None)
        return df
    except Exception as e:
        print(f"데이터베이스 쿼리 실행 중 오류 발생: {str(e)}")
        # 오류 발생 시 빈 DataFrame 반환
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def execute_query(query: str, params: Optional[List] = None) -> int:
    """
    SQL 쿼리를 실행하고 영향 받은 행 수를 반환합니다.
    
    Args:
        query (str): 실행할 SQL 쿼리
        params (Optional[List], optional): 쿼리 파라미터. 기본값은 None.
        
    Returns:
        int: 영향 받은 행 수
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 디버깅용 출력 추가
        print(f"Executing update/delete query: {query}")
        if params:
            print(f"With parameters: {params}")
            
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"데이터베이스 쿼리 실행 중 오류 발생: {str(e)}")
        if conn:
            conn.rollback()
        return 0
    finally:
        if conn:
            conn.close()

def check_database():
    """
    데이터베이스 연결 및 테이블 존재 여부를 확인합니다.
    
    Returns:
        Dict[str, Any]: 데이터베이스 상태 정보
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 테이블 목록 조회
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        result = {
            "connected": True,
            "tables": tables,
            "table_counts": {}
        }
        
        # 각 테이블의 레코드 수 조회
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            result["table_counts"][table] = count
        
        return result
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()

def fetch_one(query: str, params: Optional[Union[List, Tuple, Dict]] = None) -> Optional[tuple]:
    """
    단일 레코드를 조회하는 함수
    
    Args:
        query (str): SQL 쿼리 문자열
        params (Optional[Union[List, Tuple, Dict]]): 쿼리 파라미터
        
    Returns:
        Optional[tuple]: 조회 결과 (없으면 None)
        
    Raises:
        Exception: 데이터베이스 연결 또는 쿼리 실행 중 오류 발생
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        return cursor.fetchone()
    except Exception as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
        raise
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def fetch_all(query: str, params: Optional[Union[List, Tuple, Dict]] = None) -> List[tuple]:
    """
    모든 레코드를 조회하는 함수
    
    Args:
        query (str): SQL 쿼리 문자열
        params (Optional[Union[List, Tuple, Dict]]): 쿼리 파라미터
        
    Returns:
        List[tuple]: 조회 결과 목록
        
    Raises:
        Exception: 데이터베이스 연결 또는 쿼리 실행 중 오류 발생
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        return cursor.fetchall()
    except Exception as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
        raise
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_table_info(table_name: str) -> List[Dict[str, Any]]:
    """
    테이블 스키마 정보 조회 함수
    
    Args:
        table_name (str): 테이블 이름
        
    Returns:
        List[Dict[str, Any]]: 테이블 컬럼 정보 목록
    """
    query = f"PRAGMA table_info({table_name})"
    df = query_to_df(query)
    return df.to_dict('records')

def get_record_count(table_name: str, where_clause: str = "", params: Optional[List] = None) -> int:
    """
    테이블의 레코드 수 조회 함수
    
    Args:
        table_name (str): 테이블 이름
        where_clause (str, optional): WHERE 조건절
        params (Optional[List], optional): 쿼리 파라미터
        
    Returns:
        int: 레코드 수
    """
    query = f"SELECT COUNT(*) FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"
    
    result = fetch_one(query, params)
    return result[0] if result else 0 