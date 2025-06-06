from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# mock channel
CHANNEL_DIR = DATA_DIR / "channel"
RECIPES_DIR = DATA_DIR / "recipes"

# lockfiles
PIXI_DIR = DATA_DIR / "pixi"
PIXI_METADATA_DIR = DATA_DIR / "pixi-metadata"
CONDA_LOCK_METADATA_DIR = DATA_DIR / "conda-lock-metadata"
EXPLICIT_LOCK_DIR = DATA_DIR / "explicit"

# Enviroments
ENVIRONMENTS_DIR = DATA_DIR / "environments"
SINGLE_PACKAGE_ENV = ENVIRONMENTS_DIR / "single_package"
