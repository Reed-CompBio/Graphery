import graphene

from backend.graphql.query import Query as backend_query
from backend.graphql.mutation import Mutation as backend_mutation
from backend.model.translation_collection import translation_types


class Query(backend_query, graphene.ObjectType):
    pass


class Mutation(backend_mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,
                         mutation=Mutation,
                         types=translation_types)
