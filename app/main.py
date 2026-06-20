# app/main.py
"""SubcultureMarket DB - Flet GUI 메인 진입점.

실행 방법:
    cd subdb
    python -m flet run app/main.py            # 데스크탑 창으로 실행
    python -m flet run app/main.py --web       # 웹 브라우저로 실행

NavigationRail로 5개 화면(게임 목록 / BM 비교 / 매출 순위 / 서비스 현황 / 데이터 등록)을
전환하는 2-패널(좌측 메뉴 + 우측 콘텐츠) 레이아웃이다.
"""
import os
import duckdb
import flet as ft

from app.repository.developer_repository import DeveloperRepository
from app.repository.game_repository import GameRepository
from app.repository.bm_repository import BmRepository
from app.repository.rank_repository import RankRepository
from app.repository.join_repository import JoinRepository
from app.service.game_service import GameService
from app.service.bm_service import BmService
from app.service.rank_service import RankService
from app.service.join_service import JoinService

from app.ui.game_list_view import GameListView
from app.ui.bm_compare_view import BmCompareView
from app.ui.rank_view import RankView
from app.ui.status_view import StatusView
from app.ui.rank_insert_view import RankInsertView

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "subculture.duckdb")


class AppContext:
    """모든 화면이 공유하는 Repository/Service 인스턴스 모음."""

    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn
        self.dev_repo = DeveloperRepository(conn)
        self.game_repo = GameRepository(conn)
        self.bm_repo = BmRepository(conn)
        self.rank_repo = RankRepository(conn)
        self.join_repo = JoinRepository(conn)

        self.game_service = GameService(self.game_repo, self.rank_repo, self.bm_repo)
        self.bm_service = BmService(self.bm_repo)
        self.rank_service = RankService(self.rank_repo)
        self.join_service = JoinService(self.join_repo)


def main(page: ft.Page):
    page.title = "SubcultureMarket DB"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.window.width = 1280
    page.window.height = 820
    page.padding = 0

    conn = duckdb.connect(DB_PATH)
    ctx = AppContext(conn)

    content_area = ft.Container(expand=True, padding=28, bgcolor=ft.Colors.GREY_50)

    views = {}

    def show(key: str):
        content_area.content = views[key].build()
        content_area.update()

    views["list"] = GameListView(ctx, on_compare=lambda a, b: open_compare(a, b))
    views["bm"] = BmCompareView(ctx)
    views["rank"] = RankView(ctx)
    views["status"] = StatusView(ctx)
    views["insert"] = RankInsertView(ctx, on_saved=lambda: show("rank"))

    def open_compare(game_id_a: int, game_id_b: int):
        views["bm"].preset(game_id_a, game_id_b)
        nav_rail.selected_index = 1
        show("bm")

    def on_nav_change(e: ft.Event[ft.NavigationRail]):
        keys = ["list", "bm", "rank", "status", "insert"]
        show(keys[e.control.selected_index])

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=ft.Colors.INDIGO_50,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.SPORTS_ESPORTS_OUTLINED,
                                          selected_icon=ft.Icons.SPORTS_ESPORTS,
                                          label="게임 목록"),
            ft.NavigationRailDestination(icon=ft.Icons.BALANCE_OUTLINED,
                                          selected_icon=ft.Icons.BALANCE,
                                          label="BM 비교"),
            ft.NavigationRailDestination(icon=ft.Icons.LEADERBOARD_OUTLINED,
                                          selected_icon=ft.Icons.LEADERBOARD,
                                          label="매출 순위"),
            ft.NavigationRailDestination(icon=ft.Icons.MONITOR_HEART_OUTLINED,
                                          selected_icon=ft.Icons.MONITOR_HEART,
                                          label="서비스 현황"),
            ft.NavigationRailDestination(icon=ft.Icons.ADD_BOX_OUTLINED,
                                          selected_icon=ft.Icons.ADD_BOX,
                                          label="데이터 등록"),
        ],
        on_change=on_nav_change,
    )

    show("list")

    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
            spacing=0,
        )
    )

    def on_close(e):
        conn.close()

    page.on_disconnect = on_close


if __name__ == "__main__":
    ft.run(main)
