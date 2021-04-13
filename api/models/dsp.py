from api import db


class Ad(db.Model):
    __tablename__ = 'ad'
    """
    | Column name  | Type |               Comment              |
    |--------------|------|------------------------------------|
    | ad_id        | int  | The id of advertising ad           |
    | status       | bool | Bidding switch                     |
    | bidding_cpm  | int  | Cost per 1000 impression           |
    """
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean, nullable=False)
    bidding_cpm = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Ad(id={self.ad_id})> status={self.status} bidding_cpm={self.bidding_cpm}"
