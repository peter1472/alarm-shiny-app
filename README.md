# 알람 분석 시스템

배터리 제조 공정의 알람, 설비, 코드 데이터를 분석하기 위한 Shiny 애플리케이션입니다.

## 프로젝트 구조

```
alarm_shiny/
│
├── alarm_app/               # 애플리케이션 코드
│   ├── components/          # 재사용 가능한 UI 컴포넌트 (헤더, 푸터 등)
│   ├── modules/             # 모듈식 기능 구현
│   │   ├── dashboard/       # 대시보드 모듈
│   │   ├── master_data/     # 기준정보 관리 모듈
│   │   ├── data_extraction/ # 데이터 추출 모듈
│   │   ├── analysis/        # 분석 모듈
│   │   └── report_generator/# 리포트 생성 모듈
│   ├── models/              # 데이터 모델 클래스
│   ├── repositories/        # 데이터 액세스 계층
│   ├── services/            # 비즈니스 로직 계층
│   ├── utils/               # 유틸리티 함수
│   └── www/                 # 정적 파일 (CSS, JS, 이미지 등)
│
├── data/                    # 데이터 파일
│   └── raw/                 # 원본 데이터 파일
│       ├── code_master.txt
│       ├── equipment_master.txt
│       └── alarm_master.txt
│
├── db/                      # 데이터베이스 파일
│   └── alarm_database.db
│
├── docs/                    # 문서
├── scripts/                 # 유틸리티 스크립트
├── tests/                   # 테스트 코드
├── venv/                    # 가상 환경 (버전 관리에서 제외)
│
├── app.py                   # 애플리케이션 엔트리 포인트
├── config.py                # 구성 파일
├── requirements.txt         # 필수 패키지 목록
└── README.md                # 프로젝트 설명서
```

## 설치 및 설정

1. 필요 패키지 설치:
   ```
   pip install -r requirements.txt
   ```

2. 애플리케이션 실행:
   ```
   python app.py
   ```

## 모듈 구성

1. **대시보드 (Dashboard)**
   - 실시간 알람 상태 및 요약 정보 표시
   - 주요 지표의 시각화 차트 제공

2. **기준정보 관리 (Master Data)**
   - 설비, 알람, 코드 마스터 데이터 관리
   - 데이터 조회, 필터링, 편집 기능

3. **데이터 추출 (Data Extraction)**
   - 다양한 소스에서 알람 데이터 추출
   - 데이터 전처리 및 변환 기능

4. **분석 (Analysis)**
   - 알람 데이터 분석 및 통계 처리
   - 다양한 시각화 도구 제공

5. **리포트 생성 (Report Generator)**
   - 분석 결과를 기반으로 보고서 생성
   - 다양한 형식의 보고서 템플릿 지원

## 데이터 모델

1. **코드 마스터 (code_master)**
   - 모든 코드 체계를 관리하는 테이블
   - 각 코드의 유형, 값, 카테고리 정보 포함

2. **설비 마스터 (equipment_master)**
   - 설비 정보를 관리하는 테이블
   - 설비 코드, 설비명, 그룹, 분류 등의 정보 포함

3. **알람 마스터 (alarm_master)**
   - 알람 정보를 관리하는 테이블
   - 알람 코드, 설명, 심각도, 원인 등의 정보 포함

## 개발 상태

현재 이 프로젝트는 개발 초기 단계입니다:

- 기본 애플리케이션 구조 설정 완료
- 모듈 구조화 및 UI 템플릿 구현 중
- 각 모듈별 기능 개발 예정

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`).
3. 변경 사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`).
5. Pull Request를 제출합니다.

## 저작권 및 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요. 