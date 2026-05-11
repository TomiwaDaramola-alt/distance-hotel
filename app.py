import os
import sqlite3
import requests
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from hotel_brain import HOTEL_KNOWLEDGE


# Load environment variables
load_dotenv()

app = Flask(__name__)

# ============================================
# CONFIGURATION & SECURITY
# ============================================
app.secret_key = os.environ.get('453e6852331b7018e76017922453975adfa26b65', 'distance-hotel-secret-2026')

PAYSTACK_SECRET = os.environ.get(
    'PAYSTACK_SECRET_KEY',
    'sk_test_453e6852331b7018e76017922453975adfa26b65'
)

PAYSTACK_PUBLIC = os.environ.get(
    'PAYSTACK_PUBLIC_KEY',
    'pk_test_a49bd26daf79787b5fde3f01f093a548c00e7665'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'distance_hotel.db')

# ============================================
# DATABASE HELPERS
# ============================================

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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

# Initialize Database on Startup
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
            "description": "Comfortable and affordable accommodation perfect for budget-conscious travelers.",
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
            "description": "Upgraded comfort with air conditioning, premium bedding, and a work desk.",
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
            "description": "Spacious room with air conditioning, smart TV, and premium furnishings.",
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
            "description": "Ultimate luxury with separate living area and premium amenities.",
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
            "description": "The pinnacle of luxury. Private terrace, jacuzzi, and dedicated butler service.",
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
            "description": "Romantic retreat with ocean views and champagne service.",
            "tags": ["Romantic", "Ocean View", "Champagne"]
        }
    ]
}

# ============================================
# LOGIC HELPERS
# ============================================

def parse_price(value):
    if isinstance(value, int): return value
    cleaned = re.sub(r'[^\d]', '', str(value))
    return int(cleaned) if cleaned else 0

def calculate_nights(check_in, check_out):
    try:
        start = datetime.strptime(check_in, '%Y-%m-%d')
        end = datetime.strptime(check_out, '%Y-%m-%d')
        return max((end - start).days, 0)
    except: return 0

def calculate_total(room_price, nights):
    subtotal = room_price * nights
    vat = int(subtotal * 0.075)
    return subtotal + vat

# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    return render_template('index.html', data=HOTEL_DATA, paystack_key=PAYSTACK_PUBLIC)

@app.route('/api/initialize-payment', methods=['POST'])
def initialize_payment():
    try:
        data = request.get_json()
        email = data.get('email', 'guest@distancehotel.com.ng')
        amount = parse_price(data.get('amount', 0)) * 100
        
        headers = {'Authorization': f'Bearer {PAYSTACK_SECRET}', 'Content-Type': 'application/json'}
        payload = {
            'email': email, 'amount': amount,
            'callback_url': request.host_url + 'verify-payment',
            'metadata': data
        }
        r = requests.post('https://api.paystack.co/transaction/initialize', json=payload, headers=headers)
        res = r.json()
        return jsonify({'success': True, 'authorization_url': res['data']['authorization_url']}) if res.get('status') else jsonify({'success': False})
    except Exception as e: return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/verify-payment')
def verify_payment():
    reference = request.args.get('reference')
    headers = {'Authorization': f'Bearer {PAYSTACK_SECRET}'}
    r = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
    result = r.json()
    
    if result.get('status') and result['data']['status'] == 'success':
        meta = result['data'].get('metadata', {})
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (room_name, guest_name, email, phone, check_in, check_out, total_amount, payment_status, paystack_ref) VALUES (?,?,?,?,?,?,?,?,?)',
                     (meta.get('room_name'), meta.get('guest_name'), result['data']['customer']['email'], meta.get('phone'), meta.get('check_in'), meta.get('check_out'), result['data']['amount']//100, 'paid', reference))
        conn.commit()
        conn.close()
        return render_template('payment_success.html', reference=reference)
    return render_template('payment_failed.html')

# ============================================
# ADMIN & LOGIN (FIXED HEAD TO TOE)
# ============================================

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

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    bookings = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
    subscribers = conn.execute("SELECT * FROM subscribers ORDER BY id DESC").fetchall()
    
    total_revenue = sum(b['total_amount'] or 0 for b in bookings if b['payment_status'] == 'paid')
    total_bookings = len(bookings)
    paid_bookings = sum(1 for b in bookings if b['payment_status'] == 'paid')
    pending_bookings = sum(1 for b in bookings if b['payment_status'] == 'pending')
    
    conn.close()
    return render_template('admin.html', 
                           bookings=bookings, 
                           subscribers=subscribers, 
                           total_revenue=total_revenue, 
                           total_bookings=total_bookings,
                           paid_bookings=paid_bookings,
                           pending_bookings=pending_bookings)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Default response if AI doesn't know the answer
        response = "I'm not quite sure about that. Please contact our reception or check our room details for more info."
        
        # Look through the separate brain file
        for key, value in HOTEL_KNOWLEDGE.items():
            if key in user_message:
                response = value
                break
                
        return jsonify({'reply': response})
    except Exception as e:
        return jsonify({'reply': "My brain is a bit foggy right now. Try again?"}), 500
