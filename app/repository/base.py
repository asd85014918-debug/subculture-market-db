# app/repository/base.py
"""모든 Repository가 구현해야 하는 공통 인터페이스.

DuckDB 커넥션을 주입받아 각 테이블에 대한 CRUD 및 검색 기능을
표준화된 형태로 제공한다.
"""
from abc import ABC, abstractmethod


class IRepository(ABC):
    """Repository 공통 추상 클래스 (테이블 4개가 동일 구조를 따름)"""

    def __init__(self, conn):
        self.conn = conn  # duckdb.DuckDBPyConnection

    @abstractmethod
    def create_table(self) -> None:
        """테이블이 없을 경우 생성한다."""
        ...

    @abstractmethod
    def get_count(self) -> int:
        """테이블의 전체 레코드 수를 반환한다."""
        ...

    @abstractmethod
    def find_all(self) -> list[dict]:
        """전체 레코드를 list[dict] 형태로 반환한다."""
        ...

    @abstractmethod
    def find_by_id(self, id_: int) -> dict | None:
        """PK로 단일 레코드를 조회한다. 없으면 None."""
        ...

    @abstractmethod
    def save(self, data: dict) -> int:
        """신규 레코드를 저장하고 PK를 반환한다."""
        ...

    @abstractmethod
    def delete_by_id(self, id_: int) -> bool:
        """PK로 레코드를 삭제한다. 성공 시 True."""
        ...

    @abstractmethod
    def find_by_keyword(self, keyword: str) -> list[dict]:
        """이름/제목 등에 keyword가 포함된 레코드를 검색한다."""
        ...


def rows_to_dicts(cursor) -> list[dict]:
    """duckdb cursor 실행 결과를 list[dict]로 변환하는 헬퍼."""
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]
