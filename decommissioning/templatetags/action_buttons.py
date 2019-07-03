from crispy_forms.utils import render_crispy_form
from django_jinja import library, utils
import jinja2

from decommissioning.forms import DecommissionForm, ReinstateForm


@library.global_function
@jinja2.contextfunction
@utils.safe
def decommission_button(context, tool):
    form = DecommissionForm(initial=dict(tool=tool))
    return render_crispy_form(form, context=context)


@library.global_function
@jinja2.contextfunction
@utils.safe
def reinstate_button(context, tool):
    form = ReinstateForm(initial=dict(tool=tool))
    return render_crispy_form(form, context=context)
