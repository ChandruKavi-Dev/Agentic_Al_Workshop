import yaml
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def load_config():
    """Loads the YAML configuration file."""
    config_path = BASE_DIR / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Load the config once when the application starts
settings = load_config()