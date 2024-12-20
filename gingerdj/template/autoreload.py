from pathlib import Path

from gingerdj.dispatch import receiver
from gingerdj.template import engines
from gingerdj.template.backends.gingerdj import GingerTemplates
from gingerdj.utils._os import to_path
from gingerdj.utils.autoreload import autoreload_started, file_changed, is_ginger_path


def get_template_directories():
    # Iterate through each template backend and find
    # any template_loader that has a 'get_dirs' method.
    # Collect the directories, filtering out GingerDJ templates.
    cwd = Path.cwd()
    items = set()
    for backend in engines.all():
        if not isinstance(backend, GingerTemplates):
            continue

        items.update(cwd / to_path(dir) for dir in backend.engine.dirs if dir)

        for loader in backend.engine.template_loaders:
            if not hasattr(loader, "get_dirs"):
                continue
            items.update(
                cwd / to_path(directory)
                for directory in loader.get_dirs()
                if directory and not is_ginger_path(directory)
            )
    return items


def reset_loaders():
    from gingerdj.forms.renderers import get_default_renderer

    for backend in engines.all():
        if not isinstance(backend, GingerTemplates):
            continue
        for loader in backend.engine.template_loaders:
            loader.reset()

    backend = getattr(get_default_renderer(), "engine", None)
    if isinstance(backend, GingerTemplates):
        for loader in backend.engine.template_loaders:
            loader.reset()


@receiver(autoreload_started, dispatch_uid="template_loaders_watch_changes")
def watch_for_template_changes(sender, **kwargs):
    for directory in get_template_directories():
        sender.watch_dir(directory, "**/*")


@receiver(file_changed, dispatch_uid="template_loaders_file_changed")
def template_changed(sender, file_path, **kwargs):
    if file_path.suffix == ".py":
        return
    for template_dir in get_template_directories():
        if template_dir in file_path.parents:
            reset_loaders()
            return True
