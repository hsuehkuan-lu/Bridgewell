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
            bidding_cpm=random.randint(1, 10),
            max_bid_count=random.randint(1, 1000)
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


def test_bid_count(db_session):
    ads = [
        Ad(ad_id=1, status=True, bidding_cpm=1, max_bid_count=5, bid_count=2),
        Ad(ad_id=2, status=True, bidding_cpm=2, max_bid_count=3, bid_count=3),
        Ad(ad_id=3, status=True, bidding_cpm=3, max_bid_count=4, bid_count=3),
        Ad(ad_id=4, status=True, bidding_cpm=4, max_bid_count=10, bid_count=10)
    ]
    db_session.add_all(ads)
    db_session.commit()

    q = db_session.query(Ad).filter(
        Ad.status,
        Ad.bid_count < Ad.max_bid_count
    )
    cnt = 0
    for ad in q.yield_per(BATCH_SIZE):
        assert ad.bid_count < ad.max_bid_count, "Exceed bid count."
        cnt += 1
    assert cnt == 2, "Match number is different."
