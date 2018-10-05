from crispy_forms.helper import FormHelper


class CrispyFormMixin(object):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(CrispyFormMixin, self).__init__(*args, **kwargs)
