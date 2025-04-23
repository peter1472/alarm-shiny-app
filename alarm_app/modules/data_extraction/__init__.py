# 데이터 추출 모듈
# app.modules.data_extraction.__init__.py

from alarm_app.modules.data_extraction.ui import ui
from alarm_app.modules.data_extraction.server import server

def load_extraction_data():
    """
    데이터 추출 모듈의 데이터를 초기 로드하는 함수
    
    현재는 구현 중인 상태입니다.
    """
    return True

__all__ = ["ui", "server", "load_extraction_data"] 