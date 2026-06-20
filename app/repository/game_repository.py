# app/repository/game_repository.py
from app.repository.base import IRepository, rows_to_dicts


class GameRepository(IRepository):
    """game 테이블 CRUD + 서비스 상태/장르별 조회 (Use Case 3.1, 3.5)"""

    def create_table(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS game (
                game_id       INTEGER PRIMARY KEY,
                dev_id        INTEGER REFERENCES developer(dev_id),
                title         VARCHAR(100) NOT NULL UNIQUE,
                genre         VARCHAR(50),
                platform      VARCHAR(50),
                release_date  DATE,
                status        VARCHAR(20) DEFAULT '운영중',
                closed_date   DATE,
                closed_reason TEXT,
                image_path    VARCHAR(255),
                description   TEXT
            )
        """)

    def get_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM game").fetchone()[0]

    def find_all(self) -> list[dict]:
        # Use Case 3.1: 게임 목록 조회 (개발사명 포함 LEFT JOIN)
        cur = self.conn.execute("""
            SELECT g.*, d.name AS dev_name
            FROM game g
            LEFT JOIN developer d ON g.dev_id = d.dev_id
            ORDER BY g.game_id
        """)
        return rows_to_dicts(cur)

    def find_by_id(self, id_: int) -> dict | None:
        cur = self.conn.execute("""
            SELECT g.*, d.name AS dev_name
            FROM game g
            LEFT JOIN developer d ON g.dev_id = d.dev_id
            WHERE g.game_id = ?
        """, [id_])
        rows = rows_to_dicts(cur)
        return rows[0] if rows else None

    def save(self, data: dict) -> int:
        new_id = self.conn.execute("SELECT COALESCE(MAX(game_id), 0) + 1 FROM game").fetchone()[0]
        self.conn.execute(
            """INSERT INTO game
               (game_id, dev_id, title, genre, platform, release_date,
                status, closed_date, closed_reason, image_path, description)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [new_id, data.get("dev_id"), data["title"], data.get("genre"),
             data.get("platform"), data.get("release_date"), data.get("status", "운영중"),
             data.get("closed_date"), data.get("closed_reason"),
             data.get("image_path"), data.get("description")],
        )
        return new_id

    def delete_by_id(self, id_: int) -> bool:
        self.conn.execute("DELETE FROM game WHERE game_id = ?", [id_])
        return True

    def find_by_keyword(self, keyword: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM game WHERE title ILIKE ?", [f"%{keyword}%"]
        )
        return rows_to_dicts(cur)

    def find_by_status(self, status: str) -> list[dict]:
        """Use Case 3.5: 운영중/종료 게임 구분 조회"""
        cur = self.conn.execute(
            "SELECT * FROM game WHERE status = ? ORDER BY title", [status]
        )
        return rows_to_dicts(cur)

    def update_status(self, game_id: int, status: str, closed_date=None) -> bool:
        self.conn.execute(
            "UPDATE game SET status = ?, closed_date = ? WHERE game_id = ?",
            [status, closed_date, game_id],
        )
        return True

    def find_by_genre(self, genre: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM game WHERE genre ILIKE ?", [f"%{genre}%"]
        )
        return rows_to_dicts(cur)
