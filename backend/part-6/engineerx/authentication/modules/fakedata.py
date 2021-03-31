import os
import logging
from faker import Faker
from random import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.files import File

from wagtail.users.models import UserProfile

# logger = logging.getLogger(__name__)
logger = logging.getLogger("fake users:")
User = get_user_model()
fake = Faker()


class FakeUser:
    def __init__(self, fake_profile, password):
        name = fake_profile['name']
        name_words = name.split()
        (self.first_name, self.last_name) = (name_words[0], name_words[1:][0])
        self.username = fake_profile['username']
        self.email = fake_profile['mail']
        self.password = password


def create_user(avatar, is_moderator=False, is_editor=False):
    user = FakeUser(fake_profile=fake.profile(), password=fake.password())
    user = User.objects.create_user(
        username=user.username, email=user.email, password=user.password,
        first_name=user.first_name, last_name=user.last_name,
    )
    profile = UserProfile(user=user)
    profile.save()
    avatar_path = os.path.join(settings.AVATAR_DOWNLOADS_DIR, avatar)
    with open(avatar_path, "rb") as file:
        avatar_file = File(file)
        profile.avatar.save(avatar, avatar_file, save=True)
    logger.info(
        f'Successfully created user: {user.first_name} {user.last_name} with username: {user.username}'
    )
    if is_moderator:
        group = Group.objects.get(name='Moderators')
    elif is_editor:
        group = Group.objects.get(name='Editors')
    else:
        group = None
    if group:
        user.groups.add(group)
    return user


def create_users(size, is_moderator=False, is_editor=False):
    avatars = os.listdir(settings.AVATAR_DOWNLOADS_DIR)
    users = []
    i = 0
    while i < size:
        try:
            random_index = int(random() * len(avatars))
            users.append(
                create_user(avatars[random_index], is_moderator, is_editor)
            )
            i += 1
        except Exception as e:
            continue
    return users
