// Appointment Booking JavaScript

let bookingData = {
    doctorId: null,
    doctorName: null,
    specialization: null,
    date: null,
    time: null,
    consultationType: null,
    fee: 500
};

let currentStep = 1;

// Doctor Selection
function selectDoctor(doctorId, doctorName, specialization) {
    bookingData.doctorId = doctorId;
    bookingData.doctorName = doctorName;
    bookingData.specialization = specialization;
    
    // Highlight selected doctor
    document.querySelectorAll('.doctor-card').forEach(card => {
        card.style.borderColor = 'transparent';
    });
    event.target.closest('.doctor-card').style.borderColor = '#2E8B57';
    
    // Move to next step
    setTimeout(() => nextStep(), 500);
}

// Doctor Search
document.getElementById('doctor-search')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const doctorCards = document.querySelectorAll('.doctor-card');
    
    doctorCards.forEach(card => {
        const doctorName = card.querySelector('h3').textContent.toLowerCase();
        const specialization = card.querySelector('.specialization').textContent.toLowerCase();
        const hospital = card.querySelector('.detail-item span').textContent.toLowerCase();
        
        if (doctorName.includes(searchTerm) || specialization.includes(searchTerm) || hospital.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

// Filter by Specialization
document.querySelectorAll('.filter-chip').forEach(chip => {
    chip.addEventListener('click', function() {
        // Remove active class from all chips
        document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        
        const filter = this.dataset.filter;
        const doctorCards = document.querySelectorAll('.doctor-card');
        
        doctorCards.forEach(card => {
            if (filter === 'all' || card.dataset.specialization.includes(filter)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

// Date Selection
document.querySelectorAll('.date-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.date-card').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        bookingData.date = this.dataset.date;
    });
});

// Time Slot Selection
document.querySelectorAll('.time-slot:not(.disabled)').forEach(slot => {
    slot.addEventListener('click', function() {
        document.querySelectorAll('.time-slot').forEach(s => s.classList.remove('selected'));
        this.classList.add('selected');
        bookingData.time = this.dataset.time;
    });
});

// Consultation Type Selection
function selectConsultation(type) {
    bookingData.consultationType = type;
    
    // Update fee based on type
    const fees = {
        'video': 500,
        'clinic': 700,
        'home': 1500
    };
    bookingData.fee = fees[type];
    
    // Highlight selected consultation
    document.querySelectorAll('.consultation-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.target.closest('.consultation-card').classList.add('selected');
    
    // Move to next step
    setTimeout(() => nextStep(), 500);
}

// Navigation Functions
function nextStep() {
    // Validation
    if (currentStep === 1 && !bookingData.doctorId) {
        alert('Please select a doctor');
        return;
    }
    
    if (currentStep === 2 && (!bookingData.date || !bookingData.time)) {
        alert('Please select date and time');
        return;
    }
    
    if (currentStep === 3 && !bookingData.consultationType) {
        alert('Please select consultation type');
        return;
    }
    
    // Hide current step
    document.getElementById(`step-${currentStep}`).classList.remove('active');
    document.querySelector(`.progress-step[data-step="${currentStep}"]`).classList.add('completed');
    
    // Show next step
    currentStep++;
    document.getElementById(`step-${currentStep}`).classList.add('active');
    document.querySelector(`.progress-step[data-step="${currentStep}"]`).classList.add('active');
    
    // Update confirmation if on step 4
    if (currentStep === 4) {
        updateConfirmation();
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function previousStep() {
    // Hide current step
    document.getElementById(`step-${currentStep}`).classList.remove('active');
    document.querySelector(`.progress-step[data-step="${currentStep}"]`).classList.remove('active');
    
    // Show previous step
    currentStep--;
    document.getElementById(`step-${currentStep}`).classList.add('active');
    document.querySelector(`.progress-step[data-step="${currentStep}"]`).classList.remove('completed');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Update Confirmation Summary
function updateConfirmation() {
    document.getElementById('confirm-doctor').textContent = bookingData.doctorName;
    document.getElementById('confirm-specialization').textContent = bookingData.specialization;
    document.getElementById('confirm-date').textContent = formatDate(bookingData.date);
    document.getElementById('confirm-time').textContent = bookingData.time;
    document.getElementById('confirm-type').textContent = formatConsultationType(bookingData.consultationType);
    document.getElementById('confirm-fee').textContent = `₹${bookingData.fee}`;
    
    const total = bookingData.fee + 50; // Adding platform fee
    document.getElementById('confirm-total').textContent = `₹${total}`;
    
    // Update hidden form fields
    document.getElementById('form-doctor-id').value = bookingData.doctorId;
    document.getElementById('form-date').value = bookingData.date;
    document.getElementById('form-time').value = bookingData.time;
    document.getElementById('form-type').value = bookingData.consultationType;
}

// Helper Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

function formatConsultationType(type) {
    const types = {
        'video': 'Video Consultation',
        'clinic': 'Clinic Visit',
        'home': 'Home Visit'
    };
    return types[type] || type;
}

// Confirm Booking
function confirmBooking() {
    const terms = document.getElementById('terms');
    if (!terms.checked) {
        alert('Please accept the terms and conditions');
        return;
    }
    
    // Submit the form
    document.getElementById('booking-form').submit();
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('Booking system initialized');
});