from typing import Type

from django.core.management.utils import get_random_secret_key
from .UserModel import ROLES


class MetaData:
    about = ''
    notification_banner = ''
    notification_card_before = ''
    notification_card_after = ''


class InvitationCode:
    code_collection = {}

    @staticmethod
    def generate_invitation_code() -> str:
        return get_random_secret_key()

    @classmethod
    def refresh_all_code(cls) -> Type['InvitationCode']:
        for label in ROLES.labels:
            cls.code_collection[label] = cls.generate_invitation_code()

        return cls
