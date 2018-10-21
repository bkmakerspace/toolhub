from collections import Iterable, MutableSet
from django_jinja import library


@library.global_function(name="classlist")
class ClassList(MutableSet):
    """Data structure for holding, and ultimately returning as a single string,
    a set of identifiers that should be managed like CSS classes.
    """
    def __init__(self, arg=None):
        """Constructor.
        :param arg: A single class name or an iterable thereof.
        """
        if isinstance(arg, str):
            classes = arg.split()
        elif isinstance(arg, Iterable):
            classes = arg
        elif arg is not None:
            raise TypeError(
                "expected a string or string iterable, got %r" % type(arg))

        self.classes = set(filter(None, classes))

    def __contains__(self, class_):
        return class_ in self.classes

    def __iter__(self):
        return iter(self.classes)

    def __len__(self):
        return len(self.classes)

    def add(self, *classes):
        for class_ in classes:
            self.classes.add(class_)

    def discard(self, *classes):
        for class_ in classes:
            self.classes.discard(class_)

    def __str__(self):
        return " ".join(sorted(self.classes))

    def __html__(self):
        return 'class="%s"' % self if self else ""
