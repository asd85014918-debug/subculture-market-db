# app/ui/rank_view.py
"""매출 순위 JOIN 조회 화면 (Use Case 3.1.6).

연도/월/스토어 필터로 4-table LEFT JOIN 결과를 ft.DataTable에 표시한다.
"""
import flet as ft
from app.ui.helpers import safe_update


class RankView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.year_dd = ft.Dropdown(
            label="연도", width=120, dense=True,
            options=[ft.dropdown.Option("2025"), ft.dropdown.Option("2026")],
            value="2025", on_select=lambda e: self.refresh(),
        )
        self.month_dd = ft.Dropdown(
            label="월", width=100, dense=True,
            options=[ft.dropdown.Option(str(m)) for m in range(1, 13)],
            value="1", on_select=lambda e: self.refresh(),
        )
        self.store_dd = ft.Dropdown(
            label="스토어", width=160, dense=True,
            options=[ft.dropdown.Option("Google Play"), ft.dropdown.Option("App Store")],
            value="Google Play", on_select=lambda e: self.refresh(),
        )
        self.table_area = ft.Column()

    def build(self):
        self.refresh()
        return ft.Column(
            [
                ft.Text("매출 순위 - JOIN 종합 조회", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("developer + game + game_bm + revenue_rank 4-table LEFT JOIN",
                        size=12, color=ft.Colors.GREY_700),
                ft.Row([self.year_dd, self.month_dd, self.store_dd]),
                ft.Divider(),
                self.table_area,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def refresh(self):
        year = int(self.year_dd.value)
        month = int(self.month_dd.value)
        store = self.store_dd.value
        rows = self.ctx.join_service.get_joined_rank(year, month, store, sort_by="rank")

        data_rows = []
        for r in rows:
            rank_text = f"{r['rank_position']}위" if r["rank_position"] is not None else "-"
            data_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["game_title"])),
                ft.DataCell(ft.Text(r["dev_name"] or "-")),
                ft.DataCell(ft.Text(r["bm_type"] or "-")),
                ft.DataCell(ft.Text(f"{r['bm_score']}점" if r["bm_score"] is not None else "-")),
                ft.DataCell(ft.Text(rank_text, weight=ft.FontWeight.BOLD,
                                     color=ft.Colors.INDIGO_700)),
            ]))

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("게임명")),
                ft.DataColumn(ft.Text("개발사")),
                ft.DataColumn(ft.Text("BM유형")),
                ft.DataColumn(ft.Text("친화도")),
                ft.DataColumn(ft.Text("순위")),
            ],
            rows=data_rows,
        )
        self.table_area.controls = [table] if data_rows else [
            ft.Text("해당 조건의 데이터가 없습니다.", color=ft.Colors.GREY_600)
        ]
        safe_update(self.table_area)
