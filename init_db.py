# init_db.py
"""SubcultureMarket DB 초기화 스크립트.

처음 한 번 실행하면 subculture.duckdb 파일을 생성하고
schema.sql(DDL) + sample_data.sql(기본 5개 게임) + 서비스 종료 사례(헤븐번즈 레드)를
적재한다. 이미 DB 파일이 있으면 삭제 후 새로 만든다.

사용법:
    python init_db.py
"""
import os
import duckdb

DB_PATH = os.path.join(os.path.dirname(__file__), "subculture.duckdb")


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"기존 DB 삭제: {DB_PATH}")

    con = duckdb.connect(DB_PATH)

    with open("schema.sql", encoding="utf-8") as f:
        con.execute(f.read())
    print("스키마(4개 테이블) 생성 완료")

    with open("sample_data.sql", encoding="utf-8") as f:
        con.execute(f.read())
    print("기본 샘플 데이터(5개 게임) 적재 완료")

    # v4 보강: 서비스 종료 사례(헤븐번즈 레드)를 추가하여
    # Use Case 3.1.7(서비스 현황 조회) 및 BM 유형별 비교 분석이 의미 있는 결과를 갖도록 함
    con.execute("""
        INSERT INTO developer VALUES
        (6, 'WFS / Yostar', '일본', 2018, 'imgs/developer/wfs.png')
    """)
    con.execute("""
        INSERT INTO game VALUES
        (6, 6, '헤븐번즈 레드', 'RPG/시뮬레이션', 'Android/iOS', '2022-02-17',
         '종료', '2025-03-31', 'BM 대비 신규 유입 부족으로 서비스 종료',
         'imgs/game/hbr.png', '스토리 중심 미연시형 RPG')
    """)
    con.execute("""
        INSERT INTO game_bm VALUES
        (6, 6, '패키지형', FALSE, NULL, NULL, NULL, FALSE, 0, 0, 90,
         'imgs/bm/hbr_bm.png', '가챠 없음, 완전 무과금')
    """)
    con.execute("""
        INSERT INTO revenue_rank VALUES
        (11, 6, 2025, 1, 45, 'Google Play'),
        (12, 4, 2025, 3, 10, 'Google Play')
    """)
    con.commit()
    print("서비스 종료 사례(헤븐번즈 레드) 보강 완료")

    count = con.execute("SELECT COUNT(*) FROM game").fetchone()[0]
    print(f"\n초기화 완료: game 테이블 {count}건. subculture.duckdb 생성됨.")
    con.close()


if __name__ == "__main__":
    main()
