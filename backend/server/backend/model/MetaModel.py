from typing import Type, Container
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.conf import settings
from .UserModel import ROLES


class MetaData:
    about = ''
    notification_banner = ''
    notification_card_before = ''
    notification_card_after = ''


class InvitationCode:
    code_collection = {}
    role_mapping = {label: value for label, value in (reversed(pair) for pair in ROLES.choices)}

    @staticmethod
    def generate_invitation_code() -> str:
        return get_random_secret_key()

    @classmethod
    def refresh_all_code(cls) -> Type['InvitationCode']:
        for label in ROLES.labels:
            cls.code_collection[label] = cls.generate_invitation_code()

        with open(Path(settings.INVITATION_CODE_FOLDER) / 'invitation_codes.txt', 'w') as file:
            file.write(str(cls.code_collection))

        return cls

    @classmethod
    def codes(cls) -> Container:
        return cls.code_collection.values()
