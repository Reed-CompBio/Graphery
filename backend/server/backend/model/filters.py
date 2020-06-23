from django.db.models import QuerySet
from graphql import ResolveInfo

from backend.model.UserModel import ROLES


def published_filter(queryset: QuerySet, info: ResolveInfo) -> QuerySet:
    if info.context.user.role == ROLES.VISITOR:
        return queryset.filter(is_published=True)
    return queryset
