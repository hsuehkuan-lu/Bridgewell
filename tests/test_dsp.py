import pytest
import json
from tests.conftest import client
from app import app
from config import API_URL


def test_dsp(client):
    r = client.post(
        f'{API_URL}/bw_dsp',
        data={
            'bid_floor': 10
        }
    )
