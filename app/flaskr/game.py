from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('game', __name__)


CHAR_ADV = {
    "level 1": {
        "xp": 0,
        "apt": 0,
        "ap_next": 4
    },
    "level 2": {
        "xp": 300,
        "apt": 4,
        "ap_next": 4
    },
    "level 3": {
        "xp": 900,
        "apt": 8,
        "ap_next": 4
    },
    "level 4": {
        "xp": 2700,
        "apt": 12,
        "ap_next": 4
    },
    "level 5": {
        "xp": 6500,
        "apt": 16,
        "ap_next": 8
    },
    "level 6": {
        "xp": 14000,
        "apt": 24,
        "ap_next": 8
    },
    "level 7": {
        "xp": 23000,
        "apt": 32,
        "ap_next": 8
    },
    "level 8": {
        "xp": 34000,
        "apt": 40,
        "ap_next": 8
    },
    "level 9": {
        "xp": 48000,
        "apt": 48,
        "ap_next": 8
    },
    "level 10": {
        "xp": 64000,
        "apt": 56,
        "ap_next": 8
    },
    "level 11": {
        "xp": 85000,
        "apt": 64,
        "ap_next": 8
    },
    "level 12": {
        "xp": 100000,
        "apt": 72,
        "ap_next": 8
    },
    "level 13": {
        "xp": 120000,
        "apt": 80,
        "ap_next": 8
    },
    "level 14": {
        "xp": 140000,
        "apt": 88,
        "ap_next": 8
    },
    "level 15": {
        "xp": 165000,
        "apt": 96,
        "ap_next": 8
    },
    "level 16": {
        "xp": 195000,
        "apt": 104,
        "ap_next": 8
    },
    "level 17": {
        "xp": 225000,
        "apt": 112,
        "ap_next": 8
    },
    "level 18": {
        "xp": 265000,
        "apt": 120,
        "ap_next": 8
    },
    "level 19": {
        "xp": 305000,
        "apt": 128,
        "ap_next": 8
    },
    "level 20": {
        "xp": 355000,
        "apt": 136,
        "ap_next": 8
    },
}


def __get_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0


def __get_int(value):
    try:
        return int(value)
    except ValueError:
        return 0


@bp.route('/')
def index():
    db = get_db()
    game_sessions = db.execute(
        'SELECT g.id, u.username,'
        ' player_id, created, play_date, adventure_name, adventure_code, session_number, gm_name, gm_dci,'
        ' experience, tier1_ap, tier2_ap, tier3_ap, tier4_ap,'
        ' gold, magic_count, tier1_tp, tier2_tp, tier3_tp, tier4_tp,'
        ' renown, downtime,'
        ' story_awards, acquired_items, removed_items, downtime_activity, notes'
        ' FROM game g JOIN user u ON g.player_id = u.id'
        ' ORDER BY created ASC'
    ).fetchall()

    totals = {
        "experience": 0,
        "ap": 0,
        "gold": 0,
        "tp1": 0,
        "tp2": 0,
        "tp3": 0,
        "tp4": 0,
        "magic_count": 0,
        "downtime": 0,
        "renown": 0
    }
    for session in game_sessions:

        totals["experience"] += __get_int(session["experience"])
        totals["ap"] += (__get_int(session["tier1_ap"]) + __get_int(session["tier2_ap"])
                         + __get_int(session["tier3_ap"]) + __get_int(session["tier4_ap"]))
        totals["gold"] += __get_float(session["gold"])
        totals["tp1"] += __get_int(session["tier1_tp"])
        totals["tp2"] += __get_int(session["tier2_tp"])
        totals["tp3"] += __get_int(session["tier3_tp"])
        totals["tp4"] += __get_int(session["tier4_tp"])
        totals["magic_count"] += __get_int(session["magic_count"])
        totals["downtime"] += __get_int(session["downtime"])
        totals["renown"] += __get_int(session["renown"])

    return render_template('game/index.html', game_sessions=game_sessions, totals=totals)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        error = None
        play_date = request.form['play_date']
        adventure_name = request.form['adventure_name']
        adventure_code = request.form['adventure_code']
        session_number = request.form['session_number']
        gm_name = request.form['gm_name']
        gm_dci = request.form['gm_dci']
        experience = request.form['experience']
        tier1_ap = __get_int(request.form['tier1_ap'])
        tier2_ap = 0
        tier3_ap = 0
        tier4_ap = 0
        gold = __get_float(request.form['gold'])
        magic_count = __get_int(request.form['magic_count'])
        tier1_tp = __get_int(request.form['tier1_tp'])
        tier2_tp = __get_int(request.form['tier2_tp'])
        tier3_tp = __get_int(request.form['tier3_tp'])
        tier4_tp = __get_int(request.form['tier4_tp'])
        renown = __get_int(request.form['renown'])
        downtime = __get_int(request.form['downtime'])
        story_awards = request.form['story_awards']
        acquired_items = request.form['acquired_items']
        removed_items = request.form['removed_items']
        downtime_activity = request.form['downtime_activity']
        notes = request.form['notes']

        if not adventure_name:
            error = 'Adventure name is required.'
            # TODO: ensure input type, date field added as date to allow sort ability

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO game ('
                ' play_date, adventure_name, adventure_code, session_number, gm_name, gm_dci,'
                ' experience, tier1_ap, tier2_ap, tier3_ap, tier4_ap,'
                ' gold, magic_count, tier1_tp, tier2_tp, tier3_tp, tier4_tp,'
                ' renown, downtime,'
                ' story_awards, acquired_items, removed_items, downtime_activity, notes,'
                ' player_id'
                ' )'
                ' VALUES ('
                ' ?, ?, ?, ?, ?, ?,'
                ' ?, ?, ?, ?, ?,'
                ' ?, ?, ?, ?, ?, ?,'
                ' ?, ?,'
                ' ?, ?, ?, ?, ?,'
                ' ?'
                ' )',
                (
                    play_date, adventure_name, adventure_code, session_number, gm_name, gm_dci,
                    experience, tier1_ap, tier2_ap, tier3_ap, tier4_ap,
                    gold, magic_count, tier1_tp, tier2_tp, tier3_tp, tier4_tp,
                    renown, downtime,
                    story_awards, acquired_items, removed_items, downtime_activity, notes,
                    g.user['id']
                )
            )
            db.commit()
            return redirect(url_for('game.index'))

    return render_template('game/create.html')


def get_game(id, check_player=True):
    game_session = get_db().execute(
        'SELECT g.id, player_id,'
        ' created, play_date, adventure_name, adventure_code, session_number, gm_name, gm_dci,'
        ' experience, tier1_ap, tier2_ap, tier3_ap, tier4_ap,'
        ' gold, magic_count, tier1_tp, tier2_tp, tier3_tp, tier4_tp,'
        ' renown, downtime,'
        ' story_awards, acquired_items, removed_items, downtime_activity, notes'
        ' FROM game g JOIN user u ON g.player_id = u.id'
        ' WHERE g.id = ?',
        (id,)
    ).fetchone()

    if game_session is None:
        abort(404, "Game session id {0} doesn't exist.".format(id))

    if check_player and game_session['player_id'] != g.user['id']:
        abort(403)

    return game_session


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    game_session = get_game(id)

    if request.method == 'POST':
        error = None
        play_date = request.form['play_date']
        adventure_name = request.form['adventure_name']
        adventure_code = request.form['adventure_code']
        session_number = request.form['session_number']
        gm_name = request.form['gm_name']
        gm_dci = request.form['gm_dci']
        experience = request.form['experience']
        tier1_ap = __get_int(['tier1_ap'])
        tier2_ap = 0
        tier3_ap = 0
        tier4_ap = 0
        gold = __get_float(request.form['gold'])
        magic_count = __get_int(request.form['magic_count'])
        tier1_tp = __get_int(request.form['tier1_tp'])
        tier2_tp = __get_int(request.form['tier2_tp'])
        tier3_tp = __get_int(request.form['tier3_tp'])
        tier4_tp = __get_int(request.form['tier4_tp'])
        renown = __get_int(request.form['renown'])
        downtime = __get_int(request.form['downtime'])
        story_awards = request.form['story_awards']
        acquired_items = request.form['acquired_items']
        removed_items = request.form['removed_items']
        downtime_activity = request.form['downtime_activity']
        notes = request.form['notes']

        if not adventure_name:
            error = 'Adventure name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE game SET'
                ' play_date = ?, adventure_name = ?, adventure_code = ?, session_number = ?, gm_name = ?, gm_dci = ?,'
                ' experience = ?, tier1_ap = ?, tier2_ap = ?, tier3_ap = ?, tier4_ap = ?,'
                ' gold = ?, magic_count = ?, tier1_tp = ?, tier2_tp = ?, tier3_tp = ?, tier4_tp = ?,'
                ' renown = ?, downtime = ?,'
                ' story_awards = ?, acquired_items = ?, removed_items = ?, downtime_activity = ?, notes = ?'
                ' WHERE id = ?',
                (
                    play_date, adventure_name, adventure_code, session_number, gm_name, gm_dci,
                    experience, tier1_ap, tier2_ap, tier3_ap, tier4_ap,
                    gold, magic_count, tier1_tp, tier2_tp, tier3_tp, tier4_tp,
                    renown, downtime,
                    story_awards, acquired_items, removed_items, downtime_activity, notes,
                    id
                )
            )
            db.commit()
            return redirect(url_for('game.index'))

    return render_template('game/update.html', gs=game_session)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_game(id)
    db = get_db()
    db.execute('DELETE FROM game WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('game.index'))
