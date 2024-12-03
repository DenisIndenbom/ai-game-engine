from flask import Blueprint
from flask import render_template

from helpers import *
from methods.exceptions import NotFound
from methods.games import get_games, get_game_by_id
from methods.sessions import get_sessions, get_session_by_id, can_restart_session
from methods.sessions import grab_sessions, create_session, restart_session
from methods.teams import get_team_by_id

sessions_blueprint = Blueprint('sessions', __name__)


@sessions_blueprint.route('/')
@requires_auth
def my(user):
    return render_template('sessions/index.html', title="Мои игровые сессии", sessions=grab_sessions(user), user=user)


@sessions_blueprint.route('/active')
def active():
    return render_template('sessions/index.html', sessions=get_sessions('started'), title='Активные сессии')


@sessions_blueprint.route('/archive')
def archive():
    return render_template('sessions/index.html', sessions=get_sessions('ended'), title='Завершенные сессии')


@sessions_blueprint.route('/create', methods=['get'])
@requires_auth
def create_page(*_):
    return render_template('sessions/create.html', games=get_games())


@sessions_blueprint.route('/create', methods=['post'])
@requires_auth
def create(user):
    game_id = request.form.get('game_id')
    games = get_games()

    try:
        selected_game = get_game_by_id(game_id)
    except NotFound:
        return render_template('sessions/create.html', games=games, error="Выберите игру")

    teams_ids = request.form.getlist('teams')
    if not teams_ids:
        return render_template('sessions/create.html', game=selected_game)

    try:
        teams = [get_team_by_id(team_id) for team_id in teams_ids]

        game_session = create_session(selected_game, teams, user)

        return redirect(f'/games/{game_session.id}')
    except Exception as e:
        print(e)
        return render_template('sessions/create.html', game=selected_game, error="Ошибка запуска")


@sessions_blueprint.route('/<int:session_id>/restart')
@requires_auth
def get_stats(user, session_id):
    session = get_session_by_id(session_id)

    if can_restart_session(session, user):
        restart_session(session)

    return redirect('/sessions')
