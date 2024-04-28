from ginger.core import management
from ginger.test import TestCase, override_settings

from .models import Article


class SwappableModelTests(TestCase):
    # Limit memory usage when calling 'migrate'.
    available_apps = [
        "swappable_models",
    ]

    @override_settings(TEST_ARTICLE_MODEL="swappable_models.AlternateArticle")
    def test_generated_data(self):
        "Permissions and content types are not created for a swapped model"

        # Delete all permissions and content_types

        # Re-run migrate. This will re-build the permissions and content types.
        management.call_command("migrate", interactive=False, verbosity=0)

        # Content types and permissions exist for the swapped model,
        # but not for the swappable model.
        apps_models = [
           
        ]
        self.assertIn(("swappable_models", "alternatearticle"), apps_models)
        self.assertNotIn(("swappable_models", "article"), apps_models)

        self.assertIn(("swappable_models", "alternatearticle"), apps_models)
        self.assertNotIn(("swappable_models", "article"), apps_models)

    @override_settings(TEST_ARTICLE_MODEL="swappable_models.article")
    def test_case_insensitive(self):
        "Model names are case insensitive. Model swapping honors this."
        Article.objects.all()
        self.assertIsNone(Article._meta.swapped)
