expanded_brain = '''# hotel_brain.py
# THE KNOWLEDGE VAULT FOR DISTANCE HOTEL
# Expanded Edition — Deep Knowledge Base

HOTEL_KNOWLEDGE = {
    # ─── PRICING & ROOMS ───
    "price": "Our room rates start from ₦8,500 (Standard Fan) up to ₦45,000 (Presidential Suite). All rates include complimentary breakfast and WiFi. Prices may vary during peak seasons like Christmas, Eid, and New Year.",
    "rates": "Standard Fan Room: ₦8,500/night | Deluxe Room: ₦12,000/night | Executive AC Room: ₦15,000/night | Honeymoon Suite: ₦18,000/night | Royal Suite: ₦25,000/night | Presidential Suite: ₦45,000/night. All include VAT.",
    "cheap": "Our most affordable option is the Standard Fan Room at ₦8,500 per night. It includes a queen bed, free WiFi, and a ceiling fan. Perfect for budget travelers.",
    "expensive": "Our most luxurious option is the Presidential Suite at ₦45,000 per night. It spans 280m² with a private terrace, jacuzzi, dedicated butler service, and premium furnishings.",
    "discount": "We offer corporate discounts for extended stays (7+ nights), group bookings (5+ rooms), and loyalty program members. Contact our reservations team for a custom quote.",
    "promo": "Current promotions include: 'Stay 3 Nights, Pay for 2' on weekdays, and 15% off for early bookings made 30 days in advance.",
    
    # ─── INDIVIDUAL ROOMS ───
    "standard": "The Standard Fan Room (₦8,500/night, 28m²) features a queen bed, ceiling fan, free WiFi, en-suite bathroom with shower, and a small work desk. Ideal for solo travelers or short stays.",
    "deluxe": "The Deluxe Room (₦12,000/night, 32m²) features air conditioning, a queen bed, premium bedding, a spacious work desk, 32-inch Smart TV, mini fridge, and complimentary toiletries.",
    "executive": "The Executive AC Room (₦15,000/night, 35m²) offers a king-size bed, 43-inch Smart TV with Netflix, air conditioning, premium furnishings, a large work desk, and a rain shower.",
    "royal": "The Royal Suite (₦25,000/night, 65m²) includes a separate living area, king bed, enhanced security features, two Smart TVs, a dining area, and VIP check-in service.",
    "presidential": "The Presidential Suite (₦45,000/night, 280m²) is our crown jewel. Features: private terrace with city views, personal jacuzzi, dedicated butler on-call 24/7, two bedrooms, a private kitchenette, home theater system, and limousine airport pickup.",
    "honeymoon": "The Honeymoon Suite (₦18,000/night, 120m²) is a romantic paradise with a king bed, ocean-view balcony, champagne welcome package, rose petal turndown service, couples' spa voucher, and late checkout (2 PM).",
    
    # ─── ROOM FEATURES & AMENITIES ───
    "bed": "We offer queen beds in Standard and Deluxe rooms, king beds in Executive, Royal, Honeymoon, and Presidential suites. All mattresses are orthopedic pillow-top for maximum comfort.",
    "tv": "All rooms except Standard have Smart TVs with Netflix, YouTube, and local channels. The Presidential Suite has a full home theater system.",
    "ac": "Air conditioning is available in Deluxe, Executive, Royal, Honeymoon, and Presidential rooms. The Standard room has a powerful ceiling fan.",
    "bathroom": "All rooms have en-suite bathrooms. Deluxe and above feature rain showers. The Presidential Suite has both a rain shower and a jacuzzi tub.",
    "fridge": "Mini fridges are available in Deluxe and above, stocked with complimentary water, soft drinks, and snacks (replenished daily).",
    "balcony": "The Honeymoon Suite has a private ocean-view balcony. The Presidential Suite has a large private terrace with outdoor seating.",
    "view": "Standard and Deluxe rooms have garden views. Executive rooms have city views. Honeymoon Suite has ocean views. Presidential Suite has panoramic city and pool views.",
    "size": "Room sizes: Standard 28m² | Deluxe 32m² | Executive 35m² | Royal Suite 65m² | Honeymoon Suite 120m² | Presidential Suite 280m².",
    
    # ─── LOCATION & DIRECTIONS ───
    "location": "Distance Hotel is located at 1 Distance Boulevard, Oro, Kwara State, Nigeria. We are the premier luxury hotel in the region, just 45 minutes from Ilorin International Airport.",
    "address": "1 Distance Boulevard, Oro, Kwara State, Nigeria. Postal code: 240001.",
    "directions": "From Ilorin: Take the Ilorin-Oro Expressway for 45 minutes. From Offa: Take the Offa-Oro Road for 30 minutes. From Lagos: Drive via the Lagos-Ibadan-Ilorin Expressway (approx. 4.5 hours). We offer airport pickup services.",
    "nearby": "Nearby attractions include: Oro Central Market (5 min), Kwara State University (20 min), Esie Museum (30 min), and the scenic Oro Hills (15 min).",
    "airport": "Ilorin International Airport (ILR) is the closest airport, 45 minutes away. We offer luxury airport transfers: Sedan (₦15,000), SUV (₦25,000), or Limousine for Presidential guests (complimentary).",
    
    # ─── CHECK-IN / CHECK-OUT ───
    "check-in": "Check-in time is 2:00 PM. Early check-in (from 10 AM) is available for ₦5,000 extra, subject to room availability. Please bring a valid ID and your booking confirmation.",
    "check-out": "Check-out time is 11:00 AM. Late check-out (until 2 PM) costs ₦5,000. Until 4 PM costs ₦8,000. After 4 PM requires an extra night charge.",
    "early": "Early check-in is available from 10:00 AM for ₦5,000, depending on room availability. Contact us 24 hours in advance to arrange.",
    "late": "Late check-out is available until 2:00 PM for ₦5,000, or until 4:00 PM for ₦8,000. After 4 PM, a full extra night is charged.",
    "id": "You need a valid government-issued ID (National ID, Driver's License, International Passport, or Voter's Card) at check-in. We do not accept photocopies.",
    "deposit": "A refundable security deposit of ₦10,000 is required for all bookings. It covers potential damages or mini-bar usage and is returned at check-out after room inspection.",
    
    # ─── BOOKING & RESERVATIONS ───
    "booking": "You can book directly on our website via the 'Book Now' button, call +234 800 000 0000, email reservations@distancehotel.com.ng, or WhatsApp us. We use Paystack for secure online payments.",
    "reserve": "To reserve a room, visit our website and click 'Book Now', or call our 24/7 reservations line at +234 800 000 0000. A 50% deposit is required to confirm your booking.",
    "cancel": "Free cancellation is available up to 24 hours before check-in. Cancellations within 24 hours incur a charge of one night's rate. No-shows are charged the full booking amount.",
    "refund": "Refunds are processed within 5-7 business days to your original payment method. For Paystack payments, refunds typically appear in 3-5 business days.",
    "modify": "You can modify your booking dates or room type up to 48 hours before check-in by calling reservations. Date changes may affect pricing.",
    "group": "For group bookings (5+ rooms), contact our Group Sales Manager at groups@distancehotel.com.ng or call +234 800 000 0001. Group rates include meeting room access and customized catering.",
    "corporate": "Our Corporate Partnership Program offers: discounted rates, direct billing, monthly invoicing, and dedicated account managers. Email corporate@distancehotel.com.ng to apply.",
    
    # ─── PAYMENT ───
    "payment": "We accept Visa, Mastercard, Verve cards, bank transfers, USSD payments, and Paystack. Cash payments are accepted at the front desk. All online payments are 256-bit SSL encrypted.",
    "pay": "Payment options: (1) Online via Paystack on our website, (2) Bank transfer to GTBank 0123456789 (Distance Hotel Ltd), (3) Cash at front desk, (4) POS terminal on-site.",
    "card": "We accept all major debit and credit cards: Visa, Mastercard, and Verve. American Express is accepted with a 3% surcharge. All card transactions are secure and PCI-DSS compliant.",
    "transfer": "Bank transfer details: GTBank | Account Name: Distance Hotel Ltd | Account Number: 0123456789. Please send proof of payment to reservations@distancehotel.com.ng with your booking name.",
    "receipt": "Electronic receipts are emailed automatically after payment. Physical receipts are available at the front desk. Corporate guests receive itemized invoices.",
    "invoice": "Corporate clients receive monthly itemized invoices. Individual guests can request a detailed receipt at check-out or via email to billing@distancehotel.com.ng.",
    
    # ─── DINING & RESTAURANTS ───
    "dining": "We have 4 dining venues: The Azure (fine dining, 6:30 AM - 11 PM), Sky Lounge (rooftop bar, 4 PM - 2 AM), Poolside Grill (casual, 10 AM - 8 PM), and Cafe Distance (coffee & pastries, 7 AM - 9 PM).",
    "restaurant": "The Azure is our signature restaurant offering continental and Nigerian fusion cuisine. Open for breakfast (6:30-10:30 AM), lunch (12-3 PM), and dinner (6-11 PM). Live piano on Friday and Saturday evenings.",
    "breakfast": "Complimentary breakfast is included with all room bookings. Served at The Azure from 6:30-10:30 AM. Options: Continental buffet, Full English, or traditional Nigerian (yam, eggs, akara, pap).",
    "lunch": "Lunch is served at The Azure (12-3 PM) and Poolside Grill (12-8 PM). A la carte menu with Nigerian and international options. Average cost: ₦3,500-₦7,000 per person.",
    "dinner": "Dinner at The Azure (6-11 PM) features our chef's specials, including grilled catfish, jollof rice, pasta, steaks, and vegetarian options. Reservations recommended for weekends.",
    "bar": "Sky Lounge is our rooftop bar on the 5th floor, open 4 PM - 2 AM. Features craft cocktails, premium spirits, local and imported beers, and a wine list. Happy Hour: 4-7 PM (30% off all drinks).",
    "room service": "24-hour room service is available. Menu includes light bites, full meals, and beverages. Service charge: 10%. Average delivery time: 25 minutes.",
    "menu": "Our menus include: Nigerian specialties (jollof, pounded yam, egusi, suya), Continental dishes (pastas, steaks, salads), Seafood (grilled catfish, prawns), and Vegetarian/Vegan options.",
    "alcohol": "Alcoholic beverages are served at Sky Lounge and The Azure. We stock local beers (Star, Gulder, Heineken), imported wines, spirits, and signature cocktails. Must be 18+ to purchase.",
    "special diet": "We accommodate special dietary needs: vegetarian, vegan, gluten-free, halal, and diabetic-friendly meals. Please inform us 24 hours in advance.",
    
    # ─── AMENITIES & FACILITIES ───
    "wifi": "Complimentary high-speed fiber-optic WiFi (100 Mbps) is available in all rooms, restaurants, lobby, and pool area. Network name: 'Distance_Guest' — no password required.",
    "internet": "Free high-speed internet is available throughout the hotel. For business guests requiring dedicated bandwidth, we offer premium connections at ₦2,000/day.",
    "pool": "Our Olympic-size infinity pool is open 6 AM - 10 PM daily. Features a swim-up bar, loungers, and towel service. Children under 12 must be supervised. Poolside Grill serves refreshments.",
    "gym": "The fitness center is open 24/7 with modern cardio machines, free weights, yoga mats, and a stretching area. Personal trainers available 6 AM - 9 PM (₦5,000/session).",
    "spa": "Our Spa & Wellness center offers: Swedish massage (₦15,000/60min), Deep tissue (₦18,000/60min), Hot stone therapy (₦20,000/90min), Facials (₦12,000), and Manicure/Pedicure (₦8,000). Open 9 AM - 9 PM.",
    "parking": "We offer secured underground valet parking for ₦2,000/night. Free outdoor self-parking is also available. All parking areas have 24/7 CCTV coverage.",
    "laundry": "Laundry and dry cleaning services available. Same-day service if dropped off before 9 AM. Pricing: Shirt ₦800, Suit ₦2,500, Dress ₦2,000. Express service (4 hours) available at 50% surcharge.",
    "business": "Our Business Center includes: 3 meeting rooms, co-working space, printing/scanning, video conferencing setup, and secretarial services. Meeting rooms: ₦15,000/half-day, ₦25,000/full-day.",
    "meeting": "We have 3 meeting rooms: Boardroom (20 people), Conference Room (50 people), and Training Room (30 people). All include projector, whiteboard, flip chart, and complimentary water.",
    "conference": "The Grand Ballroom accommodates up to 500 guests for conferences, weddings, and galas. Features: crystal chandeliers, stage, AV system, simultaneous translation booths, and customizable lighting.",
    "event": "Our event spaces include: Grand Ballroom (500 guests), Garden Terrace (150 guests), and Executive Boardroom (20 guests). Wedding packages start at ₦500,000. Contact events@distancehotel.com.ng.",
    "wedding": "Wedding packages include: venue decoration, catering, bridal suite, guest accommodation discounts, and event coordination. Packages start at ₦500,000 for 100 guests. Custom packages available.",
    "kids": "The Kids Club (ages 4-12) offers supervised activities: arts & crafts, games, movie time, and a playground. Open 9 AM - 6 PM. Babysitting service available: ₦3,000/hour.",
    "pet": "We are a pet-friendly hotel! Pets up to 15kg are welcome in designated rooms for ₦5,000/night pet fee. Pet bed, bowls, and treats provided. Please inform us when booking.",
    "smoking": "Distance Hotel is a non-smoking property. Smoking is permitted only in designated outdoor areas. A ₦50,000 cleaning fee applies for smoking in rooms.",
    "accessible": "We have 4 fully accessible rooms with wheelchair ramps, grab bars, roll-in showers, and lowered fixtures. The pool has a wheelchair lift. Please request when booking.",
    
    # ─── SERVICES ───
    "concierge": "Our 24/7 concierge can assist with: restaurant reservations, tour bookings, transportation, flower delivery, gift shopping, and local recommendations. Dial 0 from your room phone.",
    "tour": "We organize local tours: Oro Heritage Tour (₦8,000/person), Kwara State Museum Visit (₦5,000), and Ilorin City Tour (₦12,000). All include transportation and a guide.",
    "transport": "Transportation services: Airport pickup (Sedan ₦15,000, SUV ₦25,000), Local taxi (₦2,000-₦5,000 depending on distance), and Car rental (₦20,000/day with driver).",
    "butler": "Butler service is exclusive to Presidential Suite guests. Your dedicated butler handles: unpacking/packing, garment pressing, shoe shining, personal shopping, and itinerary planning.",
    "housekeeping": "Daily housekeeping is included. Turn-down service is provided from 6-9 PM for Deluxe and above. Extra towels, pillows, or toiletries available on request (dial 1 from room phone).",
    "doctor": "A registered nurse is on-site 24/7. A visiting doctor is available on-call. The nearest hospital is Oro General Hospital (10 minutes away). First aid kits are in all public areas.",
    "currency": "Currency exchange is available at the front desk for USD, GBP, and EUR. Rates are updated daily based on CBN official rates. We also have an ATM in the lobby.",
    "atm": "There is a GTBank ATM in the main lobby, available 24/7. It accepts all Nigerian cards and international Visa/Mastercard.",
    
    # ─── POLICIES ───
    "policy": "Hotel policies: Check-in 2 PM, Check-out 11 AM, No smoking in rooms, No parties without approval, Quiet hours 10 PM - 7 AM, Visitors must register at front desk, and Pets only in designated rooms.",
    "age": "Guests must be 18+ to book a room. Minors (under 18) must be accompanied by a parent or guardian. Valid ID is required for all guests.",
    "visitor": "Visitors are welcome until 10 PM. Overnight visitors must be registered at the front desk and may incur additional charges. All visitors must provide ID.",
    "party": "Private parties and events in rooms require advance approval from management. A security deposit of ₦50,000 is required. Noise must be kept to reasonable levels.",
    "damage": "Guests are liable for any damages caused to hotel property. Charges will be deducted from the security deposit or billed to the guest's account.",
    "lost": "Lost and found items are kept for 30 days. Contact front desk with a description. We can ship items to you at your expense. Unclaimed items are donated to charity after 30 days.",
    
    # ─── REVIEWS & REPUTATION ───
    "review": "Distance Hotel has a 4.9/5 rating based on 1,247 verified reviews. 92% of guests rate us 5 stars. Guests praise our cleanliness, staff professionalism, and food quality.",
    "rating": "We are rated 4.9 out of 5 stars across all major platforms: Google (4.9), Booking.com (4.8), and TripAdvisor (4.9). We are the #1 rated hotel in Kwara State.",
    "award": "Awards: 'Best Luxury Hotel in Kwara' 2024 & 2025, 'Nigerian Hospitality Excellence Award' 2023, and 'Travelers' Choice' by TripAdvisor for three consecutive years.",
    
    # ─── CONTACT & SUPPORT ───
    "contact": "Reach us: Phone +234 800 000 0000 (24/7), WhatsApp +234 800 000 0000, Email reservations@distancehotel.com.ng, or visit 1 Distance Boulevard, Oro, Kwara State.",
    "phone": "Reservations: +234 800 000 0000 (24/7). Front Desk: +234 800 000 0000. Events: +234 800 000 0001. Corporate: +234 800 000 0002. Emergency: Dial 0 from any room phone.",
    "email": "General: info@distancehotel.com.ng | Reservations: reservations@distancehotel.com.ng | Events: events@distancehotel.com.ng | Corporate: corporate@distancehotel.com.ng | Billing: billing@distancehotel.com.ng",
    "whatsapp": "Chat with us on WhatsApp: +234 800 000 0000. Available 24/7 for bookings, inquiries, and support. We typically respond within 5 minutes.",
    "complaint": "We take complaints seriously. Please speak to the Duty Manager on-site, email complaints@distancehotel.com.ng, or call +234 800 000 0003. We aim to resolve all issues within 24 hours.",
    "feedback": "We love feedback! Share your experience via email to feedback@distancehotel.com.ng, our website review form, or Google Reviews. All feedback is reviewed by our management team.",
    
    # ─── STAFF & MANAGEMENT ───
    "manager": "Our General Manager is Mr. Tunde Bakare, with 20+ years in luxury hospitality. The Resident Manager is Mrs. Ngozi Eze, available daily from 8 AM - 6 PM.",
    "staff": "Our team of 120 staff includes professionally trained housekeepers, chefs, security personnel, and concierge. All staff undergo quarterly hospitality training.",
    
    # ─── HISTORY & BRAND ───
    "history": "Distance Hotel opened in 2018 as a boutique property and has grown into Kwara State's premier luxury hotel. We have hosted dignitaries, celebrities, and international delegates.",
    "about": "Distance Hotel is a proudly Nigerian luxury brand. Our philosophy: 'Where distance meets luxury.' We blend international hospitality standards with warm Nigerian hospitality.",
    "sustainability": "We are committed to sustainability: solar water heating, rainwater harvesting, energy-efficient lighting, local sourcing (80% of food from Kwara farmers), and zero single-use plastics in rooms.",
    
    # ─── EMERGENCY & SAFETY ───
    "emergency": "In case of emergency, dial 0 from any room phone to reach the front desk. Fire extinguishers are on every floor. Emergency exits are marked with green lighting. Assembly point is the front parking lot.",
    "fire": "Fire safety: Smoke detectors in all rooms, fire extinguishers on every floor, sprinkler system throughout, and fire drills conducted quarterly. Emergency exits are clearly marked.",
    "medical": "Medical emergencies: Dial 0 for the front desk. A registered nurse is on-site 24/7. Oro General Hospital is 10 minutes away. First aid kits are located on every floor.",
    "security": "Your safety is our priority. We have: 24/7 CCTV coverage (120+ cameras), armed security personnel at all entrances, electronic key card access, and a secure perimeter fence. All vehicles are screened on entry.",
    
    # ─── LOCAL AREA ───
    "oro": "Oro is a historic town in Kwara State, known for its rich cultural heritage, traditional weaving, and warm hospitality. The town has a popul