from app import app, db
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.team import Team
from app.schema.team import team_schema
from firebase_admin import auth
from app.decorators.authentication_decorators import token_required

teams = Blueprint('teams', __name__)
CORS(teams, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS')}}, supports_credentials=True)


@teams.route("/api/v1/teams/create", methods=["POST"])
def create_team():
    id_token = request.headers['Authorization']
    try:
        decoded_claims = auth.verify_id_token(id_token)
        requester_id = decoded_claims['user_id']

        name = request.json['team_name']

        new_team = Team(name=name)

        db.session.add(new_team)
        db.session.commit()

        db.session.execute('INSERT INTO teams_members VALUES (:member_id, :team_id)',
                           {'member_id': requester_id, 'team_id': new_team.id})
        db.session.commit()

        return jsonify(team_schema.dump(new_team)), 200
    except:
        db.session.rollback()
        return 'Failed to team create process, please try again', 500


@teams.route("/api/v1/teams/<team_id>/name", methods=["PUT"])
@token_required
def modify_team_by_id(team_id):
    if not team_id:
        return 'Wrong request', 404

    try:
        team = db.session.query(Team) \
            .filter(Team.id == team_id) \
            .first()

        team.name = request.json["team_name"]

        db.session.commit()

        return jsonify(team_schema.dump(team)), 201
    except:
        db.session.rollback()
        return 'Team name updated failed', 500
