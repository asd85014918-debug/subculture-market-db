# app/repository/developer_repository.py
from app.repository.base import IRepository, rows_to_dicts


class DeveloperRepository(IRepository):
    """developer 테이블 CRUD + 이미지 경로 업데이트"""

    def create_table(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS developer (
                dev_id        INTEGER PRIMARY KEY,
                name          VARCHAR(100) NOT NULL UNIQUE,
                country       VARCHAR(50),
                founded_year  INTEGER,
                image_path    VARCHAR(255)
            )
        """)

    def get_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM developer").fetchone()[0]

    def find_all(self) -> list[dict]:
        cur = self.conn.execute("SELECT * FROM developer ORDER BY dev_id")
        return rows_to_dicts(cur)

    def find_by_id(self, id_: int) -> dict | None:
        cur = self.conn.execute("SELECT * FROM developer WHERE dev_id = ?", [id_])
        rows = rows_to_dicts(cur)
        return rows[0] if rows else None

    def save(self, data: dict) -> int:
        new_id = self.conn.execute("SELECT COALESCE(MAX(dev_id), 0) + 1 FROM developer").fetchone()[0]
        self.conn.execute(
            "INSERT INTO developer VALUES (?, ?, ?, ?, ?)",
            [new_id, data["name"], data.get("country"), data.get("founded_year"), data.get("image_path")],
        )
        return new_id

    def delete_by_id(self, id_: int) -> bool:
        self.conn.execute("DELETE FROM developer WHERE dev_id = ?", [id_])
        return True

    def find_by_keyword(self, keyword: str) -> list[dict]:
        cur = self.conn.execute(
            "SELECT * FROM developer WHERE name ILIKE ?", [f"%{keyword}%"]
        )
        return rows_to_dicts(cur)

    def update_image_path(self, dev_id: int, path: str) -> bool:
        """개발사 로고 이미지 경로를 갱신한다."""
        self.conn.execute(
            "UPDATE developer SET image_path = ? WHERE dev_id = ?", [path, dev_id]
        )
        return True
