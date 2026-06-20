-- ============================================================
-- SubcultureMarket DB - Logical Design DDL
-- 작성자: OH CHAEHUN | 담당교수: 오병우
-- DBMS: DuckDB 1.x
-- ============================================================

-- ① developer : 개발사/퍼블리셔 테이블 (Entity)
CREATE TABLE developer (
    dev_id        INTEGER PRIMARY KEY,
    name          VARCHAR(100) NOT NULL UNIQUE,  -- 개발사명
    country       VARCHAR(50),                   -- 국가
    founded_year  INTEGER,                       -- 설립연도
    image_path    VARCHAR(255)                   -- 개발사 로고 이미지 경로
);

-- ② game : 게임 타이틀 테이블 (Entity, developer 참조 N:1)
CREATE TABLE game (
    game_id       INTEGER PRIMARY KEY,
    dev_id        INTEGER REFERENCES developer(dev_id),
    title         VARCHAR(100) NOT NULL UNIQUE,
    genre         VARCHAR(50),                   -- 장르 (RPG/전략/슈팅)
    platform      VARCHAR(50),                   -- 플랫폼
    release_date  DATE,                          -- 출시일
    status        VARCHAR(20) DEFAULT '운영중',  -- 운영중/종료
    closed_date   DATE,                          -- 서비스 종료일
    closed_reason TEXT,                          -- 종료 사유 (BM 실패 등)
    image_path    VARCHAR(255),                  -- 게임 키비주얼 이미지 경로
    description   TEXT
);

-- ③ game_bm : 게임 BM 정보 테이블 (Relationship, game과 1:1)
-- 영상 핵심: '신작 출시 시 유저들이 즉시 비교하는 항목'을 컬럼화
CREATE TABLE game_bm (
    bm_id         INTEGER PRIMARY KEY,
    game_id       INTEGER REFERENCES game(game_id) UNIQUE,
    bm_type       VARCHAR(30),    -- 가챠형/패키지형/배틀패스형/혼합형
    has_gacha     BOOLEAN,        -- 가챠 유무
    top_grade     VARCHAR(10),    -- 최고 등급명 (5성, SSR, SS 등)
    top_prob      DECIMAL(5,3),   -- 최고 등급 확률(%) - 비교 핵심
    pity_count    INTEGER,        -- 천장 횟수 - 비교 핵심
    has_spark     BOOLEAN,        -- 스파크(확정 교환) 유무
    monthly_pass  INTEGER,        -- 월정액 가격(원), NULL=없음
    starter_pack  INTEGER,        -- 스타터 패키지 가격(원)
    -- bm_score 산출식: CLAMP(100 - (300/pity)*20 - (1/top_prob)*5 + has_spark*10, 0, 100)
    bm_score      SMALLINT,       -- BM 유저 친화도 점수 (0~100)
    bm_image_path VARCHAR(255),   -- BM 요약 카드 이미지 경로
    note          TEXT
);

-- ④ revenue_rank : 월별 매출 순위 테이블 (Relationship, game과 N:1)
CREATE TABLE revenue_rank (
    rank_id       INTEGER PRIMARY KEY,
    game_id       INTEGER REFERENCES game(game_id),
    year          INTEGER NOT NULL,
    month         INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    rank_position INTEGER,        -- 해당 월 순위
    store         VARCHAR(20),    -- Google Play / App Store
    UNIQUE(game_id, year, month, store)
);
