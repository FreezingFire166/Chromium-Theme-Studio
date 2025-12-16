from enum import Enum, auto


class SectionType(Enum):
    COLOR = auto()
    IMAGE = auto()


SECTIONS = [
    # ── COLORS ───────────────────────────
    ("frame", "Frame", SectionType.COLOR),
    ("tab_active", "Active Tab", SectionType.COLOR),
    ("tab_inactive", "Inactive Tab", SectionType.COLOR),
    ("toolbar", "Toolbar", SectionType.COLOR),
    ("tab_text", "Tab Text", SectionType.COLOR),
    ("toolbar_text", "Toolbar Text", SectionType.COLOR),
    ("bookmark_text", "Bookmark Text", SectionType.COLOR),

    # ── IMAGES ───────────────────────────
    ("frame_image", "Frame Image", SectionType.IMAGE),
    ("background_image", "Background Image", SectionType.IMAGE),
]
