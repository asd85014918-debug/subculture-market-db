# app/service/game_service.py
from app.repository.game_repository import GameRepository
from app.repository.rank_repository import RankRepository
from app.repository.bm_repository import BmRepository


class GameService:
    """게임 목록/상세 조회 및 서비스 현황 관련 비즈니스 로직 (Use Case 3.1, 3.5)"""

    def __init__(self, game_repo: GameRepository, rank_repo: RankRepository, bm_repo: BmRepository):
        self.game_repo = game_repo
        self.rank_repo = rank_repo
        self.bm_repo = bm_repo

    def get_all_games(self, genre: str | None = None, status: str | None = None) -> list[dict]:
        """게임 목록 조회 (장르/서비스 상태 필터 지원)"""
        games = self.game_repo.find_all()
        if genre:
            games = [g for g in games if g.get("genre") and genre in g["genre"]]
        if status:
            games = [g for g in games if g.get("status") == status]
        return games

    def get_game_detail(self, game_id: int) -> dict | None:
        """게임 상세 + BM 요약 + 최근 3개월 매출 순위 (Use Case 3.1.1)"""
        game = self.game_repo.find_by_id(game_id)
        if game is None:
            return None
        game["bm_summary"] = self.bm_repo.find_bm_by_game_id(game_id)
        game["recent_ranks"] = self.rank_repo.find_rank_history(game_id, limit=3)
        return game

    def get_service_status(self) -> dict:
        """운영중 / 종료 게임을 구분하여 반환 (Use Case 3.5)"""
        return {
            "active": self.game_repo.find_by_status("운영중"),
            "closed": self.game_repo.find_by_status("종료"),
        }
