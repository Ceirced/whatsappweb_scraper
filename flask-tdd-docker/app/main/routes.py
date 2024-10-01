from flask import render_template
from app.main import bp
from app.models import get_feed, format_timestamp


@bp.route("/")
@bp.route("/index")
def index():
    feed_data = get_feed()
    human_timestamp = {
        post.timestamp: format_timestamp(post.timestamp) for post in feed_data
    }
    return render_template(
        "feed.html", feed_data=feed_data, human_timestamp=human_timestamp
    )


@bp.route("/profile/<string:username>")
def profile(username):
    feed_data = get_feed(username)

    human_timestamp = {
        post.timestamp: format_timestamp(post.timestamp) for post in feed_data
    }
    return render_template(
        "profile.html", feed_data=feed_data, human_timestamp=human_timestamp
    )
