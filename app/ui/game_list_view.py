# app/ui/game_list_view.py
"""게임 목록 / 상세 화면 (Use Case 3.1.1, 3.1.2).

검색·필터, 카드 목록, image_path 기반 이미지 출력, 게임 클릭 시 상세 패널,
2개 게임 체크 후 BM 비교 화면으로 이동하는 기능을 제공한다.
"""
import os
import flet as ft
from app.ui.helpers import safe_update


def _image_or_placeholder(image_path: str | None, size: int = 56):
    """game.image_path가 실제 파일로 존재하면 ft.Image, 아니면 placeholder 아이콘을 반환한다."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    full_path = os.path.join(base_dir, image_path) if image_path else None
    if full_path and os.path.exists(full_path):
        return ft.Image(src=full_path, width=size, height=size, fit=ft.BoxFit.COVER,
                         border_radius=10)
    return ft.Container(
        width=size, height=size, border_radius=10, bgcolor=ft.Colors.INDIGO_200,
        alignment=ft.Alignment(0, 0),
        content=ft.Icon(ft.Icons.SPORTS_ESPORTS, color=ft.Colors.WHITE, size=size * 0.5),
    )


class GameListView:
    def __init__(self, ctx, on_compare):
        self.ctx = ctx
        self.on_compare = on_compare
        self.selected: set[int] = set()
        self.detail_container = ft.Container()
        self.list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        self.search_field = ft.TextField(
            label="검색: 게임 제목", width=240, dense=True,
            on_submit=lambda e: self.refresh(),
        )
        self.genre_filter = ft.Dropdown(
            label="장르", width=160, dense=True,
            options=[ft.dropdown.Option("전체")] + [
                ft.dropdown.Option(g) for g in
                ["RPG/오픈월드", "RPG/턴제", "RPG/전략", "슈팅/RPG", "RPG/시뮬레이션"]
            ],
            value="전체",
            on_select=lambda e: self.refresh(),
        )
        self.status_filter = ft.Dropdown(
            label="서비스 상태", width=160, dense=True,
            options=[ft.dropdown.Option("전체"), ft.dropdown.Option("운영중"), ft.dropdown.Option("종료")],
            value="전체",
            on_select=lambda e: self.refresh(),
        )
        self.compare_btn = ft.ElevatedButton(
            "선택한 게임 BM 비교하기", icon=ft.Icons.COMPARE_ARROWS,
            disabled=True, on_click=self._on_compare_click,
        )

    def build(self):
        self.refresh()
        return ft.Column(
            [
                ft.Text("게임 목록", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.search_field, self.genre_filter, self.status_filter]),
                ft.Divider(),
                ft.Row(
                    [
                        ft.Container(self.list_container, expand=2),
                        ft.VerticalDivider(width=1),
                        ft.Container(self.detail_container, expand=1),
                    ],
                    expand=True,
                ),
                ft.Row([self.compare_btn], alignment=ft.MainAxisAlignment.END),
            ],
            expand=True,
        )

    def refresh(self):
        genre = None if self.genre_filter.value == "전체" else self.genre_filter.value
        status = None if self.status_filter.value == "전체" else self.status_filter.value
        games = self.ctx.game_service.get_all_games(genre=genre, status=status)

        keyword = (self.search_field.value or "").strip()
        if keyword:
            games = [g for g in games if keyword in g["title"]]

        self.list_container.controls = [self._game_card(g) for g in games]
        safe_update(self.list_container)

    def _game_card(self, g: dict):
        gid = g["game_id"]
        score = None
        bm = self.ctx.bm_repo.find_bm_by_game_id(gid)
        if bm:
            score = bm.get("bm_score")
        score_color = ft.Colors.GREEN_700 if (score or 0) >= 80 else (
            ft.Colors.AMBER_800 if (score or 0) >= 65 else ft.Colors.RED_700)

        checkbox = ft.Checkbox(value=gid in self.selected, on_change=lambda e: self._toggle(gid, e))

        return ft.Card(
            content=ft.Container(
                padding=12,
                on_click=lambda e, gid=gid: self._show_detail(gid),
                content=ft.Row(
                    [
                        checkbox,
                        _image_or_placeholder(g.get("image_path")),
                        ft.Column(
                            [
                                ft.Text(g["title"], size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{g.get('genre','-')}  ·  {g.get('dev_name','-')}",
                                        size=12, color=ft.Colors.GREY_700),
                                ft.Container(
                                    ft.Text(g.get("status", "-"), size=11, color=ft.Colors.GREEN_800),
                                    bgcolor=ft.Colors.GREEN_50,
                                    padding=ft.Padding.symmetric(vertical=4, horizontal=8),
                                    border_radius=10,
                                ),
                            ],
                            expand=True, spacing=4,
                        ),
                        ft.Column(
                            [
                                ft.Text("BM 친화도", size=11, color=ft.Colors.GREY_600),
                                ft.Text(f"{score}점" if score is not None else "-",
                                        size=20, weight=ft.FontWeight.BOLD, color=score_color),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ),
        )

    def _toggle(self, gid: int, e):
        if e.control.value:
            self.selected.add(gid)
        else:
            self.selected.discard(gid)
        self.compare_btn.disabled = len(self.selected) != 2
        safe_update(self.compare_btn)

    def _on_compare_click(self, e):
        ids = list(self.selected)
        if len(ids) == 2:
            self.on_compare(ids[0], ids[1])

    def _show_detail(self, game_id: int):
        detail = self.ctx.game_service.get_game_detail(game_id)
        if detail is None:
            return
        bm = detail.get("bm_summary") or {}
        ranks = detail.get("recent_ranks") or []

        self.detail_container.content = ft.Column(
            [
                ft.Row([_image_or_placeholder(detail.get("image_path"), size=72)]),
                ft.Text(detail["title"], size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"개발사: {detail.get('dev_name','-')}", size=13),
                ft.Text(f"장르: {detail.get('genre','-')}", size=13),
                ft.Text(f"플랫폼: {detail.get('platform','-')}", size=13),
                ft.Text(f"출시일: {detail.get('release_date','-')}", size=13),
                ft.Text(f"서비스 상태: {detail.get('status','-')}", size=13),
                ft.Divider(),
                ft.Text("BM 요약", weight=ft.FontWeight.BOLD),
                ft.Text(f"BM 유형: {bm.get('bm_type','-')}", size=13),
                ft.Text(f"최고 등급 확률: {bm.get('top_prob','-')}%", size=13),
                ft.Text(f"천장: {bm.get('pity_count','없음')}", size=13),
                ft.Text(f"BM 친화도: {bm.get('bm_score','-')}점", size=13, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("최근 매출 순위", weight=ft.FontWeight.BOLD),
                *[ft.Text(f"{r['year']}-{r['month']:02d} {r['store']}: {r['rank_position']}위", size=13)
                  for r in ranks],
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        safe_update(self.detail_container)
