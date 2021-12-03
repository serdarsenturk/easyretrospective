import base62
from flask import Blueprint, jsonify
from sqlalchemy import Sequence
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.board import Board
from app.models.member import Member
from app.schema.board import board_schema, boards_schema

boards = Blueprint('boards', __name__, url_prefix='/api/v1/boards/')

def generate_board_code(board):
    try:
        board.id = db.session.execute(Sequence("boards_id_seq"))
        board.code = base62.encode(hash(('boards', board.id)), 8)[-8:]

        db.session.add(board)
        db.session.commit()

        return board

    except IntegrityError:
        db.session.rollback()
        return generate_board_code(board)

@boards.route('members/<member_id>', methods=["POST"])
def create_board(member_id):

    new_board = Board(member_id=member_id)

    return board_schema.dump(generate_board_code(new_board))

@boards.route('<code>/members/<memberId>/', methods=["GET"])
def get_board_by_code(memberId, code):
    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .filter(Board.member_id == memberId) \
        .first()

    return jsonify(board_schema.dump(board))

@boards.route('members/<memberId>', methods=["GET"])
def get_member_boards(memberId):
    member_boards = db.session.query(Board) \
        .filter(Board.member_id == memberId ) \
        .all()

    return jsonify(boards_schema.dump(member_boards))

@boards.route('/teams/1', methods=["GET"])
def get_teams_boards():
    team_boards = db.session.query(Board).all()

    return jsonify(boards_schema.dump(team_boards))