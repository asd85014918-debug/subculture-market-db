# app/repository/bm_repository.py
from app.repository.base import IRepository, rows_to_dicts


class BmRepository(IRepository):
    """game_bm 테이블 CRUD + BM 특화 조회 (Use Case 3.2)"""

    def create_table(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS game_bm (
                bm_id         INTEGER PRIMARY KEY,
                game_id       INTEGER REFERENCES game(game_id) UNIQUE,
                bm_type       VARCHAR(30),
                has_gacha     BOOLEAN,
                top_grade     VARCHAR(10),
                top_prob      DECIMAL(5,3),
                pity_count    INTEGER,
                has_spark     BOOLEAN,
                monthly_pass  INTEGER,
                starter_pack  INTEGER,
                bm_score      SMALLINT,
                bm_image_path VARCHAR(255),
                note          TEXT
            )
        """)

    def get_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM game_bm").fetchone()[0]

    def find_all(self) -> list[dict]:
        # 가챠 친화도 점수 내림차순 (Use Case 3.2 목록 화면 요구사항)
        cur = self.conn.execute("""
            SELECT b.*, g.title
            FROM game_bm b
            JOIN game g ON b.game_id = g.game_id
            ORDER BY b.bm_score DESC
        """)
        return rows_to_dicts(cur)

    def find_by_id(self, id_: int) -> dict | None:
        cur = self.conn.execute("SELECT * FROM game_bm WHERE bm_id = ?", [id_])
        rows = rows_to_dicts(cur)
        return rows[0] if rows else None

    def save(self, data: dict) -> int:
        new_id = self.conn.execute("SELECT COALESCE(MAX(bm_id), 0) + 1 FROM game_bm").fetchone()[0]
        self.conn.execute(
            """INSERT INTO game_bm
               (bm_id, game_id, bm_type, has_gacha, top_grade, top_prob, pity_count,
                has_spark, monthly_pass, starter_pack, bm_score, bm_image_path, note)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [new_id, data["game_id"], data.get("bm_type"), data.get("has_gacha"),
             data.get("top_grade"), data.get("top_prob"), data.get("pity_count"),
             data.get("has_spark"), data.get("monthly_pass"), data.get("starter_pack"),
             data.get("bm_score"), data.get("bm_image_path"), data.get("note")],
        )
        return new_id

    def delete_by_id(self, id_: int) -> bool:
        self.conn.execute("DELETE FROM game_bm WHERE bm_id = ?", [id_])
        return True

    def find_by_keyword(self, keyword: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM game_bm WHERE note ILIKE ?", [f"%{keyword}%"]
        )
        return rows_to_dicts(cur)

    def find_bm_by_game_id(self, game_id: int) -> dict | None:
        """Use Case 3.2.1 BM 비교: game_id로 BM 상세 조회"""
        cur = self.conn.execute(
            "SELECT * FROM game_bm WHERE game_id = ?", [game_id]
        )
        rows = rows_to_dicts(cur)
        return rows[0] if rows else None

    def find_by_bm_type(self, bm_type: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM game_bm WHERE bm_type = ?", [bm_type]
        )
        return rows_to_dicts(cur)

    def update_bm_score(self, bm_id: int, score: int) -> bool:
        self.conn.execute(
            "UPDATE game_bm SET bm_score = ? WHERE bm_id = ?", [score, bm_id]
        )
        return True
