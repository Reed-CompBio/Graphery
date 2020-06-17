import graphene

import graphery.backend.graphql.schema as backend_schema


class Query(backend_schema.Query, graphene.ObjectType):
    pass


class Mutation(backend_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
