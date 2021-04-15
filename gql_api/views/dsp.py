import timeit
import requests
import random
import graphene
from graphql import GraphQLError
from api.models.dsp import Ad
from database import SCOPED_SESSION
from config import API_URL

BATCH_SIZE = 1000


class AdBid(graphene.ObjectType):
    ad_id = graphene.ID(required=True)
    price = graphene.Int(required=True)


class Query(graphene.ObjectType):
    bw_dsp = graphene.Field(AdBid, bid_floor=graphene.Int(required=True))
    timeit_dsp = graphene.Float(num_test=graphene.Int(required=True))

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

    @staticmethod
    def resolve_timeit_dsp(parent, info, num_test, **kwargs):
        def func():
            data = {'bid_floor': random.randint(1, 50)}
            r = requests.post(f'{API_URL}/bw_dsp', data=data)
        return timeit.timeit(lambda: func(), number=num_test)


class AddAds(graphene.Mutation):
    class Arguments:
        data_num = graphene.Int(default_value=10)

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(parent, info, data_num, **kwargs):
        try:
            ads = []
            for _ in range(data_num):
                ads += [Ad(
                    status=bool(random.getrandbits(1)),
                    bidding_cpm=random.randint(0, 10)
                )]
            SCOPED_SESSION.add_all(ads)
            SCOPED_SESSION.commit()
        except Exception as e:
            raise GraphQLError('500')
        return AddAds(ok=True)


class DeleteAds(graphene.Mutation):
    class Arguments:
        pass

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(parent, info, **kwargs):
        try:
            Ad.query.delete()
            SCOPED_SESSION.commit()
        except Exception as e:
            raise GraphQLError('500')
        return DeleteAds(ok=True)


class Mutation(graphene.ObjectType):
    add_ads = AddAds.Field()
    delete_ads = DeleteAds.Field()
