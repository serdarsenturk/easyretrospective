from flask import Blueprint, request, jsonify
from app import db
from app.models.board import Board
from app.models.column import Column
from app.schema.column import column_schema

columns = Blueprint('columns', __name__, url_prefix='/api/v1/members/<member_id>/boards/<code>/columns')

@columns.route('', methods=["POST"])
def create_column(member_id, code):
    column_name = request.json['column_name']
    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .filter(Board.member_id == member_id) \
        .first()

    board_id = board.id
    new_column = Column(column_name = column_name, board_id=board_id)

    db.session.add(new_column)
    db.session.commit()

    return jsonify(column_schema.dump(new_column))

@columns.route('<column_id>', methods=['DELETE'])
def delete_column_by_id(member_id, code, column_id):
    column = db.session.query(Board) \
        .filter(Board.code == code ) \
        .filter(Board.member_id == member_id) \
        .filter(Column.id == column_id) \
        .first()

    db.session.delete(column)
    db.session.commit()

    return jsonify(column_schema.dump(column))


@columns.route('<column_id>/name', methods=['PUT'])
def modify_column_by_id(member_id, code, column_id):
    column = db.session.query(Board) \
        .filter(Board.code == code ) \
        .filter(Board.member_id == member_id) \
        .filter(Column.id == column_id) \
        .first()

    column.column_name = request.json['column_name']

    db.session.commit()

    return jsonify(column_schema.dump(column))