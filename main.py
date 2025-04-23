from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv
import os
import psycopg2
import requests
import json

app = Flask(__name__)
app.secret_key = 'session'

load_dotenv()

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get('DB_NAME')

@app.route('/items', methods=["POST", "GET"])
def show_items():
  if request.method == 'GET':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()
    query = "SELECT * FROM items"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('items.html', items=data, amounts=data)
  
  if request.method == 'POST':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()
    if 'search-form' in request.form:
      search = request.form["search"]
      query1 = "SELECT * FROM items WHERE items.item = %s"
      cur.execute(query1, (search,))
      item = cur.fetchall()
      if item == []:
        query2 = "SELECT * FROM items WHERE items.itemid = %s"
        cur.execute(query2, (search,))
        item = cur.fetchall()
      cur.close()
      conn.close()
      return render_template('items.html', items=item, amounts=item)
    
    if 'LH' in request.form:
      sort = "http://127.0.0.1:6000/number_sort_LH"
      query = "SELECT * FROM items"
      cur.execute(query)
      data = cur.fetchall()

      query2 = "SELECT items.item_id, items.item, items.itemid, items.sellprice FROM items"
      cur.execute(query2)
      amounts = cur.fetchall()
      response = requests.get(sort, json={'amounts': amounts})
      if response.status_code == 200:
        sorted_amounts = response.json()['sorted_numbers']
        print(sorted_amounts)
        cur.close()
        conn.close()
        return render_template('items.html', items=data, amounts=sorted_amounts)
      
      else:
        cur.close()
        conn.close()
        return redirect('/items')
    
    if 'HL' in request.form:
      sort = "http://127.0.0.1:6000/number_sort_HL"
      query = "SELECT * FROM items"
      cur.execute(query)
      data = cur.fetchall()

      query2 = "SELECT items.item_id, items.item, items.itemid, items.sellprice FROM items"
      cur.execute(query2)
      amounts = cur.fetchall()
      response = requests.get(sort, json={'amounts': amounts})
      if response.status_code == 200:
        sorted_amounts = response.json()['sorted_numbers']
        print(sorted_amounts)
        cur.close()
        conn.close()
        return render_template('items.html', items=data, amounts=sorted_amounts)
      
      else:
        cur.close()
        conn.close()
        return redirect('/items')

    item = request.form["item"]
    itemid = request.form["itemID"]
    sellprice = request.form["price"]
    cost = request.form["cost"]
    inventory = request.form["inventory"]
    contact = request.form["contact"]

    query = "INSERT INTO items (item, itemid, sellprice, cost, inventory, contact, fk_user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    cur.execute(query, (item, itemid, sellprice, cost, inventory, contact, 1))
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/items')

@app.route('/item_update/<int:id>', methods=['POST'])
def item_update(id):
  if request.method == 'POST':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()

    item = request.form["item"]
    itemid = request.form["itemID"]
    sellprice = request.form["price"]
    cost = request.form["cost"]
    inventory = request.form["inventory"]
    contact = request.form["contact"]
    #fk_user_id = request.form[]

    query = "UPDATE items SET item = %s, itemid = %s, sellprice = %s, cost = %s, inventory = %s, contact = %s, fk_user_id = %s WHERE item_id = %s"


    cur.execute(query, (item, itemid, sellprice, cost, inventory, contact, 1, id))
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/items')

@app.route('/item_delete/<int:id>', methods=['GET'])
def delete_item(id):
  conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
  cur = conn.cursor()
  query = "DELETE FROM items WHERE items.item_id = '%s'"

  cur.execute(query, (id,))
  conn.commit()

  cur.close()
  conn.close()

  return redirect('/items')

@app.route('/employees', methods=["POST", "GET"])
def show_employees():
  if request.method == 'GET':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()
    query = "SELECT * FROM Employees"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('employees.html', employees=data, names=data)
  
  if request.method == 'POST':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()

    if 'search-form' in request.form:
      search = request.form["search"]
      query1 = "SELECT * FROM Employees WHERE employees.empname = %s"
      cur.execute(query1, (search,))
      user = cur.fetchall()
      if user == []:
        query2 = "SELECT * FROM employees WHERE employees.employeeid = %s"
        cur.execute(query2, (search,))
        user = cur.fetchall()
      cur.close()
      conn.close()
      return render_template('employees.html', employees=user, names=user)
    
    if 'AZ' in request.form:
      sort = "http://127.0.0.1:6000/name_sort_AZ"
      query = "SELECT * FROM Employees"
      cur.execute(query)
      data = cur.fetchall()

      query2 = "SELECT employees.emp_id, employees.empname, employees.employeeid, employees.jobtitle FROM employees"
      cur.execute(query2)
      names = cur.fetchall()
      print(names)
      response = requests.get(sort, json={'names':names}) #calling MICROSERVICE D
      if response.status_code == 200:
        sorted_names = response.json()['sorted_names']
        print(sorted_names)
        cur.close()
        conn.close()
        return render_template('employees.html', employees=data, names=sorted_names)
      
      else:
        cur.close()
        conn.close()
        return redirect('/employees')
      
    if 'ZA' in request.form:
      sort = "http://127.0.0.1:6000/name_sort_ZA"
      query = "SELECT * FROM Employees"
      cur.execute(query)
      data = cur.fetchall()
      
      query2 = "SELECT employees.emp_id, employees.empname, employees.employeeid, employees.jobtitle FROM employees"
      cur.execute(query2)
      names = cur.fetchall()
      response = requests.get(sort, json={'names':names})
      if response.status_code == 200:
        sorted_names = response.json()['sorted_names']
        print(sorted_names)
        cur.close()
        conn.close()
        return render_template('employees.html', employees=data, names=sorted_names)
      
      else:
        cur.close()
        conn.close()
        return redirect('/employees')
    
    empname = request.form["name"]
    employeeid = request.form["empID"]
    jobtitle = request.form["jobTitle"]
    startdate = request.form["startDate"]
    birthdate = request.form["DOB"]
    phonenumber = request.form["phone"]
    manager = request.form["manager"]

    query = "INSERT INTO employees (empname, employeeid, jobtitle, startdate, birthdate, phonenumber, manager, fk_user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    cur.execute(query, (empname, employeeid, jobtitle, startdate, birthdate, phonenumber, manager, 1))
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/employees')

@app.route('/emp_update/<int:id>', methods=['POST'])
def emp_update(id):
  if request.method == 'POST':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()

    empname = request.form["name"]
    employeeid = request.form["empID"]
    jobtitle = request.form["jobTitle"]
    startdate = request.form["startDate"]
    birthdate = request.form["DOB"]
    phonenumber = request.form["phone"]
    manager = request.form["manager"]
    #fk_user_id = request.form[]

    query = "UPDATE employees SET empname = %s, employeeid = %s, jobtitle = %s, startdate = %s, birthdate = %s, phonenumber = %s, manager = %s, fk_user_id = %s WHERE emp_id = %s"


    cur.execute(query, (empname, employeeid, jobtitle, startdate, birthdate, phonenumber, manager, 1, id))
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/employees')

@app.route('/emp_delete/<int:id>', methods=['GET'])
def delete_emp(id):
  conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
  cur = conn.cursor()
  query = "DELETE FROM employees WHERE employees.emp_id = '%s'"

  cur.execute(query, (id,))
  conn.commit()

  cur.close()
  conn.close()

  return redirect('/employees')

@app.route('/sales', methods=["POST", "GET"])
def show_sales():
  add = 'http://127.0.0.1:7000/total'
  if request.method == 'GET':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    
    cur = conn.cursor()
    query = "SELECT salesitems.sale_item_id as ID, employees.emp_id as empID, items.item_id as itemID, sales.sale_id as salesID, employees.empname as Name, items.sellprice * salesitems.quantity as Amount, sales.ordernumber as Order, items.item as Item, salesitems.quantity as quantity FROM ITEMS JOIN SALESITEMS ON ITEMS.item_id = salesitems.FK_ITEM_ID JOIN SALES ON SALESITEMS.FK_SALE_ID = SALES.sale_id JOIN employees ON SALES.fk_emp_id = employees.emp_id"
    cur.execute(query)
    sales_data = cur.fetchall()

    query2 = "SELECT * FROM employees"
    cur.execute(query2)
    employees_data = cur.fetchall()

    query3 = "SELECT * FROM items"
    cur.execute(query3)
    items_data = cur.fetchall()

    query4 = "SELECT ITEMS.SELLPRICE * SALESITEMS.QUANTITY AS AMOUNT FROM ITEMS JOIN SALESITEMS ON ITEMS.ITEM_ID = SALESITEMS.FK_ITEM_ID"
    cur.execute(query4)
    amounts = cur.fetchall()

    cur.close()
    conn.close()

    response = requests.get(add, json={'numbers':amounts})
    print(response)

    return render_template('sales.html', sales=sales_data, employees=employees_data, items=items_data, total=response.json()['total'])
  
  if request.method == 'POST':
    conn = psycopg2.connect(database=db_name, user=db_user,
                        password=db_password, host=db_host, port=db_port)
    
    cur = conn.cursor()

    if 'search-form' in request.form:
      search = request.form["search"]

      query1 = "SELECT salesitems.sale_item_id as ID, employees.emp_id as empID, items.item_id as itemID, sales.sale_id as salesID, employees.empname as Name, items.sellprice * salesitems.quantity as Amount, sales.ordernumber as Order, items.item as Item, salesitems.quantity as quantity FROM ITEMS JOIN SALESITEMS ON ITEMS.item_id = salesitems.FK_ITEM_ID JOIN SALES ON SALESITEMS.FK_SALE_ID = SALES.sale_id JOIN employees ON SALES.fk_emp_id = employees.emp_id WHERE sales.ordernumber = %s"
      cur.execute(query1, (search,))

      sales = cur.fetchall()
      
      if sales == []:
        query2 = "SELECT salesitems.sale_item_id as ID, employees.emp_id as empID, items.item_id as itemID, sales.sale_id as salesID, employees.empname as Name, items.sellprice * salesitems.quantity as Amount, sales.ordernumber as Order, items.item as Item, salesitems.quantity as quantity FROM ITEMS JOIN SALESITEMS ON ITEMS.item_id = salesitems.FK_ITEM_ID JOIN SALES ON SALESITEMS.FK_SALE_ID = SALES.sale_id JOIN employees ON SALES.fk_emp_id = employees.emp_id WHERE items.item = %s"
        cur.execute(query2, (search,))

        sales = cur.fetchall()

        if sales == []:
          query3 = "SELECT salesitems.sale_item_id as ID, employees.emp_id as empID, items.item_id as itemID, sales.sale_id as salesID, employees.empname as Name, items.sellprice * salesitems.quantity as Amount, sales.ordernumber as Order, items.item as Item, salesitems.quantity as quantity FROM ITEMS JOIN SALESITEMS ON ITEMS.item_id = salesitems.FK_ITEM_ID JOIN SALES ON SALESITEMS.FK_SALE_ID = SALES.sale_id JOIN employees ON SALES.fk_emp_id = employees.emp_id WHERE employees.empname = %s"
          cur.execute(query3, (search,))

          sales = cur.fetchall()
      
      if sales != []:
        amounts = []
        for item in sales:
          amounts.append([item[5]])
        response = requests.get(add, json={'numbers': amounts})

      query4 = "SELECT * FROM employees"
      cur.execute(query4)
      employees_data = cur.fetchall()


      query5 = "SELECT * FROM items"
      cur.execute(query5)
      items_data = cur.fetchall()
      cur.close()
      conn.close()

      return render_template('sales.html', sales=sales, employees=employees_data, items=items_data, total=response.json()['total'])

    form_data = request.form
    items = (len(form_data) - 4)/2 #calculates the number of items sold submitted in the form

    ordernumber = request.form["order"]
    amount = request.form["amount"]
    saledate = request.form["sale-date"]
    emp_id = request.form["employee"]
    #fk_user_id = request.form[]

    query = "INSERT INTO sales (ordernumber, amount, saledate, fk_emp_id, fk_user_id) VALUES (%s, %s, %s, %s, %s)"

    cur.execute(query, (ordernumber, amount, saledate, emp_id, 1))
    conn.commit()

    query1 = "SELECT sale_id FROM sales WHERE sales.ordernumber = %s"
    cur.execute(query1, (ordernumber,))
    data = cur.fetchone()

    for i in range(1, int(items)+1):
      item_id = request.form["item-sold_"+str(i)]
      qty = request.form["quantity_"+str(i)]

      query2 = "INSERT INTO salesitems (fk_sale_id, fk_item_id, quantity, fk_user_id) VALUES (%s, %s, %s, %s)"

      cur.execute(query2, (data[0], item_id, qty, 1))
      conn.commit()
    
    cur.close()
    conn.close()

    return redirect('/sales')

@app.route('/help', methods=['GET'])
def show_help():
  return render_template('/help.html')

@app.route('/home', methods=['GET', 'POST'])
def show_home():
  if request.method == 'GET':
    percentages = 'http://127.0.0.1:7000/percentage'

    conn = psycopg2.connect(database=db_name, user=db_user,
                            password=db_password, host=db_host, port=db_port)
        
    cur = conn.cursor()

    query = '''SELECT employees.empname as Name,
                sum(items.sellprice * salesitems.quantity) as Amount 
                FROM ITEMS JOIN SALESITEMS ON ITEMS.item_id = salesitems.FK_ITEM_ID 
                JOIN SALES ON SALESITEMS.FK_SALE_ID = SALES.sale_id 
                JOIN employees ON SALES.fk_emp_id = employees.emp_id
                GROUP BY Name'''
    
    query2 = '''SELECT items.item as Name,
                sum(items.sellprice * salesitems.quantity) as Amount 
                FROM ITEMS JOIN SALESITEMS ON ITEMS.item_id = salesitems.FK_ITEM_ID 
                JOIN SALES ON SALESITEMS.FK_SALE_ID = SALES.sale_id
                GROUP BY Name'''
    
    cur.execute(query)
    emp_data = cur.fetchall()
    print(emp_data)

    cur.execute(query2)
    item_data = cur.fetchall()
    print(item_data)
    

    emp_response = requests.get(percentages, json={'numbers':emp_data})
    names = [name[0] for name in emp_data]
    emp_percentages = emp_response.json()['percentages']
    print(emp_percentages)

    item_response = requests.get(percentages, json={'numbers':item_data}) ## calling MICROSERVICE C
    items = [item[0] for item in item_data]
    item_percentages = item_response.json()['percentages']
    print(item_percentages)

    return render_template('/home.html', name=names, emp_percentages=emp_percentages, item=items, item_percentages=item_percentages)
  
  if request.method == 'POST':

    if 'signUp' in request.form:
      signUp = "http://127.0.0.1:5000/create"
      validatePassword = 'http://127.0.0.1:8000/validate'

      firstName = request.form['firstname']
      lastName = request.form['lastname']
      business = request.form['businessname']
      username = request.form['username']
      password = request.form['password']
      password_verify = request.form['re-password']

      data = {'username': username,
              'password': password}
      
      validateResponse = requests.get(validatePassword, json={'password': password,
                                                               'password_verify': password_verify}) #calling MICROSERVICE B
      
      if validateResponse.status_code == 200:
      
        response = requests.post(signUp, json=data) #calling MICROSERVICE A
        if response.status_code == 200:
          userid = response.json()['user_id']
          print(userid)

          conn = psycopg2.connect(database=db_name, user=db_user,
                            password=db_password, host=db_host, port=db_port)
        
          cur = conn.cursor()

          query = '''INSERT INTO users (firstname, lastname, business, userid) VALUES (%s, %s, %s, %s)'''

          cur.execute(query, (firstName, lastName, business, userid))
          conn.commit()

          cur.close()
          conn.close()

          return redirect('/home')
        else:
          flash('Username is already in use')
          return redirect('/signup') 
      
      else:
        flash(validateResponse.json()['error'])
        return redirect('/signup')

    if 'Login' in request.form:
      Login = "http://127.0.0.1:5000/login"

      username = request.form['username']
      password = request.form['password']

      data = {'username': username,
              'password': password}
      print(data)
      response = requests.post(Login, json=data)
      print(response) #calling MICROSERVICE A
      if response.status_code == 200:
        return redirect('/home') 
      else:
        flash('Invalid username or password')
        return redirect('/')

@app.route('/', methods=['GET'])
def show_welcome():
  return render_template('/welcome.html')

@app.route('/signup', methods=['GET'])
def show_signup():
  if request.method == 'GET':
    return render_template('/signup.html')

@app.route('/change', methods=['GET', 'POST'])
def show_change():
  if request.method == 'GET':
    return render_template('/change.html')
  
  if request.method == 'POST':
    validatePassword = 'http://127.0.0.1:8000/validate'
    changePassword = 'http://127.0.0.1:5000/change'

    username = request.form['username']
    curPassword = request.form['password']
    newPassword = request.form['newPassword']

    data = {'username': username,
            'password': curPassword,
            'new_password': newPassword}
    print(data)
    validateResponse = requests.get(validatePassword, json={'password': newPassword,
                                                             'password_verify': newPassword}) #calling MICROSERVICE B
    print(validateResponse)
    if validateResponse.status_code == 200:
    
      response = requests.post(changePassword, json=data)
      print(response)

      if response.status_code == 200:
        flash("Password updated successfully")
        return redirect('/change')
      else:
        flash("Password not updated - invalid credentials")
        return redirect('/change')
    
    else:
      flash(validateResponse.json()['error'])
      return redirect('/change')


if __name__ == "__main__":
  app.run(port=7862, debug=True)