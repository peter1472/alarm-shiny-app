"""
기준정보 관리 모듈

설비, 알람, 코드 마스터 데이터를 관리하는 모듈입니다.
"""

from alarm_app.modules.master_data.ui import ui
from alarm_app.modules.master_data.server import server

def load_master_data():
    """
    마스터 데이터를 초기 로드하는 함수
    
    현재는 구현 중인 상태입니다.
    """
    return True

__all__ = ["ui", "server", "load_master_data"] 