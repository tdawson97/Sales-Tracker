import os
from flask import Flask, jsonify, request

app = Flask(__name__)
port = int(os.environ.get('PORT', 6000))


@app.route('/name_sort_AZ')
def sort_names_AZ():
  names = request.json.get('names')

  names.sort(key=lambda x: x[1])
  print(names)
  return jsonify({'sorted_names': names}), 200


@app.route('/name_sort_ZA')
def sort_names_ZA():
  names = request.json.get('names')

  names.sort(key=lambda x: x[1])
  reversed_names = [names[i] for i in range(len(names) -1, -1, -1)]
  print(names)
  return jsonify({'sorted_names': reversed_names}), 200


@app.route("/number_sort_LH")
def sort_numbers_LH():
  numbers = request.json.get('amounts')
  numbers.sort(key=lambda x: x[3])
  print(numbers)
  return jsonify({'sorted_numbers': numbers}), 200


@app.route("/number_sort_HL")
def sort_numbers_HL():
  numbers = request.json.get('amounts')
  numbers.sort(key=lambda x: x[3])
  reversed_numbers = [numbers[i] for i in range(len(numbers) -1, -1, -1)]
  print(numbers)
  return jsonify({'sorted_numbers': reversed_numbers})

if __name__ == "__main__":
  app.run(port=6000, debug=True)