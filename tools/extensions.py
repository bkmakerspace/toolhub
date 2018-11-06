from jinja2.ext import Extension

from tools.models import UserTool


class ToolConstantsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["ToolStates"] = UserTool.States
        environment.globals["ToolTransitions"] = UserTool.Transitions
        environment.globals["ToolClearance"] = UserTool.Clearance
        environment.globals["ToolVisibility"] = UserTool.Visibility
