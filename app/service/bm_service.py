# app/service/bm_service.py
from app.repository.bm_repository import BmRepository


class BmService:
    """BM(비즈니스 모델) 비교 및 BM 유저 친화도 점수 산출 (Use Case 3.2)"""

    def __init__(self, bm_repo: BmRepository):
        self.bm_repo = bm_repo

    @staticmethod
    def calc_bm_score(bm: dict) -> int:
        """BM 유저 친화도 점수 산출 공식.

        점수 = 100
               - (천장이 낮을수록 가산되는 페널티: (300/pity)*20)
               - (최고 등급 확률이 낮을수록 가산되는 페널티: (1/top_prob)*5)
               + (확정 교환(스파크) 보유 시 +10)
        0~100 사이로 CLAMP한다. 천장이 없는 경우(pity_count IS NULL)는
        '사실상 무한 천장'으로 간주하여 최대 페널티를 적용한다.
        """
        pity = bm.get("pity_count")
        top_prob = float(bm.get("top_prob") or 0.1)
        has_spark = bool(bm.get("has_spark"))

        if pity:
            pity_penalty = (300 / pity) * 20
        else:
            pity_penalty = 60  # 천장 없음 -> 최대 페널티

        prob_penalty = (1 / top_prob) * 5 if top_prob > 0 else 50
        spark_bonus = 10 if has_spark else 0

        score = 100 - pity_penalty - prob_penalty + spark_bonus
        return max(0, min(100, round(score)))

    def compare_bm(self, game_id_a: int, game_id_b: int) -> dict:
        """두 게임의 BM을 항목별로 비교한다 (Use Case 3.2.1)"""
        bm_a = self.bm_repo.find_bm_by_game_id(game_id_a)
        bm_b = self.bm_repo.find_bm_by_game_id(game_id_b)
        if bm_a is None or bm_b is None:
            raise ValueError("BM 정보가 없는 게임입니다.")

        # 저장된 bm_score가 없으면 즉시 계산
        bm_a["bm_score"] = bm_a.get("bm_score") or self.calc_bm_score(bm_a)
        bm_b["bm_score"] = bm_b.get("bm_score") or self.calc_bm_score(bm_b)

        return {
            "bm_type":      (bm_a["bm_type"], bm_b["bm_type"]),
            "top_prob":     (bm_a["top_prob"], bm_b["top_prob"]),
            "pity_count":   (bm_a["pity_count"], bm_b["pity_count"]),
            "monthly_pass": (bm_a["monthly_pass"], bm_b["monthly_pass"]),
            "bm_score":     (bm_a["bm_score"], bm_b["bm_score"]),
            "winner": "A" if bm_a["bm_score"] >= bm_b["bm_score"] else "B",
        }

    def list_bm_by_score(self, bm_type: str | None = None) -> list[dict]:
        """BM 친화도 점수 내림차순 목록 (BM 유형 필터 지원)"""
        rows = self.bm_repo.find_all()
        if bm_type:
            rows = [r for r in rows if r.get("bm_type") == bm_type]
        return rows
