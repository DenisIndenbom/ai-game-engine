from models import db


def update_session_stats(session, stats):
    session.stats = stats
    db.session.commit()
