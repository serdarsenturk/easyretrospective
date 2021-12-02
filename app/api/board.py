import base62
from flask import Blueprint, request, jsonify
from sqlalchemy import Sequence
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.board import Board
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

