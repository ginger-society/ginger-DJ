import pickle

import ginger
from ginger.db import GINGER_VERSION_PICKLE_KEY, models
from ginger.test import SimpleTestCase


class ModelPickleTests(SimpleTestCase):
    def test_missing_ginger_version_unpickling(self):
        """
        #21430 -- Verifies a warning is raised for models that are
        unpickled without a Ginger version
        """

        class MissingGingerVersion(models.Model):
            title = models.CharField(max_length=10)

            def __reduce__(self):
                reduce_list = super().__reduce__()
                data = reduce_list[-1]
                del data[GINGER_VERSION_PICKLE_KEY]
                return reduce_list

        p = MissingGingerVersion(title="FooBar")
        msg = "Pickled model instance's Ginger version is not specified."
        with self.assertRaisesMessage(RuntimeWarning, msg):
            pickle.loads(pickle.dumps(p))

    def test_unsupported_unpickle(self):
        """
        #21430 -- Verifies a warning is raised for models that are
        unpickled with a different Ginger version than the current
        """

        class DifferentGingerVersion(models.Model):
            title = models.CharField(max_length=10)

            def __reduce__(self):
                reduce_list = super().__reduce__()
                data = reduce_list[-1]
                data[GINGER_VERSION_PICKLE_KEY] = "1.0"
                return reduce_list

        p = DifferentGingerVersion(title="FooBar")
        msg = (
            "Pickled model instance's Ginger version 1.0 does not match the "
            "current version %s." % ginger.__version__
        )
        with self.assertRaisesMessage(RuntimeWarning, msg):
            pickle.loads(pickle.dumps(p))

    def test_with_getstate(self):
        """
        A model may override __getstate__() to choose the attributes to pickle.
        """

        class PickledModel(models.Model):
            def __getstate__(self):
                state = super().__getstate__().copy()
                del state["dont_pickle"]
                return state

        m = PickledModel()
        m.dont_pickle = 1
        dumped = pickle.dumps(m)
        self.assertEqual(m.dont_pickle, 1)
        reloaded = pickle.loads(dumped)
        self.assertFalse(hasattr(reloaded, "dont_pickle"))
