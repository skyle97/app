import email
from email.message import Message
from typing import Optional, List

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import s3
from app.dashboard.base import dashboard_bp
from app.extensions import db
from app.models import Contact, EmailLog, RefusedEmail
from app.pgp_utils import PGPException, load_public_key_and_check


def iter_message_parts(message):
    if message.is_multipart():
        for message in message.get_payload():
            for part in iter_message_parts(message):
                yield part
    else:
        yield message


def get(msg: Message, types: List[str]) -> Optional[str]:
    for part in iter_message_parts(msg):
        if part.get_content_type() in types:
            return part.get_payload(decode=True).decode()


def get_html(msg: Message) -> Optional[str]:
    return get(msg, ("text/html", "application/xhtml+xml"))


def get_plain(msg: Message) -> Optional[str]:
    return get(msg, ("text/plain", "text/text"))


@dashboard_bp.route("/email_log/<int:email_log_id>/", methods=["GET", "POST"])
@login_required
def email_viewer_route(email_log_id):
    # todo: add check
    # if not contact or contact.user_id != current_user.id:
    #     flash("You cannot see this page", "warning")
    #     return redirect(url_for("dashboard.index"))

    email_log = EmailLog.get(email_log_id)
    refused_email: RefusedEmail = email_log.refused_email

    msg = email.message_from_file(s3.read(refused_email.path))

    print(get_html(msg))

    return render_template(
        "dashboard/email_viewer.html",
        msg=msg,
        html=get_html(msg),
        plain=get_plain(msg),
        email_log=email_log,
    )
