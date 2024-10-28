from prometheus_client import Counter

from prometheus.conf import NAMESPACE

ginger_cache_get_total = Counter(
    "ginger_cache_get_total",
    "Total get requests on cache",
    ["backend"],
    namespace=NAMESPACE,
)
ginger_cache_hits_total = Counter(
    "ginger_cache_get_hits_total",
    "Total hits on cache",
    ["backend"],
    namespace=NAMESPACE,
)
ginger_cache_misses_total = Counter(
    "ginger_cache_get_misses_total",
    "Total misses on cache",
    ["backend"],
    namespace=NAMESPACE,
)
ginger_cache_get_fail_total = Counter(
    "ginger_cache_get_fail_total",
    "Total get request failures by cache",
    ["backend"],
    namespace=NAMESPACE,
)
