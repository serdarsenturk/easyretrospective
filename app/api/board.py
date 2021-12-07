import base62
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from sqlalchemy import Sequence
from sqlalchemy.exc import IntegrityError
from app import db, app
from app.models.board import Board
from app.models.column import Column
from app.schema.board import board_schema, boards_schema

boards = Blueprint('boards', __name__)
CORS(boards, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}})

def generate_board_code(board):
    try:
        board.name = "Retro 5/11/21"
        board.id = db.session.execute(Sequence("boards_id_seq"))
        board.code = base62.encode(hash(('boards', board.id)), 8)[-8:]

        column1 = Column(name = "What went well", board_id= board.id)
        column2 = Column(name = "What didn't go well ", board_id= board.id)
        column3 = Column(name = "To improve", board_id= board.id)

        board.columns = [column1, column2, column3]

        db.session.add(column1)
        db.session.add(column2)
        db.session.add(column3)
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

@boards.route('/api/v1/members/<id>/boards/<code>', methods=["DELETE"])
def delete_board_by_code(id, code):
    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .filter(Board.member_id == id) \
        .first()

    db.session.delete(board)
    db.session.commit()

    return jsonify(board_schema.dump(board))

@boards.route('/api/v1/boards/<code>', methods=["GET"])
def get_board_by_code(code):
    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .first()

    return jsonify(board_schema.dump(board))

@boards.route('/api/v1/members/<member_id>/boards/<code>/name', methods=["PUT"])
def modify_board_name_by_code(member_id, code):
    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .filter(Board.member_id == member_id) \
        .first()

    modified_name = request.json['name']

    board.name = modified_name

    db.session.commit()

    return jsonify(board_schema.dump(board))

@boards.route('/api/v1/members/<member_id>/boards', methods=["GET"])
def get_member_boards(member_id):
    member_boards = db.session.query(Board) \
        .filter(Board.member_id == member_id ) \
        .all()

    return jsonify(boards_schema.dump(member_boards))

