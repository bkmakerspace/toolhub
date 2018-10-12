from jinja2.ext import Extension

from tools.models import ToolStates, ToolTransitions, ToolClearance, ToolVisibility


class ToolConstantsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["ToolStates"] = ToolStates
        environment.globals["ToolTransitions"] = ToolTransitions
        environment.globals["ToolClearance"] = ToolClearance
        environment.globals["ToolVisibility"] = ToolVisibility
