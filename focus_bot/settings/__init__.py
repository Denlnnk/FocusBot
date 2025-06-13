import os

from dotenv import load_dotenv

load_dotenv()

AVAILABLE_ENVS = {'production', 'local'}

env = os.getenv('PROJECT_ENV', 'local').lower()

if env not in AVAILABLE_ENVS:
    raise ValueError(f"Invalid PROJECT_ENV: '{env}'. Must be one of {AVAILABLE_ENVS}.")

try:
    if env == 'production':
        from .production import *
    elif env == 'local':
        from .local import *
    print(f"Configuration loaded for environment: {env}")
except ImportError as e:
    raise ImportError(f"Error loading configuration for environment '{env}': {e}")
