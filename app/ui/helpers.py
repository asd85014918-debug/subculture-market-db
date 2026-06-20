# app/ui/helpers.py
"""화면(View) 클래스들이 공유하는 작은 유틸리티.

Flet 0.85+에서는 컨트롤이 아직 페이지 트리에 추가되기 전에 `.page`를 읽으면
RuntimeError가 발생한다(과거 버전은 None을 반환했음). build() 최초 호출 시점에는
아직 트리에 붙기 전이므로, update() 호출 전에 안전하게 부착 여부를 확인해야 한다.
"""


def safe_update(control) -> None:
    """control이 이미 페이지 트리에 연결되어 있으면 update()를 호출하고,
    아직 연결되지 않았으면(최초 build 단계) 조용히 넘어간다."""
    try:
        if control.page is not None:
            control.update()
    except RuntimeError:
        pass
