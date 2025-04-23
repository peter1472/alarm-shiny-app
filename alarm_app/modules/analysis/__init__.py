# 분석 모듈
# app.modules.analysis.__init__.py

from alarm_app.modules.analysis.ui import ui
from alarm_app.modules.analysis.server import server

def load_analysis_data():
    """
    분석 모듈의 데이터를 초기 로드하는 함수
    
    현재는 구현 중인 상태입니다.
    """
    return True

__all__ = ["ui", "server", "load_analysis_data"] 