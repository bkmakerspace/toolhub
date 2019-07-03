from os import path
from markdown import util, Markdown
from markdown.inlinepatterns import ImageInlineProcessor, IMAGE_LINK_RE
from markdown.blockprocessors import build_block_parser
from markdown.treeprocessors import build_treeprocessors

from tools.models import ToolPhoto


__all__ = ("FindToolPhotos",)


class ImageLinkProcessor(ImageInlineProcessor):
    """register found image instead of swapping content"""

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if handled:
            self.md.found_image(dict(src=src, title=title, text=text))

        return None, None, None


def build(md):
    patterns = util.Registry()
    patterns.register(ImageLinkProcessor(IMAGE_LINK_RE, md), "image_link", 0)
    return patterns


class FindToolPhotos(Markdown):
    def __init__(self, unassigned_only=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unassigned_only = unassigned_only
        self.images = []

    def build_parser(self):
        # don't use pre or post processors
        self.preprocessors = []
        self.parser = build_block_parser(self)
        self.inlinePatterns = build(self)
        self.treeprocessors = build_treeprocessors(self)
        self.postprocessors = []
        return self

    def found_image(self, image_data):
        self.images.append(image_data)

    def reset(self):
        self.htmlStash.reset()
        self.references.clear()
        self.images = []
        return self

    def look(self, source):
        self.lines = source.split("\n")

        # Parse the high-level elements.
        root = self.parser.parseDocument(self.lines).getroot()

        # Run the tree-processors
        for treeprocessor in self.treeprocessors:
            treeprocessor.run(root)

        if self.unassigned_only:
            photo_set = ToolPhoto.objects.filter(tool__isnull=True)
        else:
            photo_set = ToolPhoto.objects

        found_photos = []
        for image in self.images:
            photo = None
            image_name = image["src"]

            image_name_part = path.split(path.split(image_name)[0])[1]
            # path.basename(path.splitext(i.file.name)[0])

            try:
                photo = photo_set.only("id").get(file__contains=image_name_part).id
            except ToolPhoto.DoesNotExist:
                pass
            except ToolPhoto.MultipleObjectsReturned:
                pass
            try:
                assert not photo and bool(image["text"])
                photo = photo_set.only("id").get(title=image["text"]).id
            except (ToolPhoto.DoesNotExist, AssertionError):
                pass

            if bool(photo):
                found_photos.append(photo)

        return ToolPhoto.objects.filter(id__in=found_photos)
