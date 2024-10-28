from ginger_memcached_consul import memcached

from prometheus.cache.metrics import (
    ginger_cache_get_total,
    ginger_cache_hits_total,
    ginger_cache_misses_total,
)


class MemcachedCache(memcached.MemcachedCache):
    """Inherit ginger_memcached_consul to add metrics about hit/miss ratio"""

    def get(self, key, default=None, version=None):
        ginger_cache_get_total.labels(backend="ginger_memcached_consul").inc()
        cached = super().get(key, default=None, version=version)
        if cached is not None:
            ginger_cache_hits_total.labels(backend="ginger_memcached_consul").inc()
        else:
            ginger_cache_misses_total.labels(backend="ginger_memcached_consul").inc()
        return cached or default
