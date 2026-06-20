# app/service/join_service.py
from app.repository.join_repository import JoinRepository


class JoinService:
    """4-table JOIN 종합 조회 비즈니스 로직 (Use Case 3.4)"""

    def __init__(self, join_repo: JoinRepository):
        self.join_repo = join_repo

    def get_joined_rank(self, year: int, month: int, store: str, sort_by: str = "rank") -> list[dict]:
        rows = self.join_repo.find_with_bm_and_dev(year, month, store)
        if sort_by == "bm_score":
            rows.sort(key=lambda r: (r["bm_score"] is None, -(r["bm_score"] or 0)))
        return rows

    def get_bm_type_insight(self) -> list[dict]:
        """영상 핵심 분석: BM 유형별 평균 순위 vs 평균 친화도 상관관계"""
        return self.join_repo.stats_by_bm_type()
