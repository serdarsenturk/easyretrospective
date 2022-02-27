from app import db, app
from flask_cors import CORS
from sqlalchemy import Sequence
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from datetime import datetime
import base62
from app.schema.board import board_schema
from app.schema.member_board import member_boards_schema
from app.schema.team_board import team_boards_schema
from app.models.board import Board
from app.models.column import Column
from app.models.member import Member
from app.models.team import Team

boards = Blueprint('boards', __name__)
CORS(boards, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}})

def add_default_properties(board):
        generate_board_code(board)

        date = datetime.now()
        board.date = date
        board.name = f"Retro {date.strftime('%d/%m/%y')}"

        columns = [Column(name = "What went well", board_id= board.id), Column(name = "What didn't go well ", board_id= board.id), Column(name = "To improve", board_id= board.id)]
        board.columns = columns

        db.session.add(board)
        db.session.commit()

        return board

def generate_board_code(board):
    try:
        board.id = db.session.execute(Sequence("boards_id_seq"))
        board.code = base62.encode(hash(('boards', board.id)), 8)[-8:]

        return board

    except IntegrityError:
        db.session.rollback()
        return generate_board_code(board)

@boards.route('/api/v1/members/<member_id>/boards', methods=["POST"])
def create_board(member_id):
    new_board = Board(member_id=member_id)

    return board_schema.dump(add_default_properties(new_board))

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

    return jsonify(member_boards_schema.dump(member_boards))

@boards.route('/api/v1/teams/<team_id>/boards', methods=["GET"])
def get_team_boards(team_id):
    team_boards = db.session.query(Board) \
        .filter(Board.team_id == team_id ) \
        .all()

    return jsonify(team_boards_schema.dump(team_boards))