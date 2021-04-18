import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from api.models.dsp import Ad


class AdNode(SQLAlchemyObjectType):
    class Meta:
        model = Ad

    ad_id = graphene.ID(required=True)
