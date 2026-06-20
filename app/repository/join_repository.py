# app/repository/join_repository.py
from app.repository.base import rows_to_dicts


class JoinRepository:
    """4-table LEFT JOIN 전용 Repository - Use Case 3.4, 3.5"""

    def __init__(self, conn):
        self.conn = conn

    def find_with_bm_and_dev(self, year: int, month: int, store: str) -> list[dict]:
        """game + developer + game_bm + revenue_rank 4-table LEFT JOIN
        (Use Case 3.4: 특정 월 순위 상위 게임의 BM 정보 종합 조회)
        """
        cur = self.conn.execute(
            """
            SELECT
                g.title          AS game_title,
                d.name           AS dev_name,
                b.bm_type        AS bm_type,
                b.bm_score       AS bm_score,
                r.rank_position  AS rank_position,
                r.year           AS year,
                r.month          AS month,
                r.store          AS store
            FROM game g
            LEFT JOIN developer    d ON g.dev_id  = d.dev_id
            LEFT JOIN game_bm      b ON g.game_id = b.game_id
            LEFT JOIN revenue_rank r ON g.game_id = r.game_id
                AND r.year = ? AND r.month = ? AND r.store = ?
            ORDER BY r.rank_position ASC NULLS LAST
            """,
            [year, month, store],
        )
        return rows_to_dicts(cur)

    def stats_by_bm_type(self) -> list[dict]:
        """BM 유형별 평균 순위·평균 친화도 집계 - 영상 '독성 BM 분석' 대응"""
        cur = self.conn.execute(
            """
            SELECT
                b.bm_type,
                COUNT(DISTINCT g.game_id)     AS game_count,
                ROUND(AVG(b.bm_score), 1)     AS avg_bm_score,
                ROUND(AVG(r.rank_position), 1) AS avg_rank
            FROM game g
            JOIN game_bm b      ON g.game_id = b.game_id
            LEFT JOIN revenue_rank r ON g.game_id = r.game_id
            GROUP BY b.bm_type
            ORDER BY avg_bm_score DESC
            """
        )
        return rows_to_dicts(cur)

    def find_all_with_last_rank(self) -> list[dict]:
        """game + revenue_rank - 서비스 현황 + 마지막 순위 (Use Case 3.5)"""
        cur = self.conn.execute(
            """
            SELECT
                g.game_id,
                g.title,
                g.status,
                g.closed_date,
                MAX(r.rank_position) AS last_rank
            FROM game g
            LEFT JOIN revenue_rank r ON g.game_id = r.game_id
            GROUP BY g.game_id, g.title, g.status, g.closed_date
            ORDER BY g.status, g.title
            """
        )
        return rows_to_dicts(cur)
