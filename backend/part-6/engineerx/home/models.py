from django.db import models
from django.conf import settings
from django.shortcuts import redirect

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase
from taggit.models import TagBase, ItemBase

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField

from posts.blocks import SectionsBlock
from wagtail.users.models import UserProfile


class HomePage(Page):
    parent_page_types = []
    subpage_types = ['home.PostPage']


class PostTag(TagBase):
    pass


class TaggedPost(ItemBase):
    tag = models.ForeignKey(
        PostTag, related_name="tagged_posts", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to='home.PostPage',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class PostPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    sections = StreamField(SectionsBlock())
    tags = ClusterTaggableManager(through=TaggedPost, blank=True)

    @property
    def owner_info(self):
        image = None
        if UserProfile.objects.filter(user=self.owner).exists():
            if(self.owner.wagtail_userprofile.avatar):
                image = self.owner.wagtail_userprofile.avatar.url
        return {
            'firstname': self.owner.first_name,
            'lastname': self.owner.last_name,
            'image': image,
        }

    api_fields = [
        APIField('image', serializer=ImageRenditionField('min-1500x200')),
        APIField('image_16x9', serializer=ImageRenditionField('fill-1600x900-c70', source='image')),
        APIField('sections'),
        APIField('tags'),
        APIField('owner_info'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('sections'),
        FieldPanel('tags')
    ]