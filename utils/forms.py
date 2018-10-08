from crispy_forms.bootstrap import FormActions as CrispyBootstrapFormActions
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper
from crispy_forms.utils import TEMPLATE_PACK


DEFAULT_LABEL_COL = 3
DEFAULT_FIELD_COL = 9


class CrispyFormMixin(object):
    """
    Small helper that instantiates the crispy FormHelper attribute on any form
    with styling.
    """

    has_columns = True

    def __init__(self, *args, **kwargs):
        cols = kwargs.pop('cols', None)
        self.has_columns = kwargs.pop('has_columns', self.has_columns)
        if cols and self.has_columns:
            kwargs.update({
                'label_col': cols[0],
                'field_col': cols[1]
            })
        self.helper = FormHelper()
        self.helper.disable_csrf = False
        self.helper.html5_required = True  # render required attribute
        if self.has_columns:
            self.helper.form_class = 'form-horizontal'
            self.helper.cols = {
                'label_col': kwargs.pop('label_col', DEFAULT_LABEL_COL),
                'field_col': kwargs.pop('field_col', DEFAULT_FIELD_COL),
            }
            self.helper.label_class = 'col-md-{label_col}'.format(**self.helper.cols)
            self.helper.field_class = 'col-md-{field_col}'.format(**self.helper.cols)
        layout_args = self.layout_args(self.helper)
        if layout_args:
            self.helper.layout = Layout(*layout_args)
        super(CrispyFormMixin, self).__init__(*args, **kwargs)

    def layout_args(self, helper):
        pass


class FormActions(CrispyBootstrapFormActions):
    """
    Bootstrap layout object. It wraps fields in a <div class="form-group">
    Also uses the helpers col settings to offset buttons correctly.
    Example::
        FormActions(
            HTML(<span style="display: hidden;">Information Saved</span>),
            Submit('Save', 'Save', css_class='btn-primary'), helper=self.helper)
    """
    cols = None

    def __init__(self, *fields, **kwargs):
        # self.has_columns = kwargs.pop('has_columns', True)
        self.helper = kwargs.pop('helper', False)
        if self.helper and self.helper.has_columns:
            self.cols = kwargs.pop('cols', self.helper.cols)
        super().__init__(*fields, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        if self.cols:
            context.update(self.cols)
        return super().render(form, form_style, context, template_pack=template_pack, **kwargs)
