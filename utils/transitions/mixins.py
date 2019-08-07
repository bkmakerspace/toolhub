from braces.views import MessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.urls import reverse


class TransitionActionMixin:
    transition_name = None
    object_attribute = None

    def get_transition_name(self):
        return self.transition_name

    def post(self, request, *args, **kwargs):
        return self.perform_transition()

    def perform_transition(self):
        trans_object = self.get_transition_object()
        transition = getattr(trans_object, self.get_transition_name())
        # assert is transition
        # TOOD: make this look more like form view mixinx
        try:
            with transaction.atomic():
                transition(**self.get_transition_kwargs())
        except Exception as exception:
            self.handle_transition_exception(exception)
            return self.transition_failure(exception)
        # did we want to do different things based on the type of exception?
        # except ToolException as e:
        #     self.handle_transition_exception(e)
        # except MachineError as e:
        #     self.handle_transition_exception(e)
        else:
            return self.transition_success()

    def handle_transition_exception(self, exception):
        pass

    def transition_success(self):
        raise NotImplementedError

    def transition_failure(self, exception):
        raise NotImplementedError

    def get_transition_object(self):
        return getattr(self, self.object_class_attribute)

    def get_transition_kwargs(self):
        return {"user": self.request.user}


class TransitionMessageMixin(TransitionActionMixin, MessageMixin):
    """Configurable transition messages for action views"""

    transition_success_message = None
    transition_failed_message = None

    def transition_success(self):
        self.messages.success(self.get_transition_success_message(), fail_silently=True)

    def get_transition_success_message(self):
        """
        Validate that transition_success_message is set and is either a
        unicode or str object.
        """
        if self.transition_success_message is None:
            raise ImproperlyConfigured(
                "{0}.transition_success_message is not set. Define "
                "{0}.transition_success_message, or override "
                "{0}.get_transition_success_message().".format(self.__class__.__name__)
            )

        if not isinstance(
            self.transition_success_message, (six.string_types, six.text_type, Promise)
        ):
            raise ImproperlyConfigured(
                "{0}.transition_success_message must be a str or unicode "
                "object.".format(self.__class__.__name__)
            )

        return force_text(self.transition_success_message)

    def transition_failure(self, e):
        self.messages.error(self.get_transition_failed_message(), fail_silently=True)

    def get_transition_failed_message(self):
        """
        Validate that transition_failed_message is set and is either a
        unicode or str object.
        """
        if self.transition_failed_message is None:
            raise ImproperlyConfigured(
                "{0}.transition_failed_message is not set. Define "
                "{0}.transition_failed_message, or override "
                "{0}.get_transition_failed_message().".format(self.__class__.__name__)
            )

        if not isinstance(
            self.transition_failed_message, (six.string_types, six.text_type, Promise)
        ):
            raise ImproperlyConfigured(
                "{0}.transition_failed_message must be a str or unicode "
                "object.".format(self.__class__.__name__)
            )

        return force_text(self.transition_failed_message)


class ActionViewMixin(TransitionMessageMixin):
    def transition_success(self):
        super().transition_success()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def transition_failure(self, e):
        super().transition_failure(e)
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        raise NotImplementedError
