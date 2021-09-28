from uuid import uuid4

import arrow
from flask import make_response, redirect, url_for, render_template
from flask_login import login_required

from app.config import URL
from app.dashboard.base import dashboard_bp


@dashboard_bp.route("/setup_done", methods=["GET", "POST"])
@login_required
def setup_done():
    response = make_response(redirect(url_for("dashboard.index")))

    response = make_response(
        render_template(
            "dashboard/setup_done.html",
        )
    )

    response.set_cookie(
        f"setup_done_{uuid4()}",
        value="true",
        expires=arrow.now().shift(days=30).datetime,
        secure=True if URL.startswith("https") else False,
        httponly=True,
        samesite="Lax",
    )

    return response
