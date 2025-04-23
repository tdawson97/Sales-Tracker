import os
from flask import Flask, jsonify, request

app = Flask(__name__)
port = int(os.environ.get('PORT', 8000))

specChars = set("!@#$%^&*~")

def case_check(word):
  capital = False
  lowercase = False
  for char in word:
    if not capital and char.isupper():
      capital = True
    if not lowercase and char.islower():
      lowercase = True
    if capital and lowercase:
      return True
  return False

def character_check(word):
  letters = any(char.isalpha() for char in word)
  numbers = any(char.isdigit() for char in word)
  specs = not set(word).isdisjoint(specChars)

  if letters and numbers and specs:
    return True
  else:
    return False


@app.route('/validate')
def validate():
  password = request.json.get('password')
  password_verify = request.json.get('password_verify')

  if case_check(password) and character_check(password):
    if password != password_verify:
      print('Passwords do not match')
      return jsonify({'error': 'Passwords do not match'}), 401
    else:
      print('Password meets requirements')
      return jsonify({'message': 'Password meets requirements'}), 200

  else:
    print('Passwords need at least 1 capital, lowercase, number, and special character')
    return jsonify({'error': 'Passwords need at least 1 capital, lowercase, number, and special character'}), 401


if __name__ == "__main__":
  app.run(port=8000, debug=True)