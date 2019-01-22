# Temporary, fix actual library
from django_jinja import library, utils
from qr_code.qrcode.maker import make_qr_code


@library.global_function
@utils.safe
def qr_from_text(text, **kwargs):
    return make_qr_code(text, qr_code_args=kwargs, embedded=True)
