from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data
expenses = [
    {"id": 1, "category": "Food", "amount": 50},
    {"id": 2, "category": "Entertainment", "amount": 100}
]

@app.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

@app.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = {
        "id": len(expenses) + 1,
        "category": data['category'],
        "amount": data['amount']
    }
    expenses.append(new_expense)
    return jsonify(new_expense), 201

if __name__ == '__main__':
    app.run(debug=True)
