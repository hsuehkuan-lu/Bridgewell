import random
import pytest
import json
from api.models.dsp import Ad
from tests.conftest import client, db_session
from app import app

BATCH_SIZE = 1000


def test_dsp(db_session):
    ads = []
    for _ in range(1000):
        ads += [Ad(
            status=True,
            bidding_cpm=random.randint(1, 10)
        )]
    db_session.add_all(ads)
    db_session.commit()

    q = db_session.query(Ad).filter(Ad.status)
    bid_price = 0
    ads = []
    target_ad = None
    for ad in q.yield_per(BATCH_SIZE):
        price = ad.bidding_cpm * random.randint(1, 10)
        ads += [{
            'ad_id': ad.ad_id,
            'price': price
        }]
        if price > bid_price:
            bid_price = price
            target_ad = ad
    assert max(ads, key=lambda x: x['price'])['ad_id'] == target_ad.ad_id, "Ad is mismatch."
