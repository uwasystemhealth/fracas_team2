#  Better FRACAS
#  Copyright (C) 2023  Peter Tanner
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app import app, db
from app.models.authentication import User
from app.models.team import Team
from app.utils import handle_exceptions, superuser_jwt_required, user_jwt_required
from app.models.record import Record
from app.routes.authentication import send_signup_request_email


def get_teamname(user):
    if user.team_id is None:
        return "N/A"
    team = Team.query.get(user.team_id)
    return team.name

def get_if_leading(user):
    if user.leading:
        return True
    else:
        return False


def user_json(users):
    # User JSON Schema
    user_json = [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "superuser": user.superuser,
            "team_id": user.team_id,
            "team_name": get_teamname(user),
            "can_validate": user.can_validate,
            "is_leading": get_if_leading(user)
        }
        for user in users
    ]
    return jsonify(user_json)


# Get list of Users
@app.route("/api/v1/user", methods=["GET"])
@handle_exceptions
@user_jwt_required
# Get list of Users
def list_users():
    users = User.query.filter_by(registered=True).all()
    return user_json(users), 200


# Checks user validation permission
@app.route("/api/v1/user/can_validate", methods=["GET"])
@handle_exceptions
@user_jwt_required
def can_validate():
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).first()
    if user.can_validate or user.leading or user.superuser:
        return jsonify(True), 200
    else:
        return jsonify(False), 200


# Get Current User ID
@app.route("/api/v1/user/<int:user_id>", methods=["GET"])
@handle_exceptions
@user_jwt_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"err": "no_user", "msg": "User not found"}), 404
    return user_json(user), 200


# Get User via id
@app.route("/api/v1/user/current", methods=["GET"])
@handle_exceptions
@user_jwt_required
def get_current_user():
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).first()
    if user is None:
        return jsonify({"err": "no_user", "msg": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# Add user
@app.route("/api/v1/user", methods=["POST"])
@handle_exceptions
@superuser_jwt_required
def add_user():
    data = request.get_json()
    print(data)
    print(data["team"])

    registered = False

    user = User(registered=registered)

    if "name" in data:
        user.name = data["name"]
    else:
        return jsonify({"error": "Name required"}), 400
    if "email" in data:
        user.email = data["email"]
    else:
        return jsonify({"error": "Email required"}), 400
    # [!] YOU SHOULD NOT SET A PASSWORD AT THIS STAGE.
    # API ONLY FOR TESTING PURPOSES!
    # THIS WILL SET THE PASSWORD _AND_ REGISTER THE USER
    # if "password" in data:
    #     registered = True
    #     user.set_password_and_register(data["password"])
    if "team" in data:
        team_id = data["team"]
        if Team.query.filter_by(id=team_id).first():
            user.team_id = team_id
        else:
            return jsonify({"error": "Team doesn't exist"}), 400
    else:
        return jsonify({"error": "Team required"}), 400

    db.session.add(user)
    db.session.commit()

    if not registered:
        send_signup_request_email(user.email)
        return (
            jsonify(
                {"message": "User added successfully. Validation email has been sent."}
            ),
            201,
        )

    return (
        jsonify({"message": "User added successfully and registered."}),
        201,
    )


# Delete Team (Mark Inactive)
@app.route("/api/v1/user/<int:user_id>", methods=["DELETE"])
@handle_exceptions
@superuser_jwt_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    User.remove(user)
    db.session.commit()
    return jsonify({"message": "User is deregistered"}), 200


# Updates user record (with json header referencing data type)
@app.route("/api/v1/user/<int:user_id>", methods=["PUT"])
@handle_exceptions
@superuser_jwt_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    print(data)
    if "name" in data is not None or "":
        user.name = data["name"]
    if "email" in data is not None or "":
        user.email = data["email"]
    if "superuser" in data:
        user.superuser = data["superuser"]
    if "can_validate" in data:
        user.can_validate = data["can_validate"]
    if "team_id" in data:
        team = Team.query.get(data["team_id"])
        user.team = team

    db.session.commit()
    return jsonify({"message": "User Records Updated"}), 200

@app.route("/api/v1/user", methods=["PATCH"])
@handle_exceptions
@user_jwt_required
def update_local_user():
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    print(data)
    if "name" in data is not None or "":
        user.name = data["name"]
    if "email" in data is not None or "":
        user.email = data["email"]
    if ("password" in data) is not None or "":
        user.set_password_and_register(data["password"])

    db.session.commit()
    return jsonify({"message": "User Records Updated"}), 200
