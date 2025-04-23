import sqlite3
import pandas as pd
import os
from typing import List, Optional, Dict, Any
from alarm_app.models.data_models import CodeMaster, EquipmentMaster, AlarmMaster, CodedAttribute

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)

class CodeMasterRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def load_from_file(self, file_path: str) -> None:
        """파일에서 데이터를 로드하여 DB에 저장"""
        conn = self.db_manager.get_connection()
        # 기존 데이터 삭제
        cursor = conn.cursor()
        cursor.execute("DELETE FROM code_master")
        conn.commit()
        
        # 새 데이터 로드
        df = pd.read_csv(file_path, delimiter='\t')
        # 칼럼명 소문자로 변환 (SQLite 표준 맞추기)
        df.columns = [col.lower() for col in df.columns]
        df.to_sql('code_master', conn, if_exists='append', index=False)
        conn.close()
        print(f"코드 마스터: {len(df)} 행이 로드되었습니다.")
    
    def get_all(self) -> List[CodeMaster]:
        """모든 코드 마스터 데이터 조회"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT code_id, type, code, value, category, eng_category FROM code_master")
        rows = cursor.fetchall()
        conn.close()
        
        return [CodeMaster(
            code_id=row[0],
            type=row[1], 
            code=row[2], 
            value=row[3], 
            category=row[4], 
            eng_category=row[5]
        ) for row in rows]

class EquipmentMasterRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def load_from_file(self, file_path: str) -> None:
        """파일에서 데이터를 로드하여 DB에 저장"""
        conn = self.db_manager.get_connection()
        # 기존 데이터 삭제
        cursor = conn.cursor()
        cursor.execute("DELETE FROM equipment_master")
        conn.commit()
        
        # 새 데이터 로드
        df = pd.read_csv(file_path, delimiter='\t')
        
        # 칼럼 이름 매핑 (원본 파일의 칼럼명을 DB 테이블의 칼럼명에 맞게 변환)
        column_mapping = {
            'MACHINENAME': 'machinename',
            'PROCESS_C': 'process_c',
            'ROOM_C': 'room_c',
            'EQUIPMENT_C': 'equipment_c',
            'EQ_GROUP_C': 'eq_group_c',
            'EQ_CLASS_C': 'eq_class_c',
            'LOGISTICS_C': 'logistics_c',
            'FLOOR_C': 'floor_c',
            'POLARITY_C': 'polarity_c',
            '설비명 상세': 'eq_detail',
            'MCS 설비명 출처': 'mcs_source',
            'MCS 설비명': 'mcs_name',
            '가상': 'is_virtual',
            '제외': 'is_excluded',
            '상위CIM': 'upper_cim',
            '알람그룹': 'alarm_group',
            '공급업체': 'supplier',
            '비고': 'remarks'
        }
        
        # 칼럼명 변경
        df = df.rename(columns=column_mapping)
        
        # 불리언 칼럼 처리
        df['is_virtual'] = df['is_virtual'].fillna('').apply(lambda x: 1 if x == 'Y' else 0)
        df['is_excluded'] = df['is_excluded'].fillna('').apply(lambda x: 1 if x == 'Y' else 0)
        
        # 누락된 칼럼 처리
        for col in ['eq_detail', 'mcs_source', 'mcs_name', 'upper_cim', 'alarm_group', 'supplier', 'remarks']:
            if col not in df.columns:
                df[col] = ''
        
        # DB에 저장
        df.to_sql('equipment_master', conn, if_exists='append', index=False)
        conn.close()
        print(f"설비 마스터: {len(df)} 행이 로드되었습니다.")
    
    def get_all(self) -> List[EquipmentMaster]:
        """모든 설비 마스터 데이터 조회"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT eq_id, machinename, process_c, room_c, equipment_c, 
                   eq_group_c, eq_class_c, logistics_c, floor_c, polarity_c,
                   eq_detail, mcs_source, mcs_name, is_virtual, is_excluded,
                   upper_cim, alarm_group, supplier, remarks 
            FROM equipment_master
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [EquipmentMaster(
            eq_id=row[0],
            machinename=row[1],
            process_c=row[2],
            room_c=row[3],
            equipment_c=row[4],
            eq_group_c=row[5],
            eq_class_c=row[6],
            logistics_c=row[7],
            floor_c=row[8],
            polarity_c=row[9],
            eq_detail=row[10],
            mcs_source=row[11],
            mcs_name=row[12],
            is_virtual=bool(row[13]),
            is_excluded=bool(row[14]),
            upper_cim=row[15],
            alarm_group=row[16],
            supplier=row[17],
            remarks=row[18]
        ) for row in rows]

class AlarmMasterRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def load_from_file(self, file_path: str) -> None:
        """파일에서 데이터를 로드하여 DB에 저장"""
        conn = self.db_manager.get_connection()
        # 기존 데이터 삭제
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alarm_master")
        conn.commit()
        
        # 새 데이터 로드
        df = pd.read_csv(file_path, delimiter='\t')
        
        # 칼럼 이름 매핑
        column_mapping = {
            'ALARMID': 'alarmid',
            'ALARMCODE': 'alarmcode',
            'CATEGORY': 'category',
            'DESCRIPTION': 'description',
            'SEVERITY': 'severity',
            'ALARM_CAUSE': 'alarm_cause',
            'SEVERITY_DESC': 'severity_desc',
            'SEVERITY_RATIO': 'severity_ratio'
        }
        
        # 칼럼명 변경
        df = df.rename(columns=column_mapping)
        
        # 퍼센트 문자열을 숫자로 변환
        df['severity_ratio'] = df['severity_ratio'].str.replace('%', '').astype(float) / 100
        
        # DB에 저장
        df.to_sql('alarm_master', conn, if_exists='append', index=False)
        conn.close()
        print(f"알람 마스터: {len(df)} 행이 로드되었습니다.")
    
    def get_all(self) -> List[AlarmMaster]:
        """모든 알람 마스터 데이터 조회"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT alarm_id, alarmid, alarmcode, category, description, 
                   severity, alarm_cause, severity_desc, severity_ratio
            FROM alarm_master
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [AlarmMaster(
            alarm_id=row[0],
            alarmid=row[1],
            alarmcode=row[2],
            category=row[3],
            description=row[4],
            severity=row[5],
            alarm_cause=row[6],
            severity_desc=row[7],
            severity_ratio=row[8]
        ) for row in rows]

class CodedAttributeRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all(self) -> List[CodedAttribute]:
        """모든 코드화 속성 데이터 조회"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT attr_id, column_name, is_coded, code_category, code_source
            FROM coded_attribute
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [CodedAttribute(
            attr_id=row[0],
            column_name=row[1],
            is_coded=bool(row[2]),
            code_category=row[3],
            code_source=row[4]
        ) for row in rows] 