# 리포트 생성 모듈
# app.modules.report_generator.__init__.py

from alarm_app.modules.report_generator.ui import ui
from alarm_app.modules.report_generator.server import server

def load_report_data():
    """
    리포트 생성 모듈의 데이터를 초기 로드하는 함수
    
    현재는 구현 중인 상태입니다.
    """
    return True

__all__ = ["ui", "server", "load_report_data"] 