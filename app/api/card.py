from flask import Blueprint, request, jsonify
from app import db
from app.models.board import Board
from app.models.card import Card
from app.models.column import Column
from app.models.member import Member
from app.schema.card import card_schema

cards = Blueprint('cards', __name__, url_prefix='/api/v1/members/<member_id>/boards/<code>/columns/<column_id>/cards')

@cards.route('', methods=["POST"])
def create_card(member_id, code, column_id):
    content = request.json['content']
    board = db.session.query(Board) \
        .filter(Board.code == code) \
        .filter(Board.member_id == member_id) \
        .first()
    board_id = board.id

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
