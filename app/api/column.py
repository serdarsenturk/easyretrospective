from flask import Blueprint, request, jsonify
from flask_cors import CORS
from pusher import Pusher
from app import db, app
from app.models.board import Board
from app.models.column import Column
from app.schema.column import column_schema
from app.schema.column_updated import column_updated_schema

columns = Blueprint('columns', __name__, url_prefix='/api/v1/members/<member_id>/boards/<code>/columns')
CORS(columns, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}}, supports_credentials=True)

pusher = Pusher(
    app_id=app.config.get('PUSHER_APP_ID'),
    key=app.config.get('PUSHER_KEY'),
    secret=app.config.get('PUSHER_SECRET'),
    cluster='eu',
    ssl=True
)

@columns.route('', methods=["POST"])
def create_column(member_id, code):
    requester_id = request.cookies.get('member_id')

    if member_id != requester_id:
        return 'Unauthorized request', 401

    name = request.json['name']

    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .filter(Board.member_id == member_id) \
        .first()

    board_id = board.id

    new_column = Column(name = name, board_id=board_id)

    try:
        db.session.add(new_column)
        db.session.commit()

        pusher.trigger(f"board-{code}", 'column-created', {"id": new_column.id, "name": name, "cards": []})

        return jsonify(column_schema.dump(new_column))
    except:
        db.session.rollback()

@columns.route('<column_id>', methods=['DELETE'])
def delete_column_by_id(member_id, code, column_id):
    requester_id = request.cookies.get('member_id')

    if member_id != requester_id:
        return 'Unauthorized request', 401

    column = db.session.query(Column) \
        .filter(Board.code == code ) \
        .filter(Board.member_id == member_id) \
        .filter(Column.id == column_id) \
        .first()

    try:
        db.session.delete(column)
        db.session.commit()

        pusher.trigger(f"board-{code}", 'column-deleted', {"id": column_id, "name": column.name, "cards": []})

        return jsonify(column_updated_schema.dump(column))
    except:
        db.session.rollback()


@columns.route('<column_id>/name', methods=['PUT'])
def modify_column_by_id(member_id, code, column_id):
    requester_id = request.cookies.get('member_id')

    if member_id != requester_id:
        return 'Unauthorized request', 401

    column = db.session.query(Column) \
        .filter(Board.code == code ) \
        .filter(Board.member_id == member_id) \
        .filter(Column.id == column_id) \
        .first()

    name = request.json['name']

    try:
        column.name = name

        db.session.commit()

        pusher.trigger(f"board-{code}", 'column-updated', {"id": column.id, "name": name})

        return jsonify(column_updated_schema.dump(column))
    except:
        db.session.rollback()