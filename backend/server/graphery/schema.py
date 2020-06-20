import graphene

from backend.graphql.query import Query as backend_query
from backend.graphql.mutation import Mutation as backend_mutation
import backend.graphql.types as backend_types


class Query(backend_query, graphene.ObjectType):
    hello = graphene.Field(graphene.String)

    def resolve_hello(self, info, **kwargs):
        return 'hello world :)'


class Mutation(backend_mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,
                         mutation=Mutation,
                         types=[
                             backend_types.ENUSTransType,
                             backend_types.ZHCNTransType
                         ])
