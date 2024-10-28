import os

FLATPAGES_TEMPLATES = [
    {
        "BACKEND": "gingerdj.template.backends.gingerdj.GingerTemplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "OPTIONS": {
            "context_processors": (),
        },
    }
]
