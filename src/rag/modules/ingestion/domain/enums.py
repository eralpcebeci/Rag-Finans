from enum import Enum


class ElementType(str, Enum):
    TEXT = "text"
    HEADING = "heading"
    TABLE = "table"
    FIGURE = "figure"
    HEADER_FOOTER = "header_footer"
