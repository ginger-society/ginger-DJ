from ginger.core.cache.backends import locmem

from prometheus.cache.metrics import (
    ginger_cache_get_total,
    ginger_cache_hits_total,
    ginger_cache_misses_total,
)


class LocMemCache(locmem.LocMemCache):
    """Inherit filebased cache to add metrics about hit/miss ratio"""

    def get(self, key, default=None, version=None):
        ginger_cache_get_total.labels(backend="locmem").inc()
        cached = super().get(key, default=None, version=version)
        if cached is not None:
            ginger_cache_hits_total.labels(backend="locmem").inc()
        else:
            ginger_cache_misses_total.labels(backend="locmem").inc()
        return cached or default
