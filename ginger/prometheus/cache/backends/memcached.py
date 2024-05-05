from ginger.core.cache.backends import memcached

from prometheus.cache.metrics import (
    ginger_cache_get_total,
    ginger_cache_hits_total,
    ginger_cache_misses_total,
)


class MemcachedPrometheusCacheMixin:
    def get(self, key, default=None, version=None):
        ginger_cache_get_total.labels(backend="memcached").inc()
        cached = super().get(key, default=None, version=version)
        if cached is not None:
            ginger_cache_hits_total.labels(backend="memcached").inc()
        else:
            ginger_cache_misses_total.labels(backend="memcached").inc()
        return cached or default


class PyLibMCCache(MemcachedPrometheusCacheMixin, memcached.PyLibMCCache):
    """Inherit memcached to add metrics about hit/miss ratio"""

    pass


class PyMemcacheCache(MemcachedPrometheusCacheMixin, memcached.PyMemcacheCache):
    """Inherit memcached to add metrics about hit/miss ratio"""

    pass
