from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('game', __name__)


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

    return render_template('game/index.html', game_sessions=game_sessions)


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
        tier1_ap = request.form['tier1_ap']
        tier2_ap = request.form['tier2_ap']
        tier3_ap = request.form['tier3_ap']
        tier4_ap = request.form['tier4_ap']
        gold = request.form['gold']
        magic_count = request.form['magic_count']
        tier1_tp = request.form['tier1_tp']
        tier2_tp = request.form['tier2_tp']
        tier3_tp = request.form['tier3_tp']
        tier4_tp = request.form['tier4_tp']
        renown = request.form['renown']
        downtime = request.form['downtime']
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
        tier1_ap = request.form['tier1_ap']
        tier2_ap = request.form['tier2_ap']
        tier3_ap = request.form['tier3_ap']
        tier4_ap = request.form['tier4_ap']
        gold = request.form['gold']
        magic_count = request.form['magic_count']
        tier1_tp = request.form['tier1_tp']
        tier2_tp = request.form['tier2_tp']
        tier3_tp = request.form['tier3_tp']
        tier4_tp = request.form['tier4_tp']
        renown = request.form['renown']
        downtime = request.form['downtime']
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
                    g.user['id']
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
