# ============================================
# DISTANCE HOTEL — FLASK BACKEND
# Version: 3.0.0
# ============================================

import os
from dotenv import load_dotenv

load_dotenv()  # This loads the .env file locally


from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from datetime import datetime
import sqlite3
import requests
import os
import re

# ============================================
# FLASK APP
# ============================================

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'distance-hotel-secret')
# ============================================
# PAYSTACK CONFIG
# ============================================

PAYSTACK_SECRET = os.environ.get(
    'PAYSTACK_SECRET_KEY',
    'sk_test_453e6852331b7018e76017922453975adfa26b65'
)

PAYSTACK_PUBLIC = os.environ.get(
    'PAYSTACK_PUBLIC_KEY',
    'pk_test_a49bd26daf79787b5fde3f01f093a548c00e7665'
)

# ============================================
# DATABASE CONFIG
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'distance_hotel.db')

# ============================================
# DATABASE CONNECTION
# ============================================

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            guest_name TEXT NOT NULL,
            email TEXT,
            phone TEXT NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            guests INTEGER DEFAULT 1,
            requests TEXT,
            total_amount INTEGER DEFAULT 0,
            payment_status TEXT DEFAULT 'pending',
            paystack_ref TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Subscribers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Contact messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ============================================
# INITIALIZE DATABASE
# ============================================

init_db()

# ============================================
# HOTEL DATA
# ============================================

HOTEL_DATA = {
    "hotel": {
        "name": "Distance Hotel",
        "branch": "Oro HQ",
        "whatsapp": "2348000000000",
        "description": "Where distance meets luxury."
    },
    "rooms": [
        {
            "id": 1,
            "name": "Standard Fan Room",
            "price": 8500,
            "category": "standard",
            "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304",
            "guests": 2,
            "bed": "Queen Bed",
            "size": "28m²",
            "description": "Comfortable and affordable accommodation perfect for budget-conscious travelers. Features a fan, free WiFi, and a cozy atmosphere.",
            "tags": ["Fan", "WiFi", "Budget"]
        },
        {
            "id": 2,
            "name": "Deluxe Room",
            "price": 12000,
            "category": "deluxe",
            "image": "https://images.unsplash.com/photo-1590490360182-c33d57733427",
            "guests": 2,
            "bed": "Queen Bed",
            "size": "32m²",
            "description": "Upgraded comfort with air conditioning, premium bedding, and a work desk. Perfect for business and leisure travelers.",
            "tags": ["AC", "Work Desk", "Premium"]
        },
        {
            "id": 3,
            "name": "Executive AC Room",
            "price": 15000,
            "category": "executive",
            "image": "https://images.unsplash.com/photo-1566665797739-1674de7a421a",
            "guests": 2,
            "bed": "King Bed",
            "size": "35m²",
            "description": "Spacious room with air conditioning, smart TV, and premium furnishings. Ideal for business travelers seeking comfort and productivity.",
            "tags": ["AC", "Smart TV", "Luxury"]
        },
        {
            "id": 4,
            "name": "Royal Suite",
            "price": 25000,
            "category": "suite",
            "image": "https://images.unsplash.com/photo-1618773928121-c32242e63f39",
            "guests": 4,
            "bed": "King Bed",
            "size": "65m²",
            "description": "Ultimate luxury with separate living area, premium amenities, and stunning views. The perfect choice for special occasions.",
            "tags": ["VIP", "King Bed", "Security"]
        },
        {
            "id": 5,
            "name": "Presidential Suite",
            "price": 45000,
            "category": "suite",
            "image": "https://images.unsplash.com/photo-1590490360182-c33d57733427",
            "guests": 6,
            "bed": "King Bed",
            "size": "280m²",
            "description": "The pinnacle of luxury. Private terrace, jacuzzi, dedicated butler service, and panoramic views of Oro.",
            "tags": ["VIP", "Jacuzzi", "Butler"]
        },
        {
            "id": 6,
            "name": "Honeymoon Suite",
            "price": 18000,
            "category": "suite",
            "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304",
            "guests": 2,
            "bed": "King Bed",
            "size": "120m²",
            "description": "Romantic retreat with ocean views, champagne service, and rose petal arrangements. Perfect for newlyweds.",
            "tags": ["Romantic", "Ocean View", "Champagne"]
        }
    ]
}
# ============================================
# HELPERS
# ============================================

def parse_price(value):
    if isinstance(value, int):
        return value
    cleaned = re.sub(r'[^\d]', '', str(value))
    return int(cleaned) if cleaned else 0

def calculate_nights(check_in, check_out):
    try:
        start = datetime.strptime(check_in, '%Y-%m-%d')
        end = datetime.strptime(check_out, '%Y-%m-%d')
        nights = (end - start).days
        return max(nights, 0)
    except Exception:
        return 0

def calculate_total(room_price, nights):
    subtotal = room_price * nights
    vat = int(subtotal * 0.075)
    return subtotal + vat

def verify_paystack_payment(reference):
    headers = {'Authorization': f'Bearer {PAYSTACK_SECRET}'}
    response = requests.get(
        f'https://api.paystack.co/transaction/verify/{reference}',
        headers=headers,
        timeout=30
    )
    return response.json()

# ============================================
# HOME ROUTE
# ============================================

@app.route('/')
def home():
    return render_template(
        'index.html',
        data=HOTEL_DATA,
        paystack_key=PAYSTACK_PUBLIC
    )

# ============================================
# INITIALIZE PAYMENT
# ============================================

@app.route('/api/initialize-payment', methods=['POST'])
def initialize_payment():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400

        email = data.get('email', 'guest@distancehotel.com.ng')
        amount = parse_price(data.get('amount', 0)) * 100

        if amount <= 0:
            return jsonify({'success': False, 'error': 'Invalid amount'}), 400

        headers = {
            'Authorization': f'Bearer {PAYSTACK_SECRET}',
            'Content-Type': 'application/json'
        }

        payload = {
            'email': email,
            'amount': amount,
            'callback_url': request.host_url + 'verify-payment',
            'metadata': {
                'room_name': data.get('room_name', ''),
                'guest_name': data.get('guest_name', ''),
                'phone': data.get('phone', ''),
                'check_in': data.get('check_in', ''),
                'check_out': data.get('check_out', '')
            }
        }

        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            json=payload,
            headers=headers,
            timeout=30
        )

        result = response.json()

        if result.get('status'):
            return jsonify({
                'success': True,
                'authorization_url': result['data']['authorization_url'],
                'reference': result['data']['reference']
            })

        return jsonify({
            'success': False,
            'error': result.get('message', 'Payment failed')
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# VERIFY PAYMENT (PAYSTACK CALLBACK)
# ============================================

@app.route('/verify-payment')
def verify_payment():
    reference = request.args.get('reference')
    if not reference:
        return "Missing payment reference", 400

    try:
        result = verify_paystack_payment(reference)

        if result.get('status') and result['data']['status'] == 'success':
            metadata = result['data'].get('metadata', {})
            email = result['data']['customer']['email']
            amount = result['data']['amount'] // 100

            nights = calculate_nights(
                metadata.get('check_in', ''),
                metadata.get('check_out', '')
            )

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO bookings (
                    room_name, guest_name, email, phone,
                    check_in, check_out, total_amount,
                    payment_status, paystack_ref
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metadata.get('room_name', ''),
                metadata.get('guest_name', ''),
                email,
                metadata.get('phone', ''),
                metadata.get('check_in', ''),
                metadata.get('check_out', ''),
                amount,
                'paid',
                reference
            ))

            conn.commit()
            conn.close()

            return render_template(
                'payment_success.html',
                reference=reference,
                amount=amount
            )

        return render_template('payment_failed.html', reference=reference)

    except Exception as e:
        return f"Error: {str(e)}", 500
# ============================================
# BOOKING API (NO PAYMENT)
# ============================================

@app.route('/api/book', methods=['POST'])
def api_book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        required = ['room_name', 'guest_name', 'phone', 'check_in', 'check_out']
        for field in required:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing {field}'}), 400

        nights = calculate_nights(data['check_in'], data['check_out'])
        if nights <= 0:
            return jsonify({'success': False, 'error': 'Invalid dates'}), 400

        # Find room price
        room_price = 0
        for room in HOTEL_DATA['rooms']:
            if room['name'] == data['room_name']:
                room_price = room['price']
                break

        total = calculate_total(room_price, nights)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO bookings (
                room_name, guest_name, email, phone,
                check_in, check_out, guests, requests,
                total_amount, payment_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['room_name'],
            data['guest_name'],
            data.get('email', ''),
            data['phone'],
            data['check_in'],
            data['check_out'],
            data.get('guests', 1),
            data.get('requests', ''),
            total,
            data.get('payment_status', 'pending')
        ))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Booking saved',
            'total': total,
            'nights': nights
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# NEWSLETTER API
# ============================================

@app.route('/api/subscribe', methods=['POST'])
def api_subscribe():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()

        if not email or '@' not in email:
            return jsonify({'success': False, 'error': 'Invalid email'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR IGNORE INTO subscribers (email)
            VALUES (?)
        ''', (email,))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Subscribed successfully'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# CONTACT API
# ============================================

@app.route('/api/contact', methods=['POST'])
def api_contact():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return jsonify({'success': False, 'error': 'All fields required'}), 400

        if not validate_email_simple(email):
            return jsonify({'success': False, 'error': 'Invalid email'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO contacts (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, data.get('subject', 'General Inquiry'), message))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Message sent successfully'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def validate_email_simple(email):
    return '@' in email and '.' in email.split('@')[-1]

# ============================================
# ADMIN DASHBOARD
# ============================================

# ============================================
# ADMIN DASHBOARD (SECURED)
# ============================================

@app.route('/admin')
def admin():
    # CHECK: Is the user logged in?
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
    bookings = cursor.fetchall()

    cursor.execute("SELECT * FROM subscribers ORDER BY id DESC")
    subscribers = cursor.fetchall()

    # Revenue calculation
    total_revenue = sum(
        b['total_amount'] or 0 for b in bookings
        if b['payment_status'] == 'paid'
    )

    # Stats
    total_bookings = len(bookings)
    paid_bookings = sum(1 for b in bookings if b['payment_status'] == 'paid')
    pending_bookings = sum(1 for b in bookings if b['payment_status'] == 'pending')

    conn.close()

    return render_template(
        'admin.html',
        bookings=bookings,
        subscribers=subscribers,
        total_revenue=total_revenue,
        total_bookings=total_bookings,
        paid_bookings=paid_bookings,
        pending_bookings=pending_bookings
    )

# ============================================
# ADMIN API ACTIONS
# ============================================

@app.route('/api/admin/confirm/<int:booking_id>', methods=['POST'])
def confirm_booking(booking_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE bookings
            SET payment_status = 'paid'
            WHERE id = ?
        ''', (booking_id,))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Booking confirmed'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/delete/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Booking deleted'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Route not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

# ============================================
# HEALTH CHECK
# ============================================

@app.route('/health')
def health_check():
    try:
        conn = get_db_connection()
        conn.execute('SELECT 1')
        conn.close()
        db_status = 'connected'
    except Exception:
        db_status = 'error'

    return jsonify({
        'status': 'ok',
        'database': db_status,
        'service': 'Distance Hotel API',
        'version': '3.0.0'
    })
    
    
   @app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == 'admin' and pwd == 'Distance2026':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return "Invalid login details", 401
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================
# RUN SERVER
# ============================================

if __name__ == '__main__':
    # host='0.0.0.0' is required for Render to see the app
    app.run(debug=True, host='0.0.0.0', port=5000)
