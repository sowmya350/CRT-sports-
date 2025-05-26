from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
jwt = JWTManager(app)

# Config (Change your local MySQL credentials)
app.config['JWT_SECRET_KEY'] = 'my_sports_secret_key'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Hapsa@#78422'
app.config['MYSQL_DB'] = 'sports_allocations'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

# Serve frontend HTML file
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'registration.html')

# ------------------ User Registration with Role and Slot Check ------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    emailid = data.get('emailid')
    phone = data.get('phone')
    password = data.get('password')
    dob = data.get('dob')
    interested_sport = data.get('interested_sport')
    role = data.get('role')
    experience = data.get('experience')
    registration_date = datetime.now()

    # Validate required fields
    if not all([username, emailid, password, interested_sport, role]):
        return jsonify({'error': 'Missing required fields'}), 400

    cur = mysql.connection.cursor()

    try:
        # Check if user already exists
        cur.execute("SELECT userid FROM user WHERE emailid = %s", (emailid,))
        if cur.fetchone():
            return jsonify({'error': 'Email already registered'}), 409

        # Verify sport exists
        cur.execute("SELECT sportid FROM sports WHERE sportname = %s", (interested_sport,))
        sport = cur.fetchone()
        if not sport:
            return jsonify({'error': 'Invalid sport selected'}), 400
        sport_id = sport[0]

        # Check role availability
        cur.execute("""
            SELECT sr.max_slots, 
                   (SELECT COUNT(*) FROM user 
                    WHERE interested_sport = %s AND role = %s) AS current_count
            FROM sport_roles sr
            WHERE sr.sport_id = %s AND sr.role_name = %s
        """, (interested_sport, role, sport_id, role))
        role_data = cur.fetchone()

        if not role_data:
            return jsonify({'error': 'Invalid role for this sport'}), 400
        
        max_slots, current_count = role_data
        if current_count >= max_slots:
            return jsonify({'error': f'No slots left for {role} in {interested_sport}'}), 400

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert new user (userid will auto-increment)
        cur.execute("""
            INSERT INTO user (
                username, emailid, phone, password, 
                dob, interested_sport, role, experience, registration_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, emailid, phone, hashed_password, 
              dob, interested_sport, role, experience, registration_date))
        
        mysql.connection.commit()
        
        # Get the auto-generated userid
        new_userid = cur.lastrowid
        
        return jsonify({
            'message': 'Registration successful!',
            'userid': new_userid,
            'username': username,
            'role': role
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
        
    finally:
        cur.close()

# ------------------ User Login ------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    emailid = data.get('emailid')
    password = data.get('password')

    if not all([emailid, password]):
        return jsonify({'error': 'Email and password required'}), 400

    cur = mysql.connection.cursor()
    
    try:
        # Get user from database including role
        cur.execute("""
            SELECT userid, username, password, role 
            FROM user 
            WHERE emailid = %s
        """, (emailid,))
        user = cur.fetchone()

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        userid, username, password_hash, role = user
        
        # Verify password
        if not bcrypt.check_password_hash(password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Create JWT token
        access_token = create_access_token(
            identity=str(userid),
            additional_claims={'role': role},
            expires_delta=timedelta(hours=24))
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'userid': userid,
            'username': username,
            'role': role
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
# ------------------ User Profile ------------------
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT userid, username, emailid, phone, dob, interested_sport, role, experience, registration_date 
        FROM user WHERE userid = %s
    """, (current_user,))
    row = cur.fetchone()
    if row:
        keys = ['userid', 'username', 'emailid', 'phone', 'dob', 'interested_sport', 'role', 'experience', 'registration_date']
        return jsonify(dict(zip(keys, row)))
    else:
        return jsonify({'error': 'User not found'}), 404

# ------------------ View All Sports ------------------
@app.route('/sports', methods=['GET'])
def viewallsports():
    cur = mysql.connection.cursor()
    cur.execute("SELECT sportid, sportname, description FROM sports")
    rows = cur.fetchall()
    sports = [{'sportid': r[0], 'sportname': r[1], 'description': r[2]} for r in rows]
    return jsonify(sports), 200

# ------------------ Get Roles for a Sport ------------------
@app.route('/available_roles/<sportname>', methods=['GET'])
def available_roles(sportname):
    cur = mysql.connection.cursor()
    
    try:
        # Get sport ID
        cur.execute("SELECT sportid FROM sports WHERE sportname = %s", (sportname,))
        sport = cur.fetchone()
        if not sport:
            return jsonify({'error': 'Sport not found'}), 404
        sport_id = sport[0]

        # Get all standard player roles AND coach roles
        cur.execute("""
            SELECT sr.role_name, sr.max_slots,
                   (SELECT COUNT(*) FROM user 
                    WHERE interested_sport = %s AND role = sr.role_name) AS current_count
            FROM sport_roles sr
            WHERE sr.sport_id = %s
            
            UNION ALL
            
            SELECT 'Coach' as role_name, 
                   3 as max_slots,  -- Adjust this number for desired coach slots
                   (SELECT COUNT(*) FROM user 
                    WHERE interested_sport = %s AND role = 'Coach') AS current_count
        """, (sportname, sport_id, sportname))
        
        roles_data = cur.fetchall()

        available_roles = []
        for role_name, max_slots, current_count in roles_data:
            slots_left = max_slots - current_count
            available_roles.append({
                'role_name': role_name,
                'max_slots': max_slots,
                'slots_left': slots_left,
                'status': 'Available' if slots_left > 0 else 'Blocked'
            })

        return jsonify({
            'sport': sportname,
            'roles': available_roles
        }), 200

    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
        
    finally:
        cur.close()


if __name__ == '__main__':
    app.run(debug=True)