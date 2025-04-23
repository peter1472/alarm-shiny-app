# 대시보드 모듈
# app.modules.dashboard.__init__.py

from alarm_app.modules.dashboard.ui import ui
from alarm_app.modules.dashboard.server import server

def load_dashboard_data():
    """
    대시보드 데이터를 초기 로드하는 함수
    
    현재는 구현 중인 상태입니다.
    """
    return True

__all__ = ["ui", "server", "load_dashboard_data"] 