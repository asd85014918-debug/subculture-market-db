# app/repository/rank_repository.py
import duckdb
from app.repository.base import IRepository, rows_to_dicts


class DuplicateRankError(Exception):
    """동일 (game_id, year, month, store) 조합이 이미 존재할 때 발생"""
    pass


class RankRepository(IRepository):
    """revenue_rank 테이블 CRUD (Use Case 3.3 매출 순위 데이터 삽입)"""

    def create_table(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS revenue_rank (
                rank_id       INTEGER PRIMARY KEY,
                game_id       INTEGER REFERENCES game(game_id),
                year          INTEGER NOT NULL,
                month         INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
                rank_position INTEGER,
                store         VARCHAR(20),
                UNIQUE(game_id, year, month, store)
            )
        """)

    def get_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM revenue_rank").fetchone()[0]

    def find_all(self) -> list[dict]:
        cur = self.conn.execute("SELECT * FROM revenue_rank ORDER BY year DESC, month DESC")
        return rows_to_dicts(cur)

    def find_by_id(self, id_: int) -> dict | None:
        cur = self.conn.execute("SELECT * FROM revenue_rank WHERE rank_id = ?", [id_])
        rows = rows_to_dicts(cur)
        return rows[0] if rows else None

    def save(self, data: dict) -> int:
        """신규 매출 순위 삽입. UNIQUE 제약 위반 시 DuplicateRankError 발생 (Use Case 3.3)"""
        new_id = self.conn.execute("SELECT COALESCE(MAX(rank_id), 0) + 1 FROM revenue_rank").fetchone()[0]
        try:
            self.conn.execute(
                "INSERT INTO revenue_rank VALUES (?, ?, ?, ?, ?, ?)",
                [new_id, data["game_id"], data["year"], data["month"],
                 data["rank_position"], data["store"]],
            )
        except duckdb.ConstraintException as e:
            raise DuplicateRankError(
                f"이미 등록된 데이터입니다: game_id={data['game_id']}, "
                f"{data['year']}-{data['month']:02d}, {data['store']}"
            ) from e
        return new_id

    def delete_by_id(self, id_: int) -> bool:
        self.conn.execute("DELETE FROM revenue_rank WHERE rank_id = ?", [id_])
        return True

    def find_by_keyword(self, keyword: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM revenue_rank WHERE store ILIKE ?", [f"%{keyword}%"]
        )
        return rows_to_dicts(cur)

    def find_by_game_and_period(self, game_id: int, year: int, month: int) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM revenue_rank WHERE game_id = ? AND year = ? AND month = ?",
            [game_id, year, month],
        )
        return rows_to_dicts(cur)

    def find_rank_history(self, game_id: int, limit: int = 12) -> list[dict]:
        """게임 상세 화면의 '최근 N개월 매출 순위' 조회 (Use Case 3.1.1)"""
        cur = self.conn.execute(
            """SELECT * FROM revenue_rank
               WHERE game_id = ?
               ORDER BY year DESC, month DESC
               LIMIT ?""",
            [game_id, limit],
        )
        return rows_to_dicts(cur)

    def find_top_n(self, year: int, month: int, store: str, n: int = 10) -> list[dict]:
        cur = self.conn.execute(
            """SELECT * FROM revenue_rank
               WHERE year = ? AND month = ? AND store = ?
               ORDER BY rank_position ASC LIMIT ?""",
            [year, month, store, n],
        )
        return rows_to_dicts(cur)
