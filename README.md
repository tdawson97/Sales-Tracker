# Sales Tracker

Sales Tracker is a web application for tracking business sales, employees, and inventory. It offers a clean, modern interface and supports team management, sales reporting, and asset tracking.

## Features

- **User Authentication**: Users can sign up, log in, and change their password.
- **Employee Management**: Add, edit, delete, and search employees; sort employee list A-Z or Z-A using a microservice.
- **Inventory Management**: Add, edit, delete, and search inventory items.
- **Sales Reporting**: Record sales transactions, filter and search by order, item, or employee, and view totals.
- **Interactive Charts**: Visualize sales data by item and employee using dynamic charts powered by Chart.js.
- **Help/FAQ Section**: Built-in help page with answers to common usage questions.

## Technology Stack

- **Backend**: Flask (Python), PostgreSQL (main app), SQLite (user microservice)
- **Frontend**: HTML, CSS, JavaScript
- **Microservices**:
  - User management (SQLite, Flask, port 5000)
  - Name sorting (Flask, port 6000)
  - Statistics calculator (port 7000)
  - Validation service (port 8000)

## Project Structure

- `main.py` – Main Flask web application
- `templates/` – HTML templates (Home, Employees, Items, Sales, Help, Signup, Welcome)
- `static/style.css` – Main stylesheet
- `User/main.py` – User authentication microservice
- Other microservices (name sorting, statistics, validation) expected in their respective directories

## Setup & Installation

**Prerequisites:**
- Python 3.x, pip
- PostgreSQL for main app
- SQLite for user microservice

**Steps:**
1. Clone the repository:
   ```bash
   git clone https://github.com/tdawson97/Sales-Tracker.git
   cd Sales-Tracker
   ```

2. Install Python dependencies (add any missing requirements to your requirements.txt as needed):
   ```bash
   pip install flask psycopg2 requests
   ```

3. Set up your PostgreSQL database and update connection details in `main.py`.

4. Start all microservices:
   - User service: `python User/main.py` (port 5000)
   - Name sorting: (expected at port 6000)
   - Statistics: (expected at port 7000)
   - Validation: (expected at port 8000)

5. Start the main app:
   ```bash
   python main.py
   ```
   The main application runs on port 7862.

6. Access the app at `http://localhost:7862` (or the port you configure).

## Usage

- Log in or sign up from the Welcome page.
- Use navigation bar to access Employees, Items, Sales, Help.
- Add or manage employees and items via their respective tabs.
- Record sales, view sales reports, and see dynamic charts.
- For help, visit the Help tab.
