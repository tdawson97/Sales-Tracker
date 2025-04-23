import os
from flask import Flask, jsonify, request

app = Flask(__name__)
port = int(os.environ.get('PORT', 7000))


@app.route('/total')
def total():
  numbers = request.json.get('numbers')  # takes a list of numbers, returns sum
  total = 0
  for x in numbers:
    total += x[0]
  print(total)
  return jsonify({'total': total}), 200


@app.route('/percentage')  # takes a list of numbers, returns list of percentages
def percentage():
  numbers = request.json.get('numbers')
  percentages = []
  
  total = sum(x[1] for x in numbers)
  for x in numbers:
    percentage = (x[1]/total)*100
    percentages.append(int(round(percentage, 0)))
  print(percentages)
  return jsonify({'percentages': percentages}), 200


if __name__ == "__main__":
  app.run(port=7000, debug=True)