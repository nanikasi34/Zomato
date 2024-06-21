from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('zomato.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get restaurant by ID
@app.route('/api/restaurants/<int:Restaurant_ID>', methods=['GET'])
def get_restaurant(Restaurant_ID):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM restaurants WHERE Restaurant_ID = ?', (Restaurant_ID,)).fetchone()
    conn.close()
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404
    return jsonify(dict(restaurant))

# Get list of restaurants with pagination, filtering, and search functionality
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    conn = get_db_connection()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    country = request.args.get('country', type=int)
    avg_spend = request.args.get('avg_spend', type=int)
    cuisines = request.args.get('cuisines', type=str)
    search_query = request.args.get('search_query', type=str)

    query = 'SELECT * FROM restaurants WHERE 1=1'
    params = []

    if search_query:
        if search_query.isdigit():  # Check if search query is a number (Restaurant ID)
            query += ' AND Restaurant_ID = ?'
        else:  # Assume search query is a restaurant name
            query += ' AND Restaurant_Name LIKE ?'
            search_query = f'%{search_query}%'
        params.append(search_query)
    else:
        if country:
            query += ' AND Country_Code = ?'
            params.append(country)
        if avg_spend is not None:
            query += ' AND Average_Cost_for_two = ?'
            params.append(avg_spend)
        if cuisines:
            query += ' AND Cuisines LIKE ?'
            params.append(f'%{cuisines}%')

    query += ' LIMIT ? OFFSET ?'
    params.extend([per_page, offset])

    restaurants = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in restaurants])

# Restaurant list page with search, filtering, and pagination functionality
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        return redirect(url_for('index', search_query=search_query))
    
    if request.method == 'GET' and not request.args:
        return redirect(url_for('index', page=1, per_page=10, search_query='', cuisines=''))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10

    country = request.args.get('country', type=int)
    avg_spend = request.args.get('avg_spend', type=int)
    cuisines = request.args.get('cuisines', '')
    search_query = request.args.get('search_query', '')

    conn = get_db_connection()
    offset = (page - 1) * per_page

    query = 'SELECT * FROM restaurants WHERE 1=1'
    params = []

    if search_query:
        if search_query.isdigit():  # Check if search query is a number (Restaurant ID)
            query += ' AND Restaurant_ID = ?'
        else:  # Assume search query is a restaurant name
            query += ' AND Restaurant_Name LIKE ?'
            search_query = f'%{search_query}%'
        params.append(search_query)
    else:
        if country:
            query += ' AND Country_Code = ?'
            params.append(country)
        if avg_spend is not None:
            query += ' AND Average_Cost_for_two = ?'
            params.append(avg_spend)
        if cuisines:
            query += ' AND Cuisines LIKE ?'
            params.append(f'%{cuisines}%')

    query += ' LIMIT ? OFFSET ?'
    params.extend([per_page, offset])

    restaurants = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('index.html', restaurants=restaurants, page=page, per_page=per_page, country=country, avg_spend=avg_spend, cuisines=cuisines, search_query=search_query)


# Restaurant detail page
@app.route('/restaurants/<int:Restaurant_ID>')
def restaurant_detail(Restaurant_ID):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM restaurants WHERE Restaurant_ID = ?', (Restaurant_ID,)).fetchone()
    conn.close()
    if restaurant is None:
        return render_template('404.html'), 404
    return render_template('detail.html', restaurant=restaurant)

if __name__ == '__main__':
    app.run(debug=True)
