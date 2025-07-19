from enum import Enum
class AssetRoutes(Enum):
    ASSET_MANAGER = "asset.manager"
    ASSET_VIEWER  = "asset.viewer"
    ASSET_EDITOR  = "asset.editor"
    def __str__(self) -> str:
        return self.value