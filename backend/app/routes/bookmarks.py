# Better FRACAS
# Copyright (C) 2023  Insan Basrewan, Peter Tanner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import jsonify
from app import app, db
from app.models.authentication import User
from app.models.record import Record
from app.utils import user_jwt_required
from app.utils import handle_exceptions
from flask_jwt_extended import get_jwt_identity


# Add/Remove Bookmark
@app.route("/api/v1/bookmark/<int:record_id>", methods=["POST"])
@handle_exceptions
@user_jwt_required
def toggle_bookmark(record_id):
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    record = Record.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    postToggle = False
    if record in user.bookmarked:
        user.bookmarked.remove(record)
        postToggle = False
    else:
        user.bookmarked.append(record)
        postToggle = True
    db.session.commit()
    return jsonify(postToggle), 200


# Get Bookmarks
@app.route("/api/v1/bookmark", methods=["GET"])
@handle_exceptions
@user_jwt_required
def get_bookmarks():
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    bookmarks = user.bookmarked.all()
    return jsonify(bookmarks), 201


# Check if record is Bookmarked
@app.route("/api/v1/bookmark/<int:record_id>", methods=["GET"])
@handle_exceptions
@user_jwt_required
def check_bookmark(record_id):
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    record = Record.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    if record in user.bookmarked:
        return jsonify(True), 200
    else:
        return jsonify(False), 200
