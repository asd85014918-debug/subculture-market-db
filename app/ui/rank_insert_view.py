# app/ui/rank_insert_view.py
"""매출 순위 데이터 등록 화면 (Use Case 3.1.5).

게임/연도/월/순위/스토어를 입력받아 RankService.insert_rank()를 호출하고,
UNIQUE 제약 위반 시 '중복 데이터입니다' 오류를 SnackBar로 표시한다.
"""
import flet as ft
from app.ui.helpers import safe_update


class RankInsertView:
    def __init__(self, ctx, on_saved):
        self.ctx = ctx
        self.on_saved = on_saved

        games = self.ctx.game_repo.find_all()
        self.game_dd = ft.Dropdown(
            label="게임 선택", width=300,
            options=[ft.dropdown.Option(str(g["game_id"]), g["title"]) for g in games],
            value=str(games[0]["game_id"]) if games else None,
        )
        self.year_field = ft.TextField(label="연도", width=140, value="2025")
        self.month_field = ft.TextField(label="월", width=100, value="1")
        self.rank_field = ft.TextField(label="순위", width=300)
        self.store_dd = ft.Dropdown(
            label="스토어", width=300,
            options=[ft.dropdown.Option("Google Play"), ft.dropdown.Option("App Store")],
            value="Google Play",
        )
        self.error_text = ft.Text("", color=ft.Colors.RED, size=13)

    def build(self):
        self.error_text.value = ""
        return ft.Column(
            [
                ft.Text("매출 순위 데이터 등록", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("관리자 메뉴 - 신규 매출 순위를 등록합니다", size=12, color=ft.Colors.GREY_700),
                ft.Container(height=16),
                ft.Card(content=ft.Container(
                    padding=24, width=560,
                    content=ft.Column(
                        [
                            self.game_dd,
                            ft.Row([self.year_field, self.month_field]),
                            self.rank_field,
                            self.store_dd,
                            self.error_text,
                            ft.Row([
                                ft.ElevatedButton("등록", icon=ft.Icons.SAVE, on_click=self._submit),
                                ft.OutlinedButton("취소", on_click=self._reset),
                            ]),
                        ],
                        spacing=16,
                    ),
                )),
                ft.Container(
                    width=420,
                    bgcolor=ft.Colors.AMBER_50, border_radius=12, padding=16,
                    content=ft.Column([
                        ft.Text("신뢰성 - 중복 데이터 방지", weight=ft.FontWeight.BOLD,
                                color=ft.Colors.AMBER_900),
                        ft.Text(
                            "revenue_rank 테이블의 UNIQUE(game_id, year, month, store) "
                            "제약으로 동일 조합이 이미 존재하면 자동으로 등록이 거부되고 "
                            "'중복 데이터입니다' 오류가 화면에 표시됩니다.",
                            size=12, color=ft.Colors.AMBER_900,
                        ),
                    ]),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def _submit(self, e):
        self.error_text.value = ""
        try:
            game_id = int(self.game_dd.value)
            year = int(self.year_field.value)
            month = int(self.month_field.value)
            rank_position = int(self.rank_field.value)
            store = self.store_dd.value
        except (TypeError, ValueError):
            self.error_text.value = "연도/월/순위는 숫자로 입력해 주세요."
            safe_update(self.error_text)
            return

        result = self.ctx.rank_service.insert_rank(game_id, year, month, rank_position, store)
        if result["success"]:
            e.page.show_dialog(ft.SnackBar(ft.Text("등록 완료되었습니다."), bgcolor=ft.Colors.GREEN_700))
            self._reset(e)
            self.on_saved()
        else:
            self.error_text.value = result["error_msg"]
            safe_update(self.error_text)

    def _reset(self, e):
        self.rank_field.value = ""
        self.error_text.value = ""
        safe_update(self.rank_field)
        safe_update(self.error_text)
