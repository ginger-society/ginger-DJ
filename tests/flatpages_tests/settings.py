import os

FLATPAGES_TEMPLATES = [
    {
        "BACKEND": "ginger.template.backends.ginger.GingerTemplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "templates")],
        "OPTIONS": {
            "context_processors": (),
        },
    }
]
