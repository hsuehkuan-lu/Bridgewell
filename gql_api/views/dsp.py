import random
import graphene
from graphql import GraphQLError
from api.models.dsp import Ad
from gql_api.schema.dsp import AdNode

BATCH_SIZE = 1000


class AdBid(graphene.ObjectType):
    ad_id = graphene.ID(required=True)
    price = graphene.Int(required=True)


class Query(graphene.ObjectType):
    bw_dsp = graphene.Field(AdBid, bid_floor=graphene.Int(required=True))

    @staticmethod
    def resolve_bw_dsp(parent, info, bid_floor, **kwargs):
        q = Ad.query.filter(Ad.status)
        bid_price = 0
        target_ad = None
        for ad in q.yield_per(BATCH_SIZE):
            price = ad.bidding_cpm * random.randint(1, 10)
            if price >= bid_floor and price > bid_price:
                bid_price = price
                target_ad = ad
        if target_ad is None:
            raise GraphQLError('204')
        return {
            'price': bid_price,
            'ad_id': target_ad.ad_id
        }
