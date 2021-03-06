import graphene
from gql_api.views import dsp


class Query(
    dsp.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    dsp.Mutation,
    graphene.ObjectType
):
    pass


SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
