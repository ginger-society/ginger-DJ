import warnings

from ginger.core.exceptions import ImproperlyConfigured
from ginger.utils.deprecation import RemovedInGinger60Warning

try:
    import oracledb

    is_oracledb = True
except ImportError as e:
    try:
        import cx_Oracle as oracledb  # NOQA

        warnings.warn(
            "cx_Oracle is deprecated. Use oracledb instead.",
            RemovedInGinger60Warning,
            stacklevel=2,
        )
        is_oracledb = False
    except ImportError:
        raise ImproperlyConfigured(f"Error loading oracledb module: {e}")
