from config.settings.base import *  # noqa: F403

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[]) # noqa: F405
