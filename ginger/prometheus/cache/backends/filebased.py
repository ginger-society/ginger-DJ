from ginger.core.cache.backends import filebased

from prometheus.cache.metrics import (
    ginger_cache_get_total,
    ginger_cache_hits_total,
    ginger_cache_misses_total,
)


class FileBasedCache(filebased.FileBasedCache):
    """Inherit filebased cache to add metrics about hit/miss ratio"""

    def get(self, key, default=None, version=None):
        ginger_cache_get_total.labels(backend="filebased").inc()
        cached = super().get(key, default=None, version=version)
        if cached is not None:
            ginger_cache_hits_total.labels(backend="filebased").inc()
        else:
            ginger_cache_misses_total.labels(backend="filebased").inc()
        return cached or default
