from app import db, app
from flask_cors import CORS
from pusher import Pusher
from sqlalchemy import Sequence, desc
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from datetime import datetime
import base62
from app.schema.board import board_schema, boards_schema
from app.schema.member_board import member_boards_schema
from app.schema.team import teams_schema
from app.models.board import Board
from app.models.column import Column
from app.models.member import Member
from app.models.team import Team

boards = Blueprint('boards', __name__)
CORS(boards, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}})

pusher = Pusher(
    app_id=app.config.get('PUSHER_APP_ID'),
    key=app.config.get('PUSHER_KEY'),
    secret=app.config.get('PUSHER_SECRET'),
    cluster='eu',
    ssl=True
)

def add_default_properties(board):
    generate_board_code(board)

    date = datetime.now()
    board.date = date
    board.name = f"Retro {date.strftime('%d/%m/%y')}"

    columns = [Column(name = "What went well", board_id= board.id), Column(name = "What didn't go well ", board_id= board.id), Column(name = "To improve", board_id= board.id)]
    board.columns = columns

    db.session.add(board)

    try:
        db.session.commit()
        return board
    except IntegrityError:
        db.session.rollback()
        return add_default_properties(board)

def generate_board_code(board):
    board.id = db.session.execute(Sequence("boards_id_seq"))
    board.code = base62.encode(hash(('boards', board.id)), 8)[-8:]

    return board

@boards.route('/api/v1/members/<member_id>/boards', methods=["POST"])
def create_board(member_id):
    member = db.session.query(Member) \
        .filter(Member.id == member_id) \
        .first()

    if member:
        team_id = request.json["team_id"]
        temp_board = Board(member_id=member_id, team_id=team_id)

        try:
            new_board = add_default_properties(temp_board)
            pusher.trigger(f"member-{member_id}", "board-created",
                           {
                               "code": new_board.code,
                               "date": new_board.date.__str__(),
                               "member_id": new_board.member_id,
                               "name": new_board.name,
                               "team_id": new_board.team_id,
                           }
                           )

            return board_schema.dump(new_board), 201
        except Exception:
            return '', 400
    else:
        return 'Please verify your identity', 401

@boards.route('/api/v1/members/<member_id>/boards/<code>', methods=["DELETE"])
def delete_board_by_code(member_id, code):
    member = db.session.query(Member) \
        .filter(Member.boards.any(Board.code == code)) \
        .filter(Member.id == member_id) \
        .first()

    if not member:
        return 'Please verify your identity', 401

    to_delete_board = db.session.query(Board) \
        .filter(Board.code == code) \
        .first()

    db.session.delete(to_delete_board)
    db.session.commit()

    pusher.trigger(f"member-{member_id}", "board-deleted", {"code": code, "member_id": member_id})

    return 'Board deleted', 200

@boards.route('/api/v1/boards/<code>', methods=["GET"])
def get_board_by_code(code):
    member_id = request.headers.get('member_id')

    member = db.session.query(Member) \
        .filter(Member.boards.any(Board.code == code)) \
        .filter(Member.id == member_id) \
        .first()

    if not member:
        return 'Please verify your identity', 401

    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .first()

    return jsonify(board_schema.dump(board))

@boards.route('/api/v1/members/<member_id>/boards/<code>/name', methods=["PUT"])
def modify_board_name_by_code(member_id, code):
    member = db.session.query(Member) \
        .filter(Member.id == member_id) \
        .first()

    if not member:
        return 'Please verify your identity', 401

    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .filter(Board.member_id == member_id) \
        .first()

    modified_name = request.json['name']

    board.name = modified_name

    try:
        db.session.commit()

        pusher.trigger(f"member-{member_id}", "board-updated", {"code": code, "name": board.name, "date": board.date.__str__()})

        return jsonify(board_schema.dump(board)), 201
    except IntegrityError:
        db.session.rollback()
        return 'Oops, an error occurred', 500

@boards.route('/api/v1/members/<member_id>/boards', methods=["GET"])
def get_member_boards(member_id):
    member = db.session.query(Member) \
        .filter(Member.id == member_id) \
        .first()

    if not member:
        return 'Please verify your identity', 401

    member_boards = db.session.query(Board) \
        .filter(Board.member_id == member_id) \
        .filter(Board.team_id == None) \
        .order_by(desc(Board.date)) \
        .limit(8)

    return jsonify(member_boards_schema.dump(member_boards))

@boards.route('/api/v1/teams/<team_id>/boards', methods=["GET"])
def get_team_boards(team_id):
    try:
        member_id = request.headers.get('member_id')
    except:
        return 'Please verify your identity', 401

    member = db.session.query(Member) \
        .filter(Member.teams.any(Team.id == team_id)) \
        .filter(Member.id == member_id) \
        .first()

    if not member:
            return 'Member does not exists', 404

    team_boards = db.session.query(Board) \
        .filter(Board.team_id == team_id) \
        .filter(Board.member_id == member_id) \
        .order_by(desc(Board.date)) \
        .limit(8)

    return jsonify(boards_schema.dump(team_boards)), 200

@boards.route('/api/v1/members/<member_id>/teams', methods=["GET"])
def get_teams(member_id):
    member = db.session.query(Member) \
        .filter(Member.id == member_id) \
        .first()

    if member:
        try:
            return jsonify(teams_schema.dump(member.teams))
        except:
            return 'Teams not found', 404
    else:
        return 'Please verify your identity', 401
