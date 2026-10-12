from enum import Enum


class ElementType(str, Enum):
    TEXT = "text"
    HEADING = "heading"
    TABLE = "table"
    FIGURE = "figure"
    HEADER_FOOTER = "header_footer"


class LineRole(str, Enum):
    TEXT = "text"
    HEADING_CANDIDATE = "heading_candidate"


class DecisionStatus(str, Enum):
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"
