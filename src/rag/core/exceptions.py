class RagError(Exception):
    """Projedeki tüm özel hataların tabanı."""


class ParsingError(RagError):
    pass


class RetrievalError(RagError):
    pass


class GenerationError(RagError):
    pass
