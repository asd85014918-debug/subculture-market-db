"""Use Case별 동작 검증 + 콘솔 출력 데모.
실제 보고서 4장(구현)의 '실행 결과' 캡처 자료로 사용한다.
"""
import duckdb
from app.repository.developer_repository import DeveloperRepository
from app.repository.game_repository import GameRepository
from app.repository.bm_repository import BmRepository
from app.repository.rank_repository import RankRepository, DuplicateRankError
from app.repository.join_repository import JoinRepository
from app.service.game_service import GameService
from app.service.bm_service import BmService
from app.service.rank_service import RankService
from app.service.join_service import JoinService

conn = duckdb.connect("subculture.duckdb")

dev_repo = DeveloperRepository(conn)
game_repo = GameRepository(conn)
bm_repo = BmRepository(conn)
rank_repo = RankRepository(conn)
join_repo = JoinRepository(conn)

game_service = GameService(game_repo, rank_repo, bm_repo)
bm_service = BmService(bm_repo)
rank_service = RankService(rank_repo)
join_service = JoinService(join_repo)

def banner(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

# ---------------------------------------------------------------
banner("[Use Case 3.1] 게임 목록 조회")
games = game_service.get_all_games()
for g in games:
    print(f"  [{g['game_id']}] {g['title']:<20} | {g['genre']:<12} | {g['dev_name']:<20} | {g['status']}")

# ---------------------------------------------------------------
banner("[Use Case 3.1.1] 게임 상세 조회 (원신, game_id=1)")
detail = game_service.get_game_detail(1)
print(f"  제목       : {detail['title']}")
print(f"  개발사     : {detail['dev_name']}")
print(f"  장르       : {detail['genre']}")
print(f"  플랫폼     : {detail['platform']}")
print(f"  출시일     : {detail['release_date']}")
print(f"  서비스상태 : {detail['status']}")
print(f"  BM 친화도  : {detail['bm_summary']['bm_score']}점")
print(f"  최근 매출 순위:")
for r in detail['recent_ranks']:
    print(f"    - {r['year']}-{r['month']:02d} {r['store']}: {r['rank_position']}위")

# ---------------------------------------------------------------
banner("[Use Case 3.2] BM 정보 조회 (친화도 점수 내림차순)")
bm_list = bm_service.list_bm_by_score()
for b in bm_list:
    print(f"  {b['title']:<20} | {b['bm_type']} | 천장:{b['pity_count']} | 점수:{b['bm_score']}점")

# ---------------------------------------------------------------
banner("[Use Case 3.2.1] BM 비교 - 원신(1) vs Fate/Grand Order(3)")
cmp = bm_service.compare_bm(1, 3)
print(f"  {'항목':<14}{'원신':<20}{'Fate/Grand Order'}")
print(f"  {'BM 유형':<14}{cmp['bm_type'][0]:<20}{cmp['bm_type'][1]}")
print(f"  {'최고등급확률':<12}{str(cmp['top_prob'][0])+'%':<20}{str(cmp['top_prob'][1])+'%'}")
print(f"  {'천장':<14}{str(cmp['pity_count'][0]):<20}{cmp['pity_count'][1] or '없음'}")
print(f"  {'월정액':<14}{str(cmp['monthly_pass'][0]):<20}{cmp['monthly_pass'][1]}")
print(f"  {'친화도점수':<12}{str(cmp['bm_score'][0])+'점':<20}{str(cmp['bm_score'][1])+'점'}")
print(f"  -> 더 유저 친화적인 BM: 게임 {cmp['winner']} (원신)" if cmp['winner']=='A' else f"  -> 더 유저 친화적인 BM: 게임 {cmp['winner']}")

# ---------------------------------------------------------------
banner("[Use Case 3.3] 매출 순위 데이터 삽입 - 정상 케이스")
result = rank_service.insert_rank(game_id=4, year=2025, month=3, rank_position=10, store="Google Play")
print(f"  결과: {result}")

banner("[Use Case 3.3] 매출 순위 데이터 삽입 - 중복 케이스 (UNIQUE 제약 위반)")
result_dup = rank_service.insert_rank(game_id=1, year=2025, month=1, rank_position=3, store="Google Play")
print(f"  결과: {result_dup}")

# ---------------------------------------------------------------
banner("[Use Case 3.4] 4-table LEFT JOIN 종합 조회 (2025-01, Google Play)")
joined = join_service.get_joined_rank(2025, 1, "Google Play", sort_by="rank")
print(f"  {'게임명':<20}{'개발사':<20}{'BM유형':<10}{'친화도':<8}{'순위'}")
for r in joined:
    rank_str = str(r['rank_position']) if r['rank_position'] is not None else "-"
    print(f"  {r['game_title']:<20}{(r['dev_name'] or '-'):<20}{(r['bm_type'] or '-'):<10}{str(r['bm_score'] or '-'):<8}{rank_str}")

banner("[Use Case 3.4 부가] BM 유형별 평균 순위 vs 평균 친화도 (독성 BM 분석)")
insight = join_service.get_bm_type_insight()
for row in insight:
    print(f"  {row['bm_type']:<10} | 게임수:{row['game_count']} | 평균친화도:{row['avg_bm_score']}점 | 평균순위:{row['avg_rank']}위")

# ---------------------------------------------------------------
banner("[Use Case 3.5] 서비스 현황 조회 (운영중 / 종료)")
status = game_service.get_service_status()
print(f"  운영중: {len(status['active'])}개 -> {[g['title'] for g in status['active']]}")
print(f"  종료  : {len(status['closed'])}개 -> {[g['title'] for g in status['closed']]}")

conn.close()
print("\n[전체 Use Case 데모 정상 종료]")
