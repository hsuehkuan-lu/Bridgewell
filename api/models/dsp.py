from database import Base
from sqlalchemy import *


class Ad(Base):
    __tablename__ = 'ad'
    """
    | Column name  | Type |               Comment              |
    |--------------|------|------------------------------------|
    | ad_id        | int  | The id of advertising ad           |
    | status       | bool | Bidding switch                     |
    | bidding_cpm  | int  | Cost per 1000 impression           |
    """
    ad_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Boolean, nullable=False)
    bidding_cpm = Column(Integer, nullable=False)
    max_bid_count = Column(Integer, nullable=False)
    bid_count = Column(Integer, nullable=False, server_default='0')

    def __repr__(self):
        return f"<Ad(id={self.ad_id})> status={self.status} bidding_cpm={self.bidding_cpm}"
