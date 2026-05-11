// ============================================
// DISTANCE HOTEL — JAVASCRIPT ENGINE
// Version: 3.0.0
// ============================================

// ============================================
// GLOBAL STATE
// ============================================

const STATE = {
    currentRoom: null,
    currentPrice: 0,
    currency: '₦',
    isMenuOpen: false,
    scrollY: 0,
    lastScrollY: 0,
    toastTimer: null,
    prefersDark: window.matchMedia('(prefers-color-scheme: dark)').matches
};

// ============================================
// DOM CACHE
// ============================================

const DOM = {};

function cacheDOM() {
    // Navigation
    DOM.navbar = document.getElementById('navbar');
    DOM.menuIcon = document.getElementById('menuIcon');
    DOM.mobileMenu = document.getElementById('mobileMenu');

    // Room elements
    DOM.roomCards = document.querySelectorAll('.room-card');
    DOM.filterBtns = document.querySelectorAll('.filter-btn');

    // Date inputs
    DOM.checkIn = document.getElementById('checkIn');
    DOM.checkOut = document.getElementById('checkOut');
    DOM.modalCheckIn = document.getElementById('modalCheckIn');
    DOM.modalCheckOut = document.getElementById('modalCheckOut');

    // Modal elements
    DOM.bookingModal = document.getElementById('bookingModal');
    DOM.detailsModal = document.getElementById('detailsModal');
    DOM.modalRoomName = document.getElementById('modalRoomName');
    DOM.summaryRoom = document.getElementById('summaryRoom');
    DOM.summaryPrice = document.getElementById('summaryPrice');
    DOM.summaryDates = document.getElementById('summaryDates');
    DOM.rateTotal = document.getElementById('rateTotal');
    DOM.taxTotal = document.getElementById('taxTotal');
    DOM.grandTotal = document.getElementById('grandTotal');

    // Detail modal elements
    DOM.detailImage = document.getElementById('detailImage');
    DOM.detailTitle = document.getElementById('detailTitle');
    DOM.detailDesc = document.getElementById('detailDesc');
    DOM.detailPrice = document.getElementById('detailPrice');
    DOM.detailGuests = document.getElementById('detailGuests');
    DOM.detailSize = document.getElementById('detailSize');
    DOM.detailBed = document.getElementById('detailBed');

    // Toast
    DOM.toast = document.getElementById('toast');
    DOM.toastMessage = document.getElementById('toastMessage');

    // Back to top
    DOM.backToTop = document.getElementById('backToTop');

    // Body data
    DOM.whatsapp = document.body.dataset.whatsapp || '';
    DOM.hotelName = document.body.dataset.hotelName || 'Distance Hotel';
    DOM.paystackKey = document.body.dataset.paystackKey || '';

    console.log('✅ DOM cached:', DOM.roomCards.length, 'room cards found');
}

// ============================================
// SAFE QUERY HELPERS
// ============================================

function $(selector, parent = document) {
    try {
        return parent.querySelector(selector);
    } catch (error) {
        console.warn('Invalid selector:', selector);
        return null;
    }
}

function $$(selector, parent = document) {
    try {
        return parent.querySelectorAll(selector);
    } catch (error) {
        console.warn('Invalid selector:', selector);
        return [];
    }
}

// ============================================
// PRICE UTILITIES
// ============================================

function parsePrice(price) {
    if (typeof price === 'number') return price;
    if (!price) return 0;
    return parseInt(String(price).replace(/[^\d]/g, ''), 10) || 0;
}

function formatPrice(amount) {
    const safeAmount = Number(amount) || 0;
    return STATE.currency + safeAmount.toLocaleString('en-NG');
}

// ============================================
// DATE UTILITIES
// ============================================

function calculateNights(checkIn, checkOut) {
    if (!checkIn || !checkOut) return 0;
    const start = new Date(checkIn);
    const end = new Date(checkOut);
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) return 0;
    const diff = end.getTime() - start.getTime();
    if (diff <= 0) return 0;
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

function validateDateRange(checkIn, checkOut) {
    const nights = calculateNights(checkIn, checkOut);
    if (!nights) return { valid: false, message: 'Invalid booking dates' };
    if (nights > 30) return { valid: false, message: 'Maximum stay is 30 nights' };
    return { valid: true, nights };
}

// ============================================
// VALIDATION HELPERS
// ============================================

function validateEmail(email) {
    if (!email) return false;
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePhone(phone) {
    if (!phone) return false;
    const cleaned = String(phone).replace(/\D/g, '');
    return cleaned.length >= 10;
}

// ============================================
// TOAST SYSTEM
// ============================================

function showToast(message, duration = 3000) {
    if (!DOM.toast || !DOM.toastMessage) {
        console.log('Toast:', message);
        return;
    }

    clearTimeout(STATE.toastTimer);

    DOM.toastMessage.textContent = String(message);
    DOM.toast.classList.remove('show');

    // Force reflow
    void DOM.toast.offsetWidth;

    DOM.toast.classList.add('show');

    STATE.toastTimer = setTimeout(() => {
        DOM.toast.classList.remove('show');
    }, duration);
}

// ============================================
// SMOOTH SCROLL
// ============================================

function scrollToSection(id) {
    if (!id) return;
    const targetId = id.startsWith('#') ? id : `#${id}`;
    const target = document.querySelector(targetId);
    if (!target) {
        console.warn('Section not found:', targetId);
        return;
    }

    const navHeight = DOM.navbar?.offsetHeight || 80;
    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 10;

    window.scrollTo({
        top: Math.max(targetPosition, 0),
        behavior: 'smooth'
    });

    closeMobileMenu();
}

function initSmoothScroll() {
    $$('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (!href || href === '#') return;
            e.preventDefault();
            scrollToSection(href);
        });
    });
}

// ============================================
// MOBILE MENU
// ============================================

function toggleMobileMenu() {
    if (!DOM.mobileMenu || !DOM.menuIcon) return;

    STATE.isMenuOpen = !STATE.isMenuOpen;

    DOM.mobileMenu.classList.toggle('active', STATE.isMenuOpen);
    DOM.menuIcon.classList.toggle('fa-bars', !STATE.isMenuOpen);
    DOM.menuIcon.classList.toggle('fa-times', STATE.isMenuOpen);
    document.body.classList.toggle('menu-open', STATE.isMenuOpen);
}

function closeMobileMenu() {
    if (!STATE.isMenuOpen || !DOM.mobileMenu || !DOM.menuIcon) return;

    STATE.isMenuOpen = false;
    DOM.mobileMenu.classList.remove('active');
    DOM.menuIcon.classList.remove('fa-times');
    DOM.menuIcon.classList.add('fa-bars');
    document.body.classList.remove('menu-open');
}

// ============================================
// NAVBAR SCROLL
// ============================================

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function initNav() {
    if (!DOM.navbar) return;

    const handleScroll = throttle(() => {
        const currentScroll = window.scrollY || window.pageYOffset;
        STATE.scrollY = currentScroll;

        DOM.navbar.classList.toggle('scrolled', currentScroll > 50);
        DOM.navbar.classList.toggle('hidden', currentScroll > STATE.lastScrollY && currentScroll > 300);
        STATE.lastScrollY = currentScroll;

        // Back to top visibility
        if (DOM.backToTop) {
            DOM.backToTop.classList.toggle('visible', currentScroll > 600);
        }
    }, 16);

    window.addEventListener('scroll', handleScroll, { passive: true });
}

// ============================================
// MODAL SYSTEM
// ============================================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.warn('Modal not found:', modalId);
        return;
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.body.classList.add('modal-open');
    closeMobileMenu();
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.body.classList.remove('modal-open');
}

function closeBookingModal() {
    closeModal('bookingModal');
    const form = document.querySelector('#bookingModal form');
    if (form) form.reset();
    updateBookingTotal();
}

function closeDetailsModal() {
    closeModal('detailsModal');
}

function initModalBackdropClose() {
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('modal-backdrop')) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
                document.body.classList.remove('modal-open');
            }
        });
    });
}
// ============================================
// BOOKING MODAL
// ============================================

function openBookingModal(roomName, price) {
    STATE.currentRoom = roomName;
    STATE.currentPrice = parsePrice(price);

    if (DOM.modalRoomName) DOM.modalRoomName.textContent = roomName;
    if (DOM.summaryRoom) DOM.summaryRoom.textContent = roomName;
    if (DOM.summaryPrice) DOM.summaryPrice.textContent = formatPrice(STATE.currentPrice) + '/night';

    // Copy dates from hero to modal
    if (DOM.checkIn && DOM.modalCheckIn && DOM.checkIn.value) {
        DOM.modalCheckIn.value = DOM.checkIn.value;
    }
    if (DOM.checkOut && DOM.modalCheckOut && DOM.checkOut.value) {
        DOM.modalCheckOut.value = DOM.checkOut.value;
    }

    updateBookingTotal();
    openModal('bookingModal');
}

function updateBookingTotal() {
    if (!DOM.modalCheckIn || !DOM.modalCheckOut) return;

    const nights = calculateNights(DOM.modalCheckIn.value, DOM.modalCheckOut.value);

    if (nights <= 0) {
        if (DOM.summaryDates) DOM.summaryDates.textContent = 'Select valid dates';
        if (DOM.rateTotal) DOM.rateTotal.textContent = formatPrice(STATE.currentPrice) + ' × 0 nights';
        if (DOM.taxTotal) DOM.taxTotal.textContent = formatPrice(0);
        if (DOM.grandTotal) DOM.grandTotal.textContent = formatPrice(0);
        return;
    }

    const subtotal = STATE.currentPrice * nights;
    const tax = Math.round(subtotal * 0.075);
    const total = subtotal + tax;

    if (DOM.summaryDates) {
        DOM.summaryDates.textContent = `${nights} night${nights > 1 ? 's' : ''} total`;
    }
    if (DOM.rateTotal) {
        DOM.rateTotal.textContent = `${formatPrice(STATE.currentPrice)} × ${nights} nights`;
    }
    if (DOM.taxTotal) DOM.taxTotal.textContent = formatPrice(tax);
    if (DOM.grandTotal) DOM.grandTotal.textContent = formatPrice(total);
}

function switchToBooking() {
    closeDetailsModal();
    openBookingModal(STATE.currentRoom, STATE.currentPrice);
}

// ============================================
// ROOM DETAILS MODAL
// ============================================

function viewRoomDetails(roomName) {
    // Find room data from window.data or fallback
    const roomData = findRoomData(roomName);
    if (!roomData) {
        showToast('Room details not found');
        return;
    }

    STATE.currentRoom = roomData.name;
    STATE.currentPrice = roomData.price;

    if (DOM.detailImage) DOM.detailImage.src = roomData.image + '?w=1200';
    if (DOM.detailTitle) DOM.detailTitle.textContent = roomData.name;
    if (DOM.detailDesc) DOM.detailDesc.textContent = roomData.description;
    if (DOM.detailPrice) DOM.detailPrice.textContent = formatPrice(roomData.price);
    if (DOM.detailGuests) DOM.detailGuests.innerHTML = `<i class="fas fa-user-friends"></i> ${roomData.guests} Guests`;
    if (DOM.detailSize) DOM.detailSize.innerHTML = `<i class="fas fa-ruler-combined"></i> ${roomData.size}`;
    if (DOM.detailBed) DOM.detailBed.innerHTML = `<i class="fas fa-bed"></i> ${roomData.bed}`;

    // Populate amenities
    const amenitiesContainer = document.getElementById('detailAmenities');
    if (amenitiesContainer && roomData.tags) {
        amenitiesContainer.innerHTML = roomData.tags.map(tag => 
            `<span class="room-tag">${tag}</span>`
        ).join('');
    }

    openModal('detailsModal');
}

function findRoomData(roomName) {
    // Try window.data first
    if (window.data && window.data.rooms) {
        const found = window.data.rooms.find(r => r.name === roomName);
        if (found) return found;
    }

    // Fallback data
    const fallbackRooms = {
        'Standard Fan Room': {
            name: 'Standard Fan Room',
            price: 8500,
            image: 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304',
            guests: 2,
            size: '28m²',
            bed: 'Queen Bed',
            description: 'Comfortable and affordable accommodation perfect for budget-conscious travelers. Features a fan, free WiFi, and a cozy atmosphere.',
            tags: ['Fan', 'WiFi', 'Budget']
        },
        'Executive AC Room': {
            name: 'Executive AC Room',
            price: 15000,
            image: 'https://images.unsplash.com/photo-1566665797739-1674de7a421a',
            guests: 2,
            size: '35m²',
            bed: 'King Bed',
            description: 'Spacious room with air conditioning, smart TV, and premium furnishings. Ideal for business travelers seeking comfort and productivity.',
            tags: ['AC', 'Smart TV', 'Luxury']
        },
        'Royal Suite': {
            name: 'Royal Suite',
            price: 25000,
            image: 'https://images.unsplash.com/photo-1618773928121-c32242e63f39',
            guests: 4,
            size: '65m²',
            bed: 'King Bed',
            description: 'Ultimate luxury with separate living area, premium amenities, and stunning views. The perfect choice for special occasions.',
            tags: ['VIP', 'King Bed', 'Security']
        },
        'Presidential Suite': {
            name: 'Presidential Suite',
            price: 45000,
            image: 'https://images.unsplash.com/photo-1590490360182-c33d57733427',
            guests: 6,
            size: '280m²',
            bed: 'King Bed',
            description: 'The pinnacle of luxury. Private terrace, jacuzzi, dedicated butler service, and panoramic views of Oro.',
            tags: ['VIP', 'Jacuzzi', 'Butler']
        },
        'Honeymoon Suite': {
            name: 'Honeymoon Suite',
            price: 18000,
            image: 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304',
            guests: 2,
            size: '120m²',
            bed: 'King Bed',
            description: 'Romantic retreat with ocean views, champagne service, and rose petal arrangements. Perfect for newlyweds.',
            tags: ['Romantic', 'Ocean View', 'Champagne']
        }
    };

    return fallbackRooms[roomName] || null;
}

// ============================================
// PROCESS BOOKING
// ============================================

function processBooking() {
    const formData = collectFormData();

    // Validation
    const fullName = `${formData.first_name} ${formData.last_name}`.trim();
    if (!fullName) {
        showToast('Please enter your name');
        return;
    }
    if (!formData.phone) {
        showToast('Please enter your phone number');
        return;
    }
    if (!validateEmail(formData.email)) {
        showToast('Please enter a valid email');
        return;
    }

    const nights = calculateNights(formData.check_in, formData.check_out);
    if (nights <= 0) {
        showToast('Invalid booking dates');
        return;
    }

    const subtotal = STATE.currentPrice * nights;
    const vat = Math.round(subtotal * 0.075);
    const totalAmount = subtotal + vat;

    formData.total_amount = totalAmount;
    formData.guest_name = fullName;
    formData.room_name = STATE.currentRoom;

    // Button loading state
    const submitBtn = document.querySelector('#bookingModal .btn-submit');
    let originalText = 'Pay & Confirm';
    if (submitBtn) {
        originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitBtn.disabled = true;
    }

    // Check Paystack availability
    if (typeof PaystackPop === 'undefined') {
        showToast('Payment system loading... Please try again');
        if (submitBtn) {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
        return;
    }

    // Initialize Paystack
    const handler = PaystackPop.setup({
        key: DOM.paystackKey,
        email: formData.email,
        amount: totalAmount * 100,
        currency: 'NGN',
        ref: 'DH_' + Date.now(),
        metadata: {
            custom_fields: [
                { display_name: 'Room', variable_name: 'room', value: formData.room_name },
                { display_name: 'Guest', variable_name: 'guest', value: formData.guest_name },
                { display_name: 'Phone', variable_name: 'phone', value: formData.phone }
            ]
        },
        callback: function(response) {
            formData.payment_reference = response.reference;
            formData.payment_status = 'paid';
            saveBookingToDatabase(formData)
                .then(data => {
                    if (data.success) {
                        showToast('Booking Confirmed! Check your email.');
                        closeBookingModal();
                        const form = document.querySelector('#bookingModal form');
                        if (form) form.reset();
                    } else {
                        showToast(data.error || 'Booking save failed');
                    }
                })
                .catch(error => {
                    console.error(error);
                    showToast('Connection error. Please contact support.');
                })
                .finally(() => {
                    if (submitBtn) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }
                });
        },
        onClose: function() {
            showToast('Payment window closed');
            if (submitBtn) {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        }
    });

    handler.openIframe();
}

function collectFormData() {
    const getValue = (id) => {
        const el = document.getElementById(id);
        return el ? el.value.trim() : '';
    };

    return {
        first_name: getValue('bookFname'),
        last_name: getValue('bookLname'),
        email: getValue('bookEmail'),
        phone: getValue('bookPhone'),
        guests: getValue('bookGuests'),
        requests: getValue('bookRequests'),
        check_in: DOM.modalCheckIn?.value || '',
        check_out: DOM.modalCheckOut?.value || ''
    };
}

function saveBookingToDatabase(data) {
    return fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => {
        if (!res.ok) throw new Error('Server Error');
        return res.json();
    });
}
// ============================================
// WHATSAPP BOOKING
// ============================================

function bookViaWhatsApp() {
    if (!STATE.currentRoom) {
        showToast('Please select a room first');
        return;
    }

    const room = STATE.currentRoom;
    const hotel = DOM.hotelName;
    const checkIn = DOM.modalCheckIn?.value || 'Not selected';
    const checkOut = DOM.modalCheckOut?.value || 'Not selected';

    const message = `Hello ${hotel},

I would like to book:

Room: ${room}
Check-in: ${checkIn}
Check-out: ${checkOut}

Please confirm availability.`;

    const encoded = encodeURIComponent(message);
    const phone = String(DOM.whatsapp).replace(/\D/g, '');

    if (!phone) {
        showToast('WhatsApp number unavailable');
        return;
    }

    window.open(`https://wa.me/${phone}?text=${encoded}`, '_blank');
    closeBookingModal();
}

function bookViaWhatsAppFromDetails() {
    const room = STATE.currentRoom || 'Room';
    const hotel = DOM.hotelName;

    const message = `Hello ${hotel},

I want to book the ${room}.

Please confirm availability.`;

    const encoded = encodeURIComponent(message);
    const phone = String(DOM.whatsapp).replace(/\D/g, '');

    if (!phone) {
        showToast('WhatsApp unavailable');
        return;
    }

    window.open(`https://wa.me/${phone}?text=${encoded}`, '_blank');
    closeDetailsModal();
}

// ============================================
// NEWSLETTER
// ============================================

function subscribeNewsletter() {
    const input = document.querySelector('.footer-form input[type="email"]');
    if (!input) {
        showToast('Newsletter field missing');
        return;
    }

    const email = input.value.trim();
    if (!validateEmail(email)) {
        showToast('Please enter a valid email');
        return;
    }

    const submitBtn = document.querySelector('.footer-form button');
    let originalText = '';
    if (submitBtn) {
        originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        submitBtn.disabled = true;
    }

    fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    })
    .then(res => {
        if (!res.ok) throw new Error('Subscription failed');
        return res.json();
    })
    .then(data => {
        if (data.success) {
            showToast('Subscribed successfully!');
            input.value = '';
        } else {
            showToast(data.error || 'Subscription failed');
        }
    })
    .catch(error => {
        console.error(error);
        showToast('Network error. Try again.');
    })
    .finally(() => {
        if (submitBtn) {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
}

// ============================================
// ROOM FILTERING
// ============================================

function filterRooms(category = 'all') {
    if (!DOM.roomCards || DOM.roomCards.length === 0) return;

    let visibleCount = 0;

    DOM.filterBtns?.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === category);
    });

    DOM.roomCards.forEach((card, index) => {
        const cardCategory = card.dataset.category || 'standard';
        const shouldShow = category === 'all' || category === cardCategory;

        if (shouldShow) {
            card.style.display = '';
            requestAnimationFrame(() => {
                setTimeout(() => {
                    card.classList.add('visible');
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 70);
            });
            visibleCount++;
        } else {
            card.classList.remove('visible');
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.display = 'none';
            }, 200);
        }
    });

    if (visibleCount === 0) {
        showToast('No rooms found in this category');
    }
}

// ============================================
// ANIMATION OBSERVERS
// ============================================

let globalObserver = null;

function initAnimations() {
    if (!('IntersectionObserver' in window)) {
        document.querySelectorAll('.stat-item, .room-card, .amenity-card, .review-card, .trust-item')
            .forEach(el => el.classList.add('visible'));
        return;
    }

    if (globalObserver) globalObserver.disconnect();

    const options = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    };

    globalObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const target = entry.target;
            target.classList.add('visible');

            if (target.classList.contains('stat-item')) {
                animateStatNumber(target);
            }

            if (target.classList.contains('review-stats')) {
                animateStatBars();
            }

            observer.unobserve(target);
        });
    }, options);

    const targets = document.querySelectorAll(`
        .stat-item,
        .room-card,
        .amenity-card,
        .review-card,
        .gallery-item,
        .review-stats,
        .trust-item,
        .suite-card,
        .dining-card,
        .event-card
    `);

    targets.forEach(target => globalObserver.observe(target));
}

function animateStatNumber(statItem) {
    const numberEl = statItem.querySelector('.stat-number[data-target]');
    if (!numberEl || numberEl.dataset.animated === 'true') return;

    numberEl.dataset.animated = 'true';

    const target = parseFloat(numberEl.dataset.target);
    const duration = 1500;
    const startTime = performance.now();
    const isDecimal = target % 1 !== 0;

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;

        numberEl.textContent = isDecimal ? current.toFixed(1) : Math.round(current);

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            numberEl.textContent = isDecimal ? target.toFixed(1) : target;
        }
    }

    requestAnimationFrame(update);
}

function animateStatBars() {
    document.querySelectorAll('.stat-bar-fill').forEach(bar => {
        if (bar.dataset.animated === 'true') return;
        bar.dataset.animated = 'true';

        const targetWidth = bar.dataset.width || bar.style.width;
        bar.style.width = '0';

        requestAnimationFrame(() => {
            setTimeout(() => {
                bar.style.width = targetWidth;
            }, 100);
        });
    });
}

// ============================================
// GALLERY SYSTEM
// ============================================

function initGallery() {
    const galleryItems = $$('.gallery-item');
    if (!galleryItems.length) return;

    galleryItems.forEach(item => {
        item.setAttribute('tabindex', '0');
        item.setAttribute('role', 'button');

        const handleOpen = () => {
            const label = item.querySelector('.gallery-label')?.textContent || 'Gallery Image';
            showToast(`Viewing: ${label}`);
        };

        item.addEventListener('click', handleOpen);
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleOpen();
            }
        });
    });
}

// ============================================
// DATE INPUTS
// ============================================

function initDateInputs() {
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];

    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.min = todayStr;
    });

    if (DOM.checkIn && !DOM.checkIn.value) DOM.checkIn.value = todayStr;

    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];

    if (DOM.checkOut && !DOM.checkOut.value) DOM.checkOut.value = tomorrowStr;

    // Modal date change listeners
    DOM.modalCheckIn?.addEventListener('change', updateBookingTotal);
    DOM.modalCheckOut?.addEventListener('change', updateBookingTotal);
}

// ============================================
// KEYBOARD SUPPORT
// ============================================

function initKeyboard() {
    document.addEventListener('keydown', (e) => {
        // ESC closes everything
        if (e.key === 'Escape') {
            closeBookingModal();
            closeDetailsModal();
            closeMobileMenu();
        }

        // ENTER submits booking
        if (e.key === 'Enter' && e.target.closest('#bookingModal')) {
            const tag = e.target.tagName.toLowerCase();
            if (tag !== 'textarea' && tag !== 'button') {
                e.preventDefault();
                processBooking();
            }
        }
    });
}
// ============================================
// DARK MODE
// ============================================

function initDarkMode() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const handleChange = (e) => {
        STATE.prefersDark = e.matches;
        document.body.classList.toggle('dark-mode', e.matches);
    };

    handleChange(mediaQuery);

    if (mediaQuery.addEventListener) {
        mediaQuery.addEventListener('change', handleChange);
    } else {
        mediaQuery.addListener(handleChange);
    }
}

// ============================================
// CONNECTIVITY
// ============================================

function initConnectivity() {
    let lastStatus = navigator.onLine;

    function updateStatus() {
        if (navigator.onLine === lastStatus) return;
        lastStatus = navigator.onLine;

        if (navigator.onLine) {
            showToast('Back online');
        } else {
            showToast('You are offline', 5000);
        }
    }

    window.addEventListener('online', updateStatus);
    window.addEventListener('offline', updateStatus);
}

// ============================================
// ERROR HANDLING
// ============================================

function initErrorHandling() {
    window.addEventListener('error', (e) => {
        console.error('JS Error:', e.message, e.filename, e.lineno);
    });

    window.addEventListener('unhandledrejection', (e) => {
        console.error('Promise Rejection:', e.reason);
    });
}

// ============================================
// QUICK SEARCH
// ============================================

function quickSearch() {
    const rooms = document.getElementById('rooms');
    if (rooms) {
        rooms.scrollIntoView({ behavior: 'smooth' });
        filterRooms('all');
    }
}

// ============================================
// DEBOUNCE / THROTTLE
// ============================================

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============================================
// PRELOAD CRITICAL IMAGES
// ============================================

function preloadResources() {
    const criticalImages = [
        'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1600'
    ];

    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// ============================================
// MAIN INITIALIZATION
// ============================================

let APP_INITIALIZED = false;

function init() {
    if (APP_INITIALIZED) return;
    APP_INITIALIZED = true;

    console.log('🏨 Distance Hotel Initializing...');

    // Cache DOM first
    cacheDOM();

    // Core systems
    initNav();
    initSmoothScroll();
    initAnimations();
    initGallery();
    initKeyboard();
    initDarkMode();
    initDateInputs();
    initConnectivity();
    initErrorHandling();
    initModalBackdropClose();

    // Performance
    preloadResources();

    // Window resize
    const handleResize = debounce(() => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }, 150);

    window.addEventListener('resize', handleResize, { passive: true });

    // Initial filter
    filterRooms('all');

    console.log('✅ Distance Hotel Ready');
}

// ============================================
// BOOT SEQUENCE
// ============================================

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// ============================================
// PUBLIC API
// ============================================

window.DistanceHotel = {
    version: '3.0.0',
    state: STATE,
    dom: DOM,
    scrollToSection,
    filterRooms,
    openBookingModal,
    closeBookingModal,
    processBooking,
    subscribeNewsletter,
    toggleMobileMenu,
    showToast,
    helpers: {
        formatPrice,
        parsePrice,
        calculateNights,
        validateEmail,
        validatePhone
    }
};

console.log(`
🏨 ==================================
   DISTANCE HOTEL SYSTEM READY
==================================

Version: 3.0.0
Status: Production Ready
Backend: Flask Compatible
Payments: Paystack Ready
Animations: Optimized
Mobile: Responsive
==================================
`);
