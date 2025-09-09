from flask import Blueprint, request, jsonify
from db.connection import get_db_connection

notes_bp = Blueprint("notes", __name__)


# Get all notes (by user)

@notes_bp.route("/", methods=["GET"])
def get_notes():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ub_notes WHERE user_id = %s", (user_id,))
    notes = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(notes), 200



# Add note

@notes_bp.route("/", methods=["POST"])
def add_note():
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")

    if not user_id or not title or not content:
        return jsonify({"error": "user_id, title, and content required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ub_notes (user_id, title, content) VALUES (%s, %s, %s)",
        (user_id, title, content)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Note added"}), 201



# Update note

@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    if not (title or content):
        return jsonify({"error": "Nothing to update"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    if title and content:
        cursor.execute(
            "UPDATE ub_notes SET title = %s, content = %s WHERE id = %s AND user_id = %s",
            (title, content, note_id, user_id)
        )
    elif title:
        cursor.execute(
            "UPDATE ub_notes SET title = %s WHERE id = %s AND user_id = %s",
            (title, note_id, user_id)
        )
    elif content:
        cursor.execute(
            "UPDATE ub_notes SET content = %s WHERE id = %s AND user_id = %s",
            (content, note_id, user_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Note updated"}), 200



# Delete note

@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM ub_notes WHERE id = %s AND user_id = %s",
        (note_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Note deleted"}), 200
