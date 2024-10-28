from test_sqlite import *  # NOQA

DATABASES = {
    "default": {
        "ENGINE": "gingerdj.db.backends.postgresql",
        "USER": "user",
        "NAME": "gingerdj",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    },
    "other": {
        "ENGINE": "gingerdj.db.backends.postgresql",
        "USER": "user",
        "NAME": "ginger2",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    },
}
