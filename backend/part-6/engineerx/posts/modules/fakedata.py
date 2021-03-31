from faker import Faker
from random import random

from django.contrib.auth.models import Group

from wagtail.images import get_image_model

from home.models import PostPage, HomePage

fake = Faker()
Image = get_image_model()


def create_fake_richtext():
    size = int(random() * 10) + 1
    richtext = ''
    for i in range(size):
        richtext += f'<p>{fake.text()}</p>'
    return richtext


def create_paragraph_block():
    return {
        'type': 'paragraph',
        'value': create_fake_richtext(),
    }


def create_image_block():
    images = Image.objects.all()
    image = images[int(random() * len(images))]
    return {
        'type': 'image',
        'value': {'image': image.id, 'caption': create_fake_richtext()},
    }


def create_rows(size):
    rows = []
    for i in range(size):
        if random() < 0.25:
            rows.append(create_image_block())
        else:
            rows.append(create_paragraph_block())
    return rows


def create_new_section():
    return {
        'type': 'section',
        'value': {
            'title': fake.sentence(),
            'rows': create_rows(int(random() * 10) + 1)
        }
    }


def create_new_post(owner, tags):
    post = PostPage(title=fake.sentence(), owner=owner)
    home_page = HomePage.objects.first()
    home_page.add_child(instance=post)
    post = PostPage.objects.get(slug=post.slug)
    if random() >= 0.5:
        images = Image.objects.all()
        post.image = images[int(random() * len(images))]
    stream_data = post.sections.stream_data
    sections_size = int(random() * 2) + 1
    for i in range(sections_size):
        stream_data.append(create_new_section())

    for tag in tags:
        if random() < 0.3:
            post.tags.add(tag)
    post.save()
    post.save_revision().publish()
    return post


def create_tags(size):
    tags = []
    for i in range(size):
        tags.append(fake.word())
    return tags


def create_new_posts(size):
    tags = create_tags(int(size / 2))
    posts = []
    i = 0
    while i < size:
        try:
            moderators_group = Group.objects.get(name='Moderators')
            moderators = moderators_group.user_set.all()
            user = moderators[int(random() * len(moderators))]
            posts.append(create_new_post(user, tags))
            i += 1
        except:
            continue
    return posts
