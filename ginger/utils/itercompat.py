# RemovedInGinger60Warning: Remove this entire module.

import warnings

from ginger.utils.deprecation import RemovedInGinger60Warning


def is_iterable(x):
    "An implementation independent way of checking for iterables"
    warnings.warn(
        "ginger.utils.itercompat.is_iterable() is deprecated. "
        "Use isinstance(..., collections.abc.Iterable) instead.",
        RemovedInGinger60Warning,
        stacklevel=2,
    )
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True
