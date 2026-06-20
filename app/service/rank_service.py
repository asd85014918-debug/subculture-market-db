# app/service/rank_service.py
from app.repository.rank_repository import RankRepository, DuplicateRankError


class RankService:
    """매출 순위 데이터 등록 비즈니스 로직 (Use Case 3.3)"""

    def __init__(self, rank_repo: RankRepository):
        self.rank_repo = rank_repo

    def insert_rank(self, game_id: int, year: int, month: int,
                     rank_position: int, store: str) -> dict:
        """입력값 검증 후 매출 순위를 저장한다."""
        if not (1 <= month <= 12):
            return {"success": False, "error_msg": "월(month)은 1~12 사이여야 합니다."}
        if rank_position < 1:
            return {"success": False, "error_msg": "순위는 1 이상이어야 합니다."}

        try:
            new_id = self.rank_repo.save({
                "game_id": game_id, "year": year, "month": month,
                "rank_position": rank_position, "store": store,
            })
            return {"success": True, "rank_id": new_id}
        except DuplicateRankError as e:
            return {"success": False, "error_msg": str(e)}
