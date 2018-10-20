class ContextMixin:
    """Simple api for adding aditional context to a CBV"""

    def __init__(self, *args, **kwargs):
        self.context = {}
        super(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.context)
        return context

    def add_context(self, **context):
        self.context.update(**context)
