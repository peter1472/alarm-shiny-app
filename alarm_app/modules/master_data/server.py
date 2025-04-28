"""
기준정보 관리 서버 로직

설비, 알람, 코드 마스터 데이터를 관리하는 서버 로직을 정의합니다.
"""

from shiny import reactive, render, req, ui
import pandas as pd
import os
from config import get_db_path
from alarm_app.repositories.data_repositories import DatabaseManager, CodeMasterRepository
from alarm_app.services.data_services import CodeMasterService, EquipmentMasterService, AlarmMasterService
from alarm_app.models.data_models import CodeMaster

def handle_master_data(input, output, session):
    """
    기준정보 관리 페이지의 서버 로직
    
    현재 개발 중인 상태입니다.
    """
    # 서비스 초기화
    db_path = os.path.join('db', 'alarm_database.db')
    db_manager = DatabaseManager(db_path)
    code_repo = CodeMasterRepository(db_manager)
    code_service = CodeMasterService(code_repo)
    equip_service = EquipmentMasterService(db_path)
    alarm_service = AlarmMasterService(db_path)
    
    # 선택된 코드 ID 저장 변수
    selected_code_id = reactive.Value(None)
    
    # 결과 메시지 저장 변수
    result_message = reactive.Value({"text": "", "type": ""})
    
    # 데이터 다시 로드 트리거
    refresh_trigger = reactive.Value(0)
    
    # 코드 마스터 데이터 로드 (reactive.Calc로 캐싱)
    @reactive.Calc
    def get_code_data():
        """코드 마스터 데이터 조회 및 필터링"""
        # 값 변경 시 갱신 트리거
        refresh_trigger.get()
        
        # 전체 데이터 로드
        all_codes = code_service.get_all_codes()
        
        # 데이터프레임으로 변환
        df = pd.DataFrame([{
            'code_id': code.code_id,
            'type': code.type,
            'code': code.code,
            'value': code.value,
            'category': code.category,
            'eng_category': code.eng_category
        } for code in all_codes])
        
        if df.empty:
            return pd.DataFrame(columns=['code_id', 'type', 'code', 'value', 'category', 'eng_category'])
        
        # 필터링 적용
        code_type = input.code_type_filter()
        category = input.code_category_filter()
        search_term = input.code_search()
        
        # 코드 타입 필터
        if code_type and code_type != "전체":
            df = df[df["type"] == code_type]
            
        # 카테고리 필터
        if category and category != "전체":
            df = df[df["category"] == category]
            
        # 검색어 필터
        if search_term:
            search_term = search_term.lower()
            # 문자열 칼럼에 대해 검색
            df = df[
                df["type"].str.lower().str.contains(search_term, na=False) |
                df["code"].str.lower().str.contains(search_term, na=False) |
                df["value"].str.lower().str.contains(search_term, na=False) |
                df["category"].str.lower().str.contains(search_term, na=False) |
                df["eng_category"].str.lower().str.contains(search_term, na=False)
            ]
            
        return df
    
    # 데이터 갱신 함수
    def refresh_data():
        """데이터를 강제로 다시 로드"""
        refresh_trigger.set(refresh_trigger.get() + 1)
    
    # 필터 옵션 업데이트 함수
    def update_filter_options():
        """코드 마스터 필터 옵션 초기화"""
        all_codes = code_service.get_all_codes()
        
        # 데이터프레임으로 변환
        df = pd.DataFrame([{
            'type': code.type,
            'category': code.category
        } for code in all_codes])
        
        if df.empty:
            return
        
        # 고유한 타입과 카테고리 추출
        types = df["type"].unique().tolist()
        categories = df["category"].unique().tolist()
        
        # 필터 옵션 업데이트
        ui.update_select(
            "code_type_filter", 
            choices=["전체"] + types
        )
        ui.update_select(
            "code_category_filter", 
            choices=["전체"] + categories
        )
    
    # 테이블 출력
    @output
    @render.data_frame
    def code_table():
        """코드 테이블 표시"""
        df = get_code_data()
        # 데이터프레임 칼럼 순서 조정
        if not df.empty:
            # code_id는 내부 식별자로만 사용하고 표시하지 않음
            visible_cols = ['type', 'code', 'value', 'category', 'eng_category']
            # 필요한 칼럼만 선택하고 순서 지정
            display_df = df[['code_id'] + visible_cols].copy()
        else:
            display_df = df
            
        return render.DataGrid(
            display_df,
            selection_mode="row",
            height="400px",
            width="100%"
        )
    
    # 코드 수 표시
    @output
    @render.text
    def code_count_text():
        """코드 데이터 수 표시"""
        df = get_code_data()
        return f"총 {len(df)}개 항목"
    
    # 결과 메시지 표시
    @output
    @render.ui
    def code_edit_result():
        """코드 편집 결과 메시지 표시"""
        msg = result_message.get()
        if not msg["text"]:
            return None
            
        alert_class = ""
        if msg["type"] == "success":
            alert_class = "alert-success"
        elif msg["type"] == "error":
            alert_class = "alert-danger"
        elif msg["type"] == "warning":
            alert_class = "alert-warning"
        else:
            alert_class = "alert-info"
            
        return ui.div(
            ui.p(msg["text"]),
            class_=f"alert {alert_class} mb-0"
        )
    
    # 테이블 행 선택 이벤트
    @reactive.Effect
    @reactive.event(input.code_table_selected_rows)
    def _():
        # 선택된 행이 있는지 확인
        selected_rows = input.code_table_selected_rows()
        if not selected_rows:
            return
        
        # 선택된 행의 데이터 가져오기
        selected_idx = selected_rows[0]
        df = get_code_data()
        
        if selected_idx >= len(df):
            return
            
        selected_row = df.iloc[selected_idx]
        selected_code_id.set(selected_row['code_id'])
        
        # 편집 폼에 데이터 설정
        ui.update_text("type", value=selected_row['type'])
        ui.update_text("code", value=selected_row['code'])
        ui.update_text("value", value=selected_row['value'])
        ui.update_text("category", value=selected_row['category'])
        ui.update_text("eng_category", value=selected_row['eng_category'])
        
        # 결과 메시지 초기화
        result_message.set({"text": "", "type": ""})
    
    # 폼 초기화 함수
    def clear_form():
        """편집 폼 초기화"""
        selected_code_id.set(None)
        ui.update_text("type", value="")
        ui.update_text("code", value="")
        ui.update_text("value", value="")
        ui.update_text("category", value="")
        ui.update_text("eng_category", value="")
    
    # 코드 추가 처리
    @reactive.Effect
    @reactive.event(input.add_code)
    def _():
        """새 코드 데이터 추가"""
        # 입력값 가져오기
        code_type = input.type()
        code_value = input.code()
        value_desc = input.value()
        category = input.category()
        eng_category = input.eng_category()
        
        # 유효성 검사
        if not all([code_type, code_value, value_desc, category]):
            result_message.set({
                "text": "모든 필수 필드를 입력하세요.",
                "type": "warning"
            })
            return
        
        try:
            # 코드 객체 생성 (code_id는 None으로 설정하여 새 레코드 표시)
            code = CodeMaster(
                code_id=None,
                type=code_type,
                code=code_value,
                value=value_desc,
                category=category,
                eng_category=eng_category
            )
            
            # 코드 서비스를 통해 추가
            print(f"[DEBUG] 서비스 추가 호출 전: {code}")
            success = code_service.add_code(code)
            print(f"[DEBUG] 추가 결과: {success}")
            
            if success:
                result_message.set({
                    "text": "코드가 성공적으로 추가되었습니다.",
                    "type": "success"
                })
                
                # 폼 초기화
                clear_form()
                
                # 필터 옵션 업데이트
                update_filter_options()
                
                # 데이터 갱신
                refresh_data()
            else:
                result_message.set({
                    "text": "코드 추가에 실패했습니다.",
                    "type": "error"
                })
                
        except Exception as e:
            print(f"[ERROR] 서버에서 코드 추가 중 오류: {str(e)}")
            result_message.set({
                "text": f"코드 추가 중 오류 발생: {str(e)}",
                "type": "error"
            })
    
    # 코드 수정 처리
    @reactive.Effect
    @reactive.event(input.update_code)
    def _():
        """코드 데이터 업데이트"""
        # 코드 ID가 선택되었는지 확인
        code_id = selected_code_id.get()
        if code_id is None:
            result_message.set({
                "text": "수정할 코드를 먼저 선택하세요.",
                "type": "warning"
            })
            return
        
        # 입력값 가져오기
        code_type = input.type()
        code_value = input.code()
        value_desc = input.value()
        category = input.category()
        eng_category = input.eng_category()
        
        print(f"[DEBUG] 입력값: ID={code_id}, type={code_type}, code={code_value}, value={value_desc}, category={category}, eng_category={eng_category}")
        
        # 유효성 검사
        if not all([code_type, code_value, value_desc]):
            result_message.set({
                "text": "필수 필드를 모두 입력하세요.",
                "type": "error"
            })
            return
        
        try:
            # 코드 객체 생성
            code = CodeMaster(
                code_id=code_id,
                type=code_type,
                code=code_value,
                value=value_desc,
                category=category,
                eng_category=eng_category
            )
            
            # 코드 서비스를 통해 업데이트
            print(f"[DEBUG] 서비스 업데이트 호출 전: {code}")
            success = code_service.update_code(code)
            print(f"[DEBUG] 업데이트 결과: {success}")
            
            if success:
                result_message.set({
                    "text": "코드가 성공적으로 수정되었습니다.",
                    "type": "success"
                })
                
                # 필터 옵션 업데이트
                update_filter_options()
                
                # 데이터 갱신
                refresh_data()
            else:
                result_message.set({
                    "text": "코드 수정에 실패했습니다.",
                    "type": "error"
                })
                
        except Exception as e:
            print(f"[ERROR] 서버에서 코드 수정 중 오류: {str(e)}")
            result_message.set({
                "text": f"코드 수정 중 오류 발생: {str(e)}",
                "type": "error"
            })
    
    # 코드 삭제 처리
    @reactive.Effect
    @reactive.event(input.delete_code)
    def _():
        """코드 데이터 삭제"""
        # 코드 ID가 선택되었는지 확인
        code_id = selected_code_id.get()
        if code_id is None:
            result_message.set({
                "text": "삭제할 코드를 먼저 선택하세요.",
                "type": "warning"
            })
            return
            
        try:
            # code_id를 명시적으로 int로 변환
            code_id = int(code_id)
            print(f"[DEBUG] 삭제 시도: code_id={code_id}")
            
            # 코드 서비스를 통해 삭제
            success = code_service.delete_code(code_id)
            print(f"[DEBUG] 삭제 결과: {success}")
            
            if success:
                result_message.set({
                    "text": "코드가 성공적으로 삭제되었습니다.",
                    "type": "success"
                })
                
                # 필터 옵션 업데이트
                update_filter_options()
                
                # 데이터 갱신
                refresh_data()
                
                # 폼 초기화
                clear_form()
            else:
                result_message.set({
                    "text": "코드 삭제에 실패했습니다.",
                    "type": "error"
                })
            
        except Exception as e:
            print(f"[ERROR] 코드 삭제 중 오류 발생: {e}")
            result_message.set({
                "text": f"코드 삭제 중 오류 발생: {str(e)}",
                "type": "error"
            })
    
    # 필터 초기화
    @reactive.Effect
    @reactive.event(input.reset_code_filter)
    def _():
        ui.update_text("code_search", value="")
        ui.update_select("code_type_filter", selected="전체")
        ui.update_select("code_category_filter", selected="전체")
    
    # 초기화 실행
    update_filter_options()

def load_master_data():
    """
    마스터 데이터를 초기 로드하는 함수
    
    현재는 구현 중인 상태입니다.
    """
    return True 