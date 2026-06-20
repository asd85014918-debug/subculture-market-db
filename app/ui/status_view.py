# app/ui/status_view.py
"""서비스 현황 화면 (Use Case 3.1.7).

운영중 게임과 서비스 종료 게임을 2-컬럼으로 구분하여 표시한다.
"""
import flet as ft
from app.ui.helpers import safe_update


class StatusView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.area = ft.Row(spacing=24, vertical_alignment=ft.CrossAxisAlignment.START)

    def build(self):
        self.refresh()
        return ft.Column(
            [
                ft.Text("서비스 현황", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("운영중인 게임과 서비스 종료 게임을 구분하여 표시합니다",
                        size=12, color=ft.Colors.GREY_700),
                ft.Divider(),
                self.area,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh(self):
        status = self.ctx.game_service.get_service_status()
        last_rank_rows = {r["game_id"]: r for r in self.ctx.join_repo.find_all_with_last_rank()}

        active_cards = [
            ft.Card(content=ft.Container(
                padding=12,
                content=ft.Row([ft.Icon(ft.Icons.CIRCLE, size=10, color=ft.Colors.GREEN),
                                 ft.Text(g["title"])]),
            )) for g in status["active"]
        ]
        closed_cards = []
        for g in status["closed"]:
            info = last_rank_rows.get(g["game_id"], {})
            closed_cards.append(ft.Card(content=ft.Container(
                padding=12,
                content=ft.Column([
                    ft.Row([ft.Icon(ft.Icons.CIRCLE, size=10, color=ft.Colors.RED),
                            ft.Text(g["title"], weight=ft.FontWeight.BOLD)]),
                    ft.Text(f"종료일: {g.get('closed_date','-')}", size=12, color=ft.Colors.GREY_700),
                    ft.Text(f"마지막 순위: {info.get('last_rank','-')}위", size=12, color=ft.Colors.GREY_700),
                ]),
            )))

        self.area.controls = [
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Container(ft.Text(f"운영중 ({len(active_cards)})", weight=ft.FontWeight.BOLD,
                                          color=ft.Colors.GREEN_800),
                                  bgcolor=ft.Colors.GREEN_50, padding=10, border_radius=8),
                    *active_cards,
                ], spacing=8),
            ),
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Container(ft.Text(f"서비스 종료 ({len(closed_cards)})", weight=ft.FontWeight.BOLD,
                                          color=ft.Colors.RED_800),
                                  bgcolor=ft.Colors.RED_50, padding=10, border_radius=8),
                    *closed_cards,
                ], spacing=8),
            ),
        ]
        safe_update(self.area)
