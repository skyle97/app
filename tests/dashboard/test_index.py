from flask import url_for, g

from app.models import (
    Alias,
)
from tests.utils import login


def test_create_random_alias_success(flask_client):
    login(flask_client)
    assert Alias.count() == 1

    r = flask_client.post(
        url_for("dashboard.index"),
        data={"form-name": "create-random-email"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert Alias.count() == 2


def test_too_many_requests(flask_client):
    login(flask_client)

    # can't create more than 5 aliases in 1 minute
    for i in range(7):
        r = flask_client.post(
            url_for("dashboard.index"),
            data={"form-name": "create-random-email"},
            follow_redirects=True,
        )

        # to make flask-limiter work with unit test
        # https://github.com/alisaifee/flask-limiter/issues/147#issuecomment-642683820
        g._rate_limiting_complete = False
    else:
        # last request
        assert r.status_code == 429
        assert "Whoa, slow down there, pardner!" in str(r.data)
