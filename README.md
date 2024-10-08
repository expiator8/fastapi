# 프로젝트 구조

## 폴더 구조

```bash
project/
│
├── api/
│   └── v1/
│       ├── models/
│       │   └── app_name.py
│       ├── routes/
│       │   ├── __init__.py
│       │   └── app_name.py
│       ├── service/
│       │   └── app_name.py
│       └── __init__.py
│ 
├── core
│   ├── entity/
│   ├── modules/
│   ├── repository/
│   ├── database.py
│   ├── enums.py.py
│   └── utils.py
│
├── logs/
│   ├── access.log
│   └── error.log
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── tests/
├── .env
├── .gitignore
├── alembic.ini
├── config.py
├── LICENSE
├── main.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## 역할

1. api/: API 관련 코드
    - v1/: API 버전별 디렉토리
        - models/: 데이터 모델 정의 파일 디렉토리
            - app_name.py: 특정 애플리케이션, 기능별 model. e.g. users
        - router/: FastAPI 라우터 정의.엔드포인트 설정 파일 디렉토리
            - __init__.py: 전체 애플리케이션 api router 정의
            - app_name.py: 특정 애플리케이션, 기능별 router. e.g. users
        - service/: 비즈니스 로직 파일 디렉토리
            - app_name.py: 특정 애플리케이션, 기능별 service. e.g. users
2. core/
    - entity/: 데이터베이스 엔티티 정의
    - modules/: 외부 모듈 관리 디렉토리. e.g. oauth, email
    - repository/: 데이터베이스와 상호작용 담당. e.g. crud, filter, exclude
    - database.py: 데이터베이스 연결 및 세션 관리 설정
    - enums.py:  열거형(enum) 타입 정의
    - utils.py: 유틸리티 함수 정의
3. logs/
    - access.log: api access log 저장
    - error.log: 경고, 에러 log 저장
4. migrations/: Alembic 데이터베이스 마이그레이션 파일 관리 디렉토리
    - versions/: 버전별 마이그레이션 스크립트 파일 디렉토리
    - env.py: 마이그레이션 설정, 동작 정의
    - README: Alembic 사용법 설명
    - script.py.mako: 마이그레이션 스크립트 생성에 사용되는 템플릿 파일
5. tests/: 테스트 코드 관리 디렉토리
6. .env: 환경 변수 관리
7. .gitignore: Git에 업로드하지 않을 파일 및 디렉토리 명시
8. alembic.ini: Alembic 기본 설정 파일. 전역 설정 정의. e.g. 데이터베이스 URL
9. config.py: 프로젝트 설정 정의. e.g. celery
10. main.py: FastAPI 애플리케이션 실행 파일. 프로젝트에서 사용하는 에플리케이션 라우터 관리
11. poetry.lock: 패키지 의존성 버전 고정
12. pyproject.toml: 패키지 빌드 설정 관리
