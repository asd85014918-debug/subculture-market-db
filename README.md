# SubcultureMarket DB

데이터베이스 Term Project — 모바일 서브컬처 게임의 BM(비즈니스 모델)과
매출 순위 데이터를 DuckDB에 통합하고 Flet GUI로 비교·분석하는 애플리케이션.

유튜브 영상 「신작 서브컬처 게임이 점점 살아남기 힘들어지는 이유」가 제기한
"신작 출시 시 유저들이 기존 게임의 가챠 확률·천장·과금 구조와 즉시 비교한다"는
문제의식을, 원신·명조·Fate/Grand Order·블루 아카이브·니케·헤븐번즈 레드(서비스 종료)
6개 게임의 실제 BM/매출 데이터로 구체화하였다.

## 기술 스택

- **DB**: DuckDB (로컬 파일 기반, 서버 불필요)
- **GUI**: Flet (Flutter 기반 Python GUI 프레임워크)
- **언어**: Python 3.11+ (Repository / Service 계층 분리)

## 스키마

| 테이블 | 유형 | 설명 |
|---|---|---|
| `developer` | Entity | 개발사 정보 (로고 이미지 경로 포함) |
| `game` | Entity | 게임 타이틀 정보 (developer 참조 N:1, 키비주얼 이미지 경로 포함) |
| `game_bm` | Relationship | 게임별 BM 상세 (game과 1:1) — 가챠 확률·천장·월정액 등 |
| `revenue_rank` | Relationship | 게임별 월간 매출 순위 (game과 N:1) — UNIQUE 제약으로 중복 방지 |

ERD는 `docs/erd_diagram.jpg` (VSCode ERD Editor, Crow's Feet 표기법) 참고.

## 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. DB 초기화 (최초 1회, 또는 데이터를 리셋하고 싶을 때)
python init_db.py

# 3. Flet 앱 실행 (데스크탑 창)
python -m flet run app/main.py

# 또는 웹 브라우저로 실행
python -m flet run app/main.py --web
```

## 화면 구성

좌측 NavigationRail + 우측 콘텐츠의 2-패널 구조이며, 5개 화면을 제공한다.

1. **게임 목록** — 카드형 목록, 검색/필터, 게임별 image_path를 `ft.Image`로 출력
2. **BM 비교** — 두 게임의 BM 항목을 `ft.DataTable`로 비교, 친화도 높은 쪽 강조
3. **매출 순위** — `developer + game + game_bm + revenue_rank` 4-table LEFT JOIN 결과
4. **서비스 현황** — 운영중/종료 게임 구분, 종료 게임은 종료일·마지막 순위 표시
5. **데이터 등록** — 매출 순위 신규 등록, UNIQUE 제약 위반 시 오류 메시지 표시

## Use Case 실행 결과 (콘솔 데모)

GUI 없이 Repository/Service 계층만 단독으로 검증하려면:

```bash
python run_usecase_demo.py
```

7개 Use Case(목록 조회, 상세 조회, BM 조회, BM 비교, 매출 순위 삽입(정상/중복),
JOIN 조회, 서비스 현황 조회)가 순차 실행되며 콘솔에 결과가 출력된다.

## 프로젝트 구조

```
app/
  main.py                  # Flet 앱 진입점 (NavigationRail 라우팅)
  repository/               # DuckDB 접근 계층 (5개: Developer/Game/Bm/Rank/Join)
  service/                  # 비즈니스 로직 계층 (BM 점수 산출 등)
  ui/                       # Flet 화면 5개
schema.sql                  # DDL
sample_data.sql              # 기본 샘플 데이터 (5개 게임)
init_db.py                   # DB 초기화 스크립트 (schema + sample + 종료 사례 보강)
run_usecase_demo.py          # Use Case 통합 콘솔 데모
imgs/                        # 게임 키비주얼 / 개발사 로고 이미지
```

## 담당교수

컴퓨터공학전공 오병우 교수
