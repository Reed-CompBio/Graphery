import graphene

import backend.graphql.schema as backend_schema


class Query(backend_schema.Query, graphene.ObjectType):
    hello = graphene.Field(graphene.String)

    def resolve_hello(self, info, **kwargs):
        return 'hello'


class Mutation(backend_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
