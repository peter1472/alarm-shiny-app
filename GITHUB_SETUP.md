# GitHub 리포지토리 설정 가이드

이 프로젝트를 GitHub에 업로드하기 위한 단계별 가이드입니다.

## 1. 로컬 Git 리포지토리 초기화

현재 프로젝트 폴더에서 다음 명령어를 실행하여 Git 리포지토리를 초기화합니다:

```bash
git init
```

## 2. 파일 스테이징 및 커밋

변경된 파일을 스테이징하고 첫 번째 커밋을 생성합니다:

```bash
# 모든 파일 스테이징
git add .

# 첫 번째 커밋 생성
git commit -m "Initial commit: Basic Shiny application structure"
```

## 3. GitHub 리포지토리 생성

1. GitHub 계정에 로그인합니다.
2. 오른쪽 상단의 '+' 아이콘을 클릭하고 'New repository'를 선택합니다.
3. 리포지토리 이름(예: 'alarm-shiny-app')을 입력합니다.
4. 선택적으로 설명을 추가합니다.
5. 리포지토리를 공개(Public) 또는 비공개(Private)로 설정합니다.
6. 'Initialize this repository with a README'는 체크하지 않습니다(이미 로컬에 README.md가 있음).
7. 'Create repository'를 클릭합니다.

## 4. 로컬 리포지토리를 GitHub에 연결

GitHub에서 제공하는 명령어를 사용하여 로컬 리포지토리를 원격 리포지토리에 연결합니다:

```bash
# GitHub 리포지토리를 원격 저장소로 추가
git remote add origin https://github.com/your-username/alarm-shiny-app.git

# 로컬 변경사항을 원격 저장소에 푸시
git push -u origin main  # 또는 git push -u origin master (Git 버전에 따라 다름)
```

## 5. 브랜칭 전략 설정 (권장)

향후 개발을 위한 브랜칭 전략을 설정합니다:

```bash
# 개발 브랜치 생성
git checkout -b develop

# 기능별 브랜치 예시 (필요시)
git checkout -b feature/dashboard-module
git checkout -b feature/master-data-module
```

## 6. 이슈 및 프로젝트 관리

1. GitHub의 Issues 기능을 사용하여 할 일과 버그를 추적합니다.
2. GitHub Projects 기능을 사용하여 칸반 보드 스타일로 작업을 관리합니다.
3. 풀 리퀘스트(PR)를 통해 코드 리뷰 프로세스를 구현합니다.

## 7. 자동화 설정 (선택 사항)

GitHub Actions를 사용하여 CI/CD 파이프라인을 설정할 수 있습니다:

1. `.github/workflows` 디렉토리 생성
2. Python 애플리케이션을 위한 워크플로우 YAML 파일 생성
3. 테스트, 린팅, 배포 등의 자동화 설정

---

이 가이드를 따라 설정하면 프로젝트가 GitHub에서 효과적으로 관리될 수 있으며, 협업 및 버전 관리가 용이해집니다. 