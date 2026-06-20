-- ============================================================
-- SubcultureMarket DB - 샘플 데이터 INSERT
-- ============================================================

-- developer 샘플 데이터
INSERT INTO developer VALUES
    (1, 'HoYoverse (miHoYo)', '중국', 2012, 'imgs/developer/hoyoverse.png'),
    (2, 'Kuro Games', '중국', 2014, 'imgs/developer/kuro.png'),
    (3, 'TYPE-MOON / Aniplex', '일본', 2000, 'imgs/developer/typemoon.png'),
    (4, 'Nexon Games', '한국', 2014, 'imgs/developer/nexon.png'),
    (5, 'Shift Up', '한국', 2013, 'imgs/developer/shiftup.png');

-- game 샘플 데이터
INSERT INTO game VALUES
    (1, 1, '원신', 'RPG/오픈월드', 'Android/iOS/PC/PS', '2020-09-28',
        '운영중', NULL, NULL, 'imgs/game/genshin.png', 'HoYoverse 대표 오픈월드 RPG'),
    (2, 2, '명조: 워더링 웨이브스', 'RPG/오픈월드', 'Android/iOS/PC', '2024-05-22',
        '운영중', NULL, NULL, 'imgs/game/wuwa.png', '원신 대항마 오픈월드 RPG'),
    (3, 3, 'Fate/Grand Order', 'RPG/턴제', 'Android/iOS', '2015-07-30',
        '운영중', NULL, NULL, 'imgs/game/fgo.png', 'TYPE-MOON IP 기반 수집형 RPG'),
    (4, 4, '블루 아카이브', 'RPG/전략', 'Android/iOS/PC', '2021-11-08',
        '운영중', NULL, NULL, 'imgs/game/bluearchive.png', '학원 배경 전술 RPG'),
    (5, 5, '니케: 승리의 여신', '슈팅/RPG', 'Android/iOS/PC', '2022-11-04',
        '운영중', NULL, NULL, 'imgs/game/nikke.png', '포스트아포칼립스 슈팅 RPG');

-- game_bm 샘플 데이터
-- bm_id, game_id, bm_type, has_gacha, top_grade, top_prob, pity, has_spark, monthly, starter, bm_score, bm_image_path, note
INSERT INTO game_bm VALUES
    (1, 1, '가챠형', TRUE,  '5성', 0.600, 90,   TRUE,  16900, 4900, 82, 'imgs/bm/genshin_bm.png', '소프트 파닙 90회, 확정 교환 없음'),
    (2, 2, '가챠형', TRUE,  '5성', 0.800, 80,   TRUE,  16900, 3900, 79, 'imgs/bm/wuwa_bm.png',    '100회 확정 교환 존재'),
    (3, 3, '가챠형', TRUE,  'SSR', 1.000, NULL, FALSE, 12000, NULL, 48, 'imgs/bm/fgo_bm.png',     '천장 없음, 연속 소환 보너스만'),
    (4, 4, '가챠형', TRUE,  'SS',  0.700, 200,  TRUE,  9900,  3300, 72, 'imgs/bm/ba_bm.png',      '200회 천장, 스파크 시스템'),
    (5, 5, '가챠형', TRUE,  'SSR', 4.000, 200,  TRUE,  9900,  2900, 78, 'imgs/bm/nikke_bm.png',   '일반 4% + 보장 시스템');

-- revenue_rank 샘플 데이터
INSERT INTO revenue_rank VALUES
    (1,  1, 2025, 1,  3,  'Google Play'),
    (2,  1, 2025, 2,  5,  'Google Play'),
    (3,  2, 2025, 1,  7,  'Google Play'),
    (4,  2, 2025, 2,  4,  'Google Play'),
    (5,  3, 2025, 1,  18, 'Google Play'),
    (6,  3, 2025, 2,  22, 'Google Play'),
    (7,  4, 2025, 1,  9,  'Google Play'),
    (8,  5, 2025, 1,  2,  'Google Play'),
    (9,  1, 2025, 1,  2,  'App Store'),
    (10, 3, 2025, 1,  6,  'App Store');
