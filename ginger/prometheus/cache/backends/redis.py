from ginger import VERSION as GINGER_VERSION
from ginger_redis import cache, exceptions
from prometheus.cache.metrics import (
    ginger_cache_get_fail_total,
    ginger_cache_get_total,
    ginger_cache_hits_total,
    ginger_cache_misses_total,
)


class RedisCache(cache.RedisCache):
    """Inherit redis to add metrics about hit/miss/interruption ratio"""

    @cache.omit_exception
    def get(self, key, default=None, version=None, client=None):
        try:
            ginger_cache_get_total.labels(backend="redis").inc()
            cached = self.client.get(key, default=None, version=version, client=client)
        except exceptions.ConnectionInterrupted as e:
            ginger_cache_get_fail_total.labels(backend="redis").inc()
            if self._ignore_exceptions:
                if self._log_ignored_exceptions:
                    cache.logger.error(str(e))
                return default
            raise
        else:
            if cached is not None:
                ginger_cache_hits_total.labels(backend="redis").inc()
                return cached
            else:
                ginger_cache_misses_total.labels(backend="redis").inc()
                return default


if GINGER_VERSION >= (4, 0):
    from ginger.core.cache.backends.redis import RedisCache

    class NativeRedisCache(RedisCache):

        def get(self, key, default=None, version=None):
            ginger_cache_get_total.labels(backend="native_redis").inc()
            try:
                result = super().get(key, default=None, version=version)
            except Exception:
                ginger_cache_get_fail_total.labels(backend="native_redis").inc()
                raise
            if result is not None:
                ginger_cache_hits_total.labels(backend="native_redis").inc()
                return result
            else:
                ginger_cache_misses_total.labels(backend="native_redis").inc()
                return default
