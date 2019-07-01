from typing import NamedTuple

from django.contrib.humanize.templatetags.humanize import intcomma
from jinja2.ext import Extension
from memoize import memoize

from tools.models import ToolHistory, UserTool
from toolhub_auth.models import User


class EventsExtension(Extension):
    pass


class Stat(NamedTuple):
    name: str
    value: str
    unit: str

    def __repr__(self) -> str:
        return f"{self.value}{self.unit} {self.name}"


class StatTracker:
    def __init__(self):
        self.stats = []

        self.add_stat("Tools", UserTool.objects.count())
        self.add_stat("Users", User.objects.filter(is_active=True).count())
        self.add_stat("Actions", ToolHistory.objects.count())

    def add_stat(self, name, value, unit=None):
        self.stats.append(Stat(name, intcomma(value), unit or ""))

    def __iter__(self) -> iter:
        return iter(self.stats)

    def __len__(self) -> int:
        return len(self.stats)


class StatsExtension(Extension):
    @memoize(timeout=120)
    def build_stats(self):
        return StatTracker()

    def __init__(self, env):
        super().__init__(env)
        env.globals["toolhub_stats"] = self.build_stats
