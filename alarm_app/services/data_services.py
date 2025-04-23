from typing import List, Optional
from alarm_app.models.data_models import CodeMaster, EquipmentMaster, AlarmMaster, CodedAttribute
from alarm_app.repositories.data_repositories import (
    CodeMasterRepository, EquipmentMasterRepository, 
    AlarmMasterRepository, CodedAttributeRepository
)

class CodeMasterService:
    def __init__(self, repository: CodeMasterRepository):
        self.repository = repository
    
    def import_from_file(self, file_path: str) -> None:
        """파일에서 데이터 가져오기"""
        self.repository.load_from_file(file_path)
    
    def get_all_codes(self) -> List[CodeMaster]:
        """모든 코드 조회"""
        return self.repository.get_all()
    
    def get_codes_by_category(self, category: str) -> List[CodeMaster]:
        """카테고리별 코드 조회"""
        all_codes = self.repository.get_all()
        return [code for code in all_codes if code.category == category]

class EquipmentMasterService:
    def __init__(self, repository: EquipmentMasterRepository):
        self.repository = repository
    
    def import_from_file(self, file_path: str) -> None:
        """파일에서 데이터 가져오기"""
        self.repository.load_from_file(file_path)
    
    def get_all_equipment(self) -> List[EquipmentMaster]:
        """모든 설비 조회"""
        return self.repository.get_all()

class AlarmMasterService:
    def __init__(self, repository: AlarmMasterRepository):
        self.repository = repository
    
    def import_from_file(self, file_path: str) -> None:
        """파일에서 데이터 가져오기"""
        self.repository.load_from_file(file_path)
    
    def get_all_alarms(self) -> List[AlarmMaster]:
        """모든 알람 조회"""
        return self.repository.get_all()

class CodedAttributeService:
    def __init__(self, repository: CodedAttributeRepository):
        self.repository = repository
    
    def get_all_attributes(self) -> List[CodedAttribute]:
        """모든 코드화 속성 조회"""
        return self.repository.get_all()
    
    def get_coded_attributes(self) -> List[CodedAttribute]:
        """코드화된 속성만 조회"""
        all_attributes = self.repository.get_all()
        return [attr for attr in all_attributes if attr.is_coded] 