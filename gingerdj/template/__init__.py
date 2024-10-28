"""
GingerDJ's support for templates.

The gingerdj.template namespace contains two independent subsystems:

1. Multiple Template Engines: support for pluggable template backends,
   built-in backends and backend-independent APIs
2. GingerDJ Template Language: GingerDJ's own template engine, including its
   built-in loaders, context processors, tags and filters.

Ideally these subsystems would be implemented in distinct packages. However
keeping them together made the implementation of Multiple Template Engines
less disruptive .

Here's a breakdown of which modules belong to which subsystem.

Multiple Template Engines:

- gingerdj.template.backends.*
- gingerdj.template.loader
- gingerdj.template.response

GingerDJ Template Language:

- gingerdj.template.base
- gingerdj.template.context
- gingerdj.template.context_processors
- gingerdj.template.loaders.*
- gingerdj.template.context_processors.debug
- gingerdj.template.defaultfilters
- gingerdj.template.defaulttags
- gingerdj.template.engine
- gingerdj.template.loader_tags
- gingerdj.template.smartif

Shared:

- gingerdj.template.utils

"""

# Multiple Template Engines

from .engine import Engine
from .utils import EngineHandler

engines = EngineHandler()

__all__ = ("Engine", "engines")


# GingerDJ Template Language

# Public exceptions
from .base import VariableDoesNotExist  # NOQA isort:skip
from .context import Context, ContextPopException, RequestContext  # NOQA isort:skip
from .exceptions import TemplateDoesNotExist, TemplateSyntaxError  # NOQA isort:skip

# Template parts
from .base import (  # NOQA isort:skip
    Node,
    NodeList,
    Origin,
    Template,
    Variable,
)

# Library management
from .library import Library  # NOQA isort:skip

# Import the .autoreload module to trigger the registrations of signals.
from . import autoreload  # NOQA isort:skip


__all__ += ("Template", "Context", "RequestContext")
