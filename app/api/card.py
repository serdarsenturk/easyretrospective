from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app import db, app
from app.models.board import Board
from app.models.card import Card
from app.models.column import Column
from app.models.member import Member
from app.schema.card import card_schema
from pusher import Pusher

cards = Blueprint('cards', __name__, url_prefix='/api/v1/members/<member_id>/boards/<code>/columns/<column_id>/cards')
CORS(cards, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}})

@cards.route('', methods=["POST"])
def create_card(member_id, code, column_id):
    content = request.json['content']

    new_card = Card(content = content, member_id = member_id, column_id = column_id)

    db.session.add(new_card)
    db.session.commit()

    return jsonify(card_schema.dump(new_card))

@cards.route('<card_id>', methods=["DELETE"])
def delete_card_by_id(member_id, code, column_id, card_id):
    card = db.session.query(Card) \
        .filter(Card.id == card_id) \
        .filter(Column.id == column_id) \
        .filter(Board.code == code) \
        .filter(Member.id == member_id) \
        .first()

    db.session.delete(card)
    db.session.commit()

    return jsonify(card_schema.dump(card))

@cards.route('<card_id>/content', methods=["PUT"])
def modify_card_content_by_id(member_id, code, column_id, card_id):
    card = db.session.query(Card) \
        .filter(Card.id == card_id) \
        .filter(Column.id == column_id) \
        .filter(Board.code == code) \
        .filter(Member.id == member_id) \
        .first()

    new_content = request.json['content']
    card.content = new_content

    db.session.commit()

    return jsonify(card_schema.dump(card))