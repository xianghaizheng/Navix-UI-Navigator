from enum import Enum
class DataRoutes(Enum):
    DATA_EXPLORER = "data.explorer"
    DATA_IMPORTER = "data.importer"
    QUERY_BUILDER = "query.builder"
    def __str__(self) -> str:
        return self.value