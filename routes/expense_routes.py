from flask import Blueprint, request, jsonify
from db.connection import get_db_connection

expense_bp = Blueprint("expenses", __name__)


# Get all expenses (by user)

@expense_bp.route("/", methods=["GET"])
def get_expenses():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ub_expenses WHERE user_id = %s", (user_id,))
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(expenses), 200



# Add expense

@expense_bp.route("/", methods=["POST"])
def add_expense():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    category = data.get("category")
    note = data.get("note")

    if not user_id or not amount or not category:
        return jsonify({"error": "user_id, amount, and category required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ub_expenses (user_id, amount, category, note) VALUES (%s, %s, %s, %s)",
        (user_id, amount, category, note)
    )
    conn.commit()
    expense_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Expense added",
        "expense": {"id": expense_id, "amount": amount, "category": category, "note": note}
    }), 201



# Update expense

@expense_bp.route("/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    fields = []
    values = []

    if "amount" in data:
        fields.append("amount = %s")
        values.append(data["amount"])
    if "category" in data:
        fields.append("category = %s")
        values.append(data["category"])
    if "note" in data:
        fields.append("note = %s")
        values.append(data["note"])

    if not fields:
        return jsonify({"error": "Nothing to update"}), 400

    query = f"UPDATE ub_expenses SET {', '.join(fields)} WHERE id = %s AND user_id = %s"
    values.extend([expense_id, user_id])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(values))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Expense updated"}), 200



# Delete expense

@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM ub_expenses WHERE id = %s AND user_id = %s",
        (expense_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Expense deleted"}), 200
