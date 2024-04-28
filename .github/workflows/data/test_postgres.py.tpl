from test_sqlite import *  # NOQA

DATABASES = {
    "default": {
        "ENGINE": "ginger.db.backends.postgresql",
        "USER": "user",
        "NAME": "ginger",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    },
    "other": {
        "ENGINE": "ginger.db.backends.postgresql",
        "USER": "user",
        "NAME": "ginger2",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    },
}
