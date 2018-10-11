from crispy_forms.utils import render_crispy_form
from django_jinja import library, utils
import jinja2


@library.global_function
@jinja2.contextfunction
@utils.safe
def crispy(context, form):
    return render_crispy_form(form, context=context)
