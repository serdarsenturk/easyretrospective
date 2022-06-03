from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app import db, app
from app.models.board import Board
from app.models.card import Card
from app.models.column import Column
from app.models.member import Member
from app.schema.card import card_schema
from pusher import Pusher
from app.decorators.authentication_decorators import token_required

cards = Blueprint('cards', __name__, url_prefix='/api/v1/members/<member_id>/boards/<code>/columns/<column_id>/cards')
CORS(cards, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}}, supports_credentials=True)

pusher = Pusher(
    app_id=app.config.get('PUSHER_APP_ID'),
    key=app.config.get('PUSHER_KEY'),
    secret=app.config.get('PUSHER_SECRET'),
    cluster='eu',
    ssl=True
)


@cards.route('', methods=["POST"])
@token_required
def create_card(member_id, code, column_id):
    content = request.json['content']

    new_card = Card(content=content, member_firebase_id=member_id, column_id=column_id)

    try:
        db.session.add(new_card)
        db.session.commit()

        pusher.trigger(f"board-{code}-{column_id}", 'card-created',
                       {"column_id": column_id, "content": content, "id": new_card.id, "member_id": member_id})

        return jsonify(card_schema.dump(new_card))
    except:
        db.session.rollback()


@cards.route('<card_id>', methods=["DELETE"])
@token_required
def delete_card_by_id(member_id, code, column_id, card_id):
    card = db.session.query(Card) \
        .filter(Card.id == card_id) \
        .filter(Column.id == column_id) \
        .filter(Board.code == code) \
        .filter(Member.firebase_user_id == member_id) \
        .first()

    try:
        db.session.delete(card)
        db.session.commit()

        pusher.trigger(f"board-{code}-{column_id}", 'card-deleted',
                       {"id": card.id, "column_id": card.column_id, "member_id": member_id})

        return jsonify(card_schema.dump(card))
    except:
        db.session.rollback()


@cards.route('<card_id>/content', methods=["PUT"])
@token_required
def modify_card_content_by_id(member_id, code, column_id, card_id):
    card = db.session.query(Card) \
        .filter(Card.id == card_id) \
        .filter(Column.id == column_id) \
        .filter(Board.code == code) \
        .filter(Member.firebase_user_id == member_id) \
        .first()

    if not card:
        return 'Card could not find!', 501

    new_content = request.json['content']

    try:
        card.content = new_content

        db.session.commit()

        pusher.trigger(f"board-{code}-{column_id}", 'card-updated', {"id": card.id, "content": new_content})

        return jsonify(card_schema.dump(card))
    except:
        db.session.rollback()
