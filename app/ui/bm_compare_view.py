# app/ui/bm_compare_view.py
"""BM 상세 비교 화면 (Use Case 3.1.4).

두 게임을 드롭다운으로 선택하면 ft.DataTable로 BM 항목을 나란히 비교하고,
친화도 점수가 더 높은 쪽 셀을 초록색, 낮은 쪽을 빨간색으로 강조한다.
"""
import flet as ft
from app.ui.helpers import safe_update


class BmCompareView:
    def __init__(self, ctx):
        self.ctx = ctx
        games = self.ctx.game_repo.find_all()
        self.options = [ft.dropdown.Option(str(g["game_id"]), g["title"]) for g in games]

        self.dd_a = ft.Dropdown(label="게임 A", width=240, options=self.options,
                                 on_select=lambda e: self._render())
        self.dd_b = ft.Dropdown(label="게임 B", width=240, options=self.options,
                                 on_select=lambda e: self._render())
        self.result_area = ft.Column()

        if len(games) >= 2:
            self.dd_a.value = str(games[0]["game_id"])
            self.dd_b.value = str(games[2]["game_id"] if len(games) > 2 else games[1]["game_id"])

    def preset(self, game_id_a: int, game_id_b: int):
        self.dd_a.value = str(game_id_a)
        self.dd_b.value = str(game_id_b)

    def build(self):
        self._render()
        return ft.Column(
            [
                ft.Text("BM 상세 비교", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("두 게임을 선택하면 BM 항목을 나란히 비교합니다", size=13, color=ft.Colors.GREY_700),
                ft.Row([self.dd_a, self.dd_b,
                        ft.ElevatedButton("비교하기", icon=ft.Icons.COMPARE_ARROWS,
                                           on_click=lambda e: self._render())]),
                ft.Divider(),
                self.result_area,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def _render(self):
        if not self.dd_a.value or not self.dd_b.value:
            return
        gid_a, gid_b = int(self.dd_a.value), int(self.dd_b.value)
        if gid_a == gid_b:
            self.result_area.controls = [ft.Text("서로 다른 두 게임을 선택해 주세요.", color=ft.Colors.RED)]
            safe_update(self.result_area)
            return

        try:
            cmp = self.ctx.bm_service.compare_bm(gid_a, gid_b)
        except ValueError as e:
            self.result_area.controls = [ft.Text(str(e), color=ft.Colors.RED)]
            safe_update(self.result_area)
            return

        game_a = self.ctx.game_repo.find_by_id(gid_a)
        game_b = self.ctx.game_repo.find_by_id(gid_b)

        def cell(value, highlight=None):
            color = None
            if highlight == "win":
                color = ft.Colors.GREEN_50
            elif highlight == "lose":
                color = ft.Colors.RED_50
            return ft.DataCell(
                ft.Container(ft.Text(str(value)), bgcolor=color,
                              padding=6, border_radius=6, alignment=ft.Alignment(0, 0))
            )

        winner = cmp["winner"]
        score_a, score_b = cmp["bm_score"]

        rows = [
            ("BM 유형", cmp["bm_type"][0], cmp["bm_type"][1], None),
            ("최고 등급 확률", f"{cmp['top_prob'][0]}%", f"{cmp['top_prob'][1]}%", None),
            ("천장 (Pity)", cmp["pity_count"][0] or "없음", cmp["pity_count"][1] or "없음", None),
            ("월정액", cmp["monthly_pass"][0], cmp["monthly_pass"][1], None),
            ("BM 유저 친화 점수", f"{score_a}점", f"{score_b}점", "score"),
        ]

        data_rows = []
        for label, va, vb, kind in rows:
            if kind == "score":
                ha = "win" if winner == "A" else "lose"
                hb = "win" if winner == "B" else "lose"
            else:
                ha = hb = None
            data_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(label, weight=ft.FontWeight.BOLD)),
                cell(va, ha),
                cell(vb, hb),
            ]))

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("BM 항목")),
                ft.DataColumn(ft.Text(game_a["title"])),
                ft.DataColumn(ft.Text(game_b["title"])),
            ],
            rows=data_rows,
            column_spacing=40,
        )

        self.result_area.controls = [table]
        safe_update(self.result_area)
