from typing import Optional

import graphene

from graphql import GraphQLError
from django.contrib.auth import authenticate, login, logout

from backend.graphql.decorators import admin_required
from backend.graphql.mutation_base import SuccessMutationBase
from backend.graphql.utils import process_model_wrapper
from backend.intel_wrappers.intel_wrapper import UserWrapper
from backend.model.MetaModel import InvitationCode
from backend.graphql.decorators import login_required
from backend.graphql.types import UserType
from backend.model.UserModel import User


class RefreshInvitationCode(SuccessMutationBase):
    @admin_required
    @graphene.resolve_only_args
    def mutate(self):
        InvitationCode.refresh_all_code()
        return RefreshInvitationCode(success=True)


class Register(SuccessMutationBase):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        invitation_code = graphene.String(required=True)

    user = graphene.Field(UserType, required=True)

    @graphene.resolve_only_args
    def mutate(self, email: str, username: str, password: str, invitation_code: str):
        email = email.strip()
        username = username.strip()
        password = password.strip()
        invitation_code = invitation_code.strip()

        if not invitation_code:
            raise GraphQLError("You have to enter an invitation code!")

        role_string: Optional[str] = next((label for label, value in InvitationCode.code_collection.items()
                                          if value == invitation_code), None)

        if role_string is None:
            raise GraphQLError("You don't have the permission to register!")

        role: int = InvitationCode.role_mapping[role_string]

        user_wrapper: UserWrapper = process_model_wrapper(UserWrapper,
                                                          email=email, username=username, password=password, role=role)

        return Register(success=True, user=user_wrapper.model)


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean(required=True)
    user = graphene.Field(UserType)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(info.context, user)
        return Login(success=user is not None, user=user)


class Logout(graphene.Mutation):
    success = graphene.Boolean(required=True)

    @login_required
    def mutate(self, info):
        user = info.context.user
        if user.is_authenticated:
            logout(info.context)
            return Login(success=True)
        else:
            raise GraphQLError('Not Logged In')
