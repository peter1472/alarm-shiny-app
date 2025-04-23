import os
import argparse
from alarm_app.repositories.data_repositories import DatabaseManager, CodeMasterRepository, EquipmentMasterRepository, AlarmMasterRepository
from alarm_app.services.data_services import CodeMasterService, EquipmentMasterService, AlarmMasterService

def create_services():
    """서비스 객체들을 생성하여 반환"""
    # 데이터베이스 경로 설정
    db_path = os.path.join('db', 'alarm_database.db')
    
    # 데이터베이스 관리자 초기화
    db_manager = DatabaseManager(db_path)
    
    # 리포지토리 초기화
    code_repo = CodeMasterRepository(db_manager)
    equipment_repo = EquipmentMasterRepository(db_manager)
    alarm_repo = AlarmMasterRepository(db_manager)
    
    # 서비스 초기화
    code_service = CodeMasterService(code_repo)
    equipment_service = EquipmentMasterService(equipment_repo)
    alarm_service = AlarmMasterService(alarm_repo)
    
    return code_service, equipment_service, alarm_service

def load_all_data(code_file, equipment_file, alarm_file):
    """모든 데이터 파일을 로드"""
    code_service, equipment_service, alarm_service = create_services()
    
    # 데이터 로드
    try:
        if code_file:
            print(f"\n코드 마스터 데이터 로드 중... (파일: {code_file})")
            code_service.import_from_file(code_file)
            print("코드 마스터 데이터 로드 완료")
        
        if equipment_file:
            print(f"\n설비 마스터 데이터 로드 중... (파일: {equipment_file})")
            equipment_service.import_from_file(equipment_file)
            print("설비 마스터 데이터 로드 완료")
        
        if alarm_file:
            print(f"\n알람 마스터 데이터 로드 중... (파일: {alarm_file})")
            alarm_service.import_from_file(alarm_file)
            print("알람 마스터 데이터 로드 완료")
        
        print("\n모든 데이터가 성공적으로 로드되었습니다!")
        return True
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {e}")
        raise 