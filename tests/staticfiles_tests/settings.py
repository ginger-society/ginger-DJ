import os.path
from pathlib import Path

TEST_ROOT = os.path.dirname(__file__)

TEST_SETTINGS = {
    "MEDIA_URL": "media/",
    "STATIC_URL": "static/",
    "MEDIA_ROOT": os.path.join(TEST_ROOT, "project", "site_media", "media"),
    "STATIC_ROOT": os.path.join(TEST_ROOT, "project", "site_media", "static"),
    "STATICFILES_DIRS": [
        os.path.join(TEST_ROOT, "project", "documents"),
        ("prefix", os.path.join(TEST_ROOT, "project", "prefixed")),
        Path(TEST_ROOT) / "project" / "pathlib",
    ],
    "STATICFILES_FINDERS": [
        "gingerdj.contrib.staticfiles.finders.FileSystemFinder",
        "gingerdj.contrib.staticfiles.finders.AppDirectoriesFinder",
        "gingerdj.contrib.staticfiles.finders.DefaultStorageFinder",
    ],
    "INSTALLED_APPS": [
        "gingerdj.contrib.staticfiles",
        "staticfiles_tests",
        "staticfiles_tests.apps.test",
        "staticfiles_tests.apps.no_label",
    ],
    "MIDDLEWARE": [],
}
