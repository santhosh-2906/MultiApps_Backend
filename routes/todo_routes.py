from flask import Blueprint, request, jsonify
from db.connection import get_db_connection

todo_bp = Blueprint("todos", __name__)


# Get all todos (by user)

@todo_bp.route("/", methods=["GET"])
def get_todos():
    user_id = request.args.get("user_id")   # frontend sends as query param ?user_id=1
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ub_todos WHERE user_id = %s", (user_id,))
    todos = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(todos), 200

# Add todo

@todo_bp.route("/", methods=["POST"])
def add_todo():
    data = request.json
    user_id = data.get("user_id")
    task = data.get("task")

    if not user_id or not task:
        return jsonify({"error": "user_id and task required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ub_todos (user_id, task) VALUES (%s, %s)",
        (user_id, task)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Todo added"}), 201



# Update todo (task or status)

@todo_bp.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    user_id = data.get("user_id")
    task = data.get("task")
    status = data.get("status")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    if not (task or status):
        return jsonify({"error": "Nothing to update"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    if task and status:
        cursor.execute(
            "UPDATE ub_todos SET task = %s, status = %s WHERE id = %s AND user_id = %s",
            (task, status, todo_id, user_id)
        )
    elif task:
        cursor.execute(
            "UPDATE ub_todos SET task = %s WHERE id = %s AND user_id = %s",
            (task, todo_id, user_id)
        )
    elif status:
        cursor.execute(
            "UPDATE ub_todos SET status = %s WHERE id = %s AND user_id = %s",
            (status, todo_id, user_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Todo updated"}), 200


# Delete todo

@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM ub_todos WHERE id = %s AND user_id = %s",
        (todo_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Todo deleted"}), 200
