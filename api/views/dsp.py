from flask import request, jsonify, abort, Blueprint
from api.models.dsp import Ad
from database import db
import random

BATCH_SIZE = 1000

dsp_app = Blueprint('dsp_app', __name__)


def orm_select_ad(bid_floor):
    bid_floor = int(bid_floor)
    q = Ad.query.filter(
        Ad.status,
        Ad.bid_count < Ad.max_bid_count
    )
    bid_price = 0
    target_ad = None
    for ad in q.yield_per(BATCH_SIZE):
        price = ad.bidding_cpm * random.randint(1, 10)
        if price >= bid_floor and price > bid_price:
            bid_price = price
            target_ad = ad
    if target_ad is None:
        return {}, 204
    db.session.query(Ad).filter(
        Ad.ad_id == target_ad.ad_id
    ).update({'bid_count': Ad.bid_count + 1})
    db.session.commit()
    return jsonify({
        'price': bid_price,
        'ad_id': target_ad.ad_id
    })


def raw_sql_select_ad(bid_floor):
    bid_floor = int(bid_floor)
    sql = '''
        select * from ad
            where ad.status = True;
    '''
    cursor = db.session.execute(sql).cursor
    records = cursor.fetchmany(BATCH_SIZE)
    bid_price = 0
    target_ad_id = None
    while records:
        for row in records:
            price = row[2] * random.randint(1, 10)
            if price >= bid_floor and price > bid_price:
                bid_price = price
                target_ad_id = row[0]
        records = cursor.fetchmany(BATCH_SIZE)
    cursor.close()
    if target_ad_id is None:
        return {}, 204
    return jsonify({
        'price': bid_price,
        'ad_id': target_ad_id
    })


def add_ads(data_num):
    data_num = int(data_num)
    ads = []
    for _ in range(data_num):
        ads += [Ad(
            status=bool(random.getrandbits(1)),
            bidding_cpm=random.randint(0, 10),
            max_bid_count=random.randint(1, 1000)
        )]
    db.session.add_all(ads)
    db.session.commit()


def delete_ads():
    Ad.query.delete()
    db.session.commit()


@dsp_app.route('/bw_dsp', methods=['POST'])
def bw_dsp():
    bid_floor = request.values.get('bid_floor')
    if bid_floor is None or not bid_floor.isdigit():
        abort(400)
    return orm_select_ad(bid_floor)


@dsp_app.route('/add_ad_data', methods=['POST'])
def add_ad_data():
    data_num = request.values.get('data_num', 10)
    try:
        add_ads(data_num)
    except Exception as e:
        abort(500, e)
    return jsonify(success=True)


@dsp_app.route('/delete_ad_data', methods=['POST'])
def delete_ad_data():
    try:
        delete_ads()
    except Exception as e:
        abort(500, e)
    return jsonify(success=True)


@dsp_app.route('/test')
def test():
    return jsonify({'test': [1, 2, 3]})
