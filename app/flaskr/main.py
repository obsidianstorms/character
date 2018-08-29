import functools
import json
import pendulum

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    if g.user:
        return render_template('main/index.html')

    return redirect(url_for('auth.login'))


@bp.route('/export', methods=('GET', 'POST'))
def export():
    export_games()
    return render_template('main/index.html')


@bp.route('/load', methods=('GET', 'POST'))
def load():
    return render_template('main/index.html')


def export_games():
    db = get_db()
    game_sessions = db.execute(
        'SELECT g.id as session_id, u.username,'
        ' player_id as character_id, created, play_date, adventure_name, adventure_code, session_number, gm_name, gm_dci,'
        ' experience, tier1_ap, tier2_ap, tier3_ap, tier4_ap,'
        ' gold, magic_count, tier1_tp, tier2_tp, tier3_tp, tier4_tp,'
        ' renown, downtime,'
        ' story_awards, acquired_items, removed_items, downtime_activity, notes'
        ' FROM game g JOIN user u ON g.player_id = u.id'
        ' ORDER BY created ASC'
    ).fetchall()

    sessions = []
    for row in game_sessions:
        sessions.append(
            {
                "session_id": row['session_id'],
                "character_id": row['character_id'],
                "character": row['username'],
                "play_date": row['play_date'],
                "adventure_name": row['adventure_name'],
                "adventure_code": row['adventure_code'],
                "session_number": row['session_number'],
                "gm_name": row['gm_name'],
                "gm_dci": row['gm_dci'],
                "experience": row['experience'],
                "ap": row['tier1_ap'],
                "gold": row['gold'],
                "magic_count": row['magic_count'],
                "tier1_tp": row['tier1_tp'],
                "tier2_tp": row['tier2_tp'],
                "tier3_tp": row['tier3_tp'],
                "tier4_tp": row['tier4_tp'],
                "downtime": row['downtime'],
                "renown": row['renown'],
                "story_awards": row['story_awards'],
                "acquired_items": row['acquired_items'],
                "removed_items": row['removed_items'],
                "downtime_activity": row['downtime_activity'],
                "notes": row['notes']
            }
        )

    print(json.dumps({'sessions': sessions}))
    print(pendulum.today().format('YYYY-MM-DD'))




