from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from tools.models import ToolTaxonomy, UserTool



class ToolTaxonomyNode(DjangoObjectType):

    class Meta:
        model = ToolTaxonomy
        interfaces = (Node,)
        filter_fields = ['name', 'slug', 'state']

# class UserToolNode()

class Query:
    tool_taxonomy = Node.Field(ToolTaxonomyNode)
    all_tool_taxonomies = DjangoFilterConnectionField(ToolTaxonomyNode)

    # ingredient = Node.Field(IngredientNode)
    # all_ingredients = DjangoFilterConnectionField(IngredientNode)
