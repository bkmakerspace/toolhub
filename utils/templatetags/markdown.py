from django.utils.module_loading import import_string
from django_jinja import library, utils
from markdownx.settings import MARKDOWNX_MARKDOWNIFY_FUNCTION


markdownify = import_string(MARKDOWNX_MARKDOWNIFY_FUNCTION)


@library.global_function
@utils.safe
def markdown(text, *args, **kwargs):
    return markdownify(text, *args, **kwargs)
