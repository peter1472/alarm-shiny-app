"""
기준정보 관리 UI 컴포넌트

설비, 알람, 코드 마스터 데이터를 관리하는 UI 요소를 정의합니다.
"""

from shiny import ui

# 코드 마스터 관리 탭 UI 정의
def code_master_tab():
    return ui.div(
        ui.layout_sidebar(
            # 사이드바 영역
            ui.sidebar(
                ui.card(
                    ui.card_header("코드 마스터 필터"),
                    ui.div(
                        # 검색 입력
                        ui.input_text("code_search", "통합 검색", placeholder="검색어 입력..."),
                        
                        ui.hr(),
                        
                        # 필드별 필터
                        ui.input_select("code_type_filter", "type",
                                       choices=["전체"] + [], multiple=False),
                        ui.input_select("code_category_filter", "category",
                                       choices=["전체"] + [], multiple=False),
                        
                        ui.br(),
                        
                        # 초기화 버튼만 유지
                        ui.div(
                            ui.input_action_button("reset_code_filter", "필터 초기화", 
                                                 class_="btn-outline-secondary"),
                            class_="d-flex justify-content-end"
                        ),
                        style="padding: 15px;"
                    )
                )
            ),
            
            # 메인 영역
            # 데이터 조회 카드
            ui.card(
                ui.card_header(
                    ui.row(
                        ui.column(6, ui.h4("코드 마스터 데이터")),
                        ui.column(6, ui.div(
                            ui.output_text("code_count_text"),
                            style="text-align: right;"
                        ))
                    )
                ),
                ui.card_body(
                    ui.output_data_frame("code_table")
                )
            ),
            
            ui.br(),
            
            # 데이터 편집 카드
            ui.card(
                ui.card_header(
                    ui.row(
                        ui.column(6, ui.h4("코드 데이터 편집")),
                        ui.column(6, ui.div(
                            ui.input_action_button("add_code", "추가", 
                                                 class_="btn-success me-2"),
                            ui.input_action_button("update_code", "수정", 
                                                 class_="btn-warning me-2"),
                            ui.input_action_button("delete_code", "삭제", 
                                                 class_="btn-danger"),
                            class_="d-flex justify-content-end"
                        ))
                    )
                ),
                ui.card_body(
                    ui.div(
                        ui.row(
                            ui.column(6, ui.input_text("type", "type")),
                            ui.column(6, ui.input_text("code", "code"))
                        ),
                        ui.row(
                            ui.column(6, ui.input_text("value", "value")),
                            ui.column(6, ui.input_text("category", "category"))
                        ),
                        ui.row(
                            ui.column(12, ui.input_text("eng_category", "eng_category"))
                        )
                    )
                ),
                ui.card_footer(
                    ui.output_ui("code_edit_result")
                )
            )
        )
    )

# 통합된 마스터 데이터 UI
master_data_ui = ui.navset_card_tab(
    ui.nav_panel("코드 마스터", code_master_tab()),
    # 추후 알람 마스터, 설비 마스터 탭 추가 예정
    id="master_data_tabs"
) 