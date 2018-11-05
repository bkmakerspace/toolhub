from crispy_forms.utils import render_crispy_form
from django_jinja import library, utils
import jinja2

from borrowing.forms import BorrowForm, ReturnForm


@library.global_function
@jinja2.contextfunction
@utils.safe
def borrow_button(context, tool):
    form = BorrowForm(initial=dict(tool=tool))
    return render_crispy_form(form, context=context)


@library.global_function
@jinja2.contextfunction
@utils.safe
def return_button(context, tool):
    form = ReturnForm(initial=dict(tool=tool))
    return render_crispy_form(form, context=context)
