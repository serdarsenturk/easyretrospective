import base62
from flask import Blueprint, jsonify
from sqlalchemy import Sequence
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.board import Board
from app.models.member import Member
from app.models.column import Column
from app.models.card import Card
from app.schema.board import board_schema, boards_schema

boards = Blueprint('boards', __name__)

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

@boards.route('/api/v1/members/<member_id>/boards', methods=["POST"])
def create_board(member_id):
    new_board = Board(member_id=member_id)

    return board_schema.dump(generate_board_code(new_board))

@boards.route('/api/v1/boards/<code>', methods=["GET"])
def get_board_by_code(code):
    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .first()

    return jsonify(board_schema.dump(board))

@boards.route('/api/v1/members/<member_id>/boards', methods=["GET"])
def get_member_boards(member_id):
    member_boards = db.session.query(Board) \
        .filter(Board.member_id == member_id ) \
        .all()

    return jsonify(boards_schema.dump(member_boards))