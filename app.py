from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return render_template('some.html')

# Route for index.html
@app.route('/index')
def index():
    return render_template('index.html')

# Add Food Route
@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        if request.is_json:
            # Get the JSON data from the request
            data = request.get_json()
            food_name = data.get('food_name')
            quantity = data.get('quantity')
            expiry_date = data.get('expiry_date')
            location = data.get('location')
        else:
            # Handle form submission (non-JSON case, in case you have form posts)
            food_name = request.form['food_name']
            quantity = request.form['quantity']
            expiry_date = request.form['expiry_date']
            location = request.form['location']

        # Insert into the database
        conn = sqlite3.connect('food.db')
        c = conn.cursor()
        c.execute("INSERT INTO food_items (food_name, quantity, expiry_date, location) VALUES (?, ?, ?, ?)",
                  (food_name, quantity, expiry_date, location))
        conn.commit()
        conn.close()

        # Return JSON response for API calls
        if request.is_json:
            return jsonify({"message": "Food item added successfully!"}), 200
        else:
            # Redirect for form submissions
            return redirect(url_for('available_food'))

    # Render the form in case of GET request
    return render_template('index.html')


# Available Food Route

@app.route('/available_food')
def available_food():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()
    c.execute("SELECT * FROM food_items")
    food_items = c.fetchall()
    conn.close()

    # Print the raw data for debugging
    print(food_items)

    food_items_list = [
        {
            'food_name': item[0],
            'quantity': item[1],
            'expiry_date': item[2],
            'location': item[3]
        }
        for item in food_items
    ]
    
    # Print the formatted food items to ensure correctness
    print(food_items_list)

    return jsonify({'food_items': food_items_list})


# Create the database and table
def init_db():
    conn = sqlite3.connect('food.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            quantity TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Initialize database on startup
    app.run(debug=True)
