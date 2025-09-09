from flask import Blueprint, request, jsonify
from db.connection import get_db_connection

auth_bp = Blueprint("auth", __name__)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if username exists
    cursor.execute("SELECT * FROM ub_users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Username already taken"}), 400

    # Insert user
    cursor.execute(
        "INSERT INTO ub_users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()

    user_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({
        "message": "User registered successfully",
        "user": {"id": user_id, "username": username}
    }), 201


# Login
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Username and password required"}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute(
#         "SELECT * FROM ub_users WHERE username = %s AND password = %s",
#         (username, password)
#     )   
#     user = cursor.fetchone()
#     cursor.close()
#     conn.close()

#     if user:
#         return jsonify({
#             "message": "Login successful",
#             "user": {"id": user["id"], "username": user["username"]}
#         }), 200
#     else:
#         return jsonify({"error": "Invalid credentials"}), 401
import traceback

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM ub_users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                "message": "Login successful",
                "user": {"id": user.get("id"), "username": user.get("username")}
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print("🔥 ERROR in /auth/login:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
