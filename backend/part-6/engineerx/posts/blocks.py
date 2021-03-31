from django.conf import settings

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class CodeBlock(blocks.StructBlock):
    language = blocks.CharBlock()
    content = blocks.TextBlock()

    class Meta:
        icon = 'cogs'


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock(
        features=settings.DEFAULT_RICHTEXT_FEATURES, required=False
    )

    class Meta:
        icon = 'image'


class ParagraphBlock(blocks.RichTextBlock):
    def __init__(self, features=settings.DEFAULT_RICHTEXT_FEATURES, **kwargs):
        super().__init__(features=features, **kwargs)

    class Meta:
        icon = 'doc-full'


class RowsBlock(blocks.StreamBlock):
    image = ImageBlock()
    paragraph = ParagraphBlock()
    code = CodeBlock()


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    rows = RowsBlock(required=True)

    class Meta:
        icon = 'doc-empty'


class SectionsBlock(blocks.StreamBlock):
    section = SectionBlock()
