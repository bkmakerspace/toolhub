import graphene

from graphene_django.debug import DjangoDebug
from tools.schema import Query as ToolsQuery


class Query(
    ToolsQuery,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query)
