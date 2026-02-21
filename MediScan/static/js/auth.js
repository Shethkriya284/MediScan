// Toggle Password Visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling;

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Show/Hide Forms
function showLogin() {
    hideAllForms();
    document.getElementById('loginForm').classList.remove('hidden');
}

function showSignup() {
    hideAllForms();
    document.getElementById('signupForm').classList.remove('hidden');
}

function showOTPLogin() {
    hideAllForms();
    document.getElementById('otpLoginForm').classList.remove('hidden');
}

function showOTPVerify(email) {
    hideAllForms();
    document.getElementById('otpVerifyForm').classList.remove('hidden');
    document.getElementById('otpEmailDisplay').textContent = email;
    document.getElementById('verifyEmail').value = email;
    startCountdown();
}

function hideAllForms() {
    const forms = document.querySelectorAll('.form-wrapper');
    forms.forEach(form => form.classList.add('hidden'));
}

// Check if we need to show OTP verify on page load (after signup)
document.addEventListener('DOMContentLoaded', function () {
    if (window.showOTPVerifyOnLoad && window.pendingVerificationEmail) {
        showOTPVerify(window.pendingVerificationEmail);
    }

    // Add scroll indicator if content is scrollable
    checkScrollable();

    // OTP Input Handling
    const otpInputs = document.querySelectorAll('.otp-input');

    otpInputs.forEach((input, index) => {
        input.addEventListener('input', function (e) {
            const value = e.target.value;

            // Only allow numbers
            if (!/^\d*$/.test(value)) {
                e.target.value = '';
                return;
            }

            // Move to next input
            if (value && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }

            // Update hidden OTP value
            updateOTPValue();
        });

        input.addEventListener('keydown', function (e) {
            // Move to previous input on backspace
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });

        // Handle paste
        input.addEventListener('paste', function (e) {
            e.preventDefault();
            const pastedData = e.clipboardData.getData('text');
            const digits = pastedData.replace(/\D/g, '').split('');

            digits.forEach((digit, i) => {
                if (index + i < otpInputs.length) {
                    otpInputs[index + i].value = digit;
                }
            });

            updateOTPValue();

            // Focus last filled input
            const lastIndex = Math.min(index + digits.length - 1, otpInputs.length - 1);
            otpInputs[lastIndex].focus();
        });
    });
});

function updateOTPValue() {
    const otpInputs = document.querySelectorAll('.otp-input');
    const otp = Array.from(otpInputs).map(input => input.value).join('');
    document.getElementById('otpValue').value = otp;
}

// Request OTP
document.getElementById('requestOTPForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = document.getElementById('otpEmail').value;
    const button = this.querySelector('button');
    const originalText = button.innerHTML;

    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    try {
        const response = await fetch('/api/send-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        });

        const data = await response.json();

        if (data.success) {
            showNotification('OTP sent successfully! Check your email.', 'success');
            showOTPVerify(email);
        } else {
            // Check if user needs to sign up
            if (data.action === 'signup_required') {
                showNotification(data.message + ' Redirecting to signup...', 'error');
                setTimeout(() => {
                    showSignup();
                    // Pre-fill email in signup form
                    document.getElementById('signupEmail').value = email;
                    document.getElementById('signupEmail').focus();
                }, 2000);
            } else {
                showNotification(data.message || 'Failed to send OTP', 'error');
            }
        }
    } catch (error) {
        showNotification('Network error. Please try again.', 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
});

// Verify OTP
document.getElementById('verifyOTPForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = document.getElementById('verifyEmail').value;
    const otp = document.getElementById('otpValue').value;

    if (otp.length !== 6) {
        showNotification('Please enter complete 6-digit OTP', 'error');
        return;
    }

    const button = this.querySelector('button');
    const originalText = button.innerHTML;

    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

    try {
        const response = await fetch('/api/verify-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email, otp: otp })
        });

        const data = await response.json();

        if (data.success) {
            showNotification('Login successful!', 'success');
            setTimeout(() => {
                window.location.href = data.redirect || '/dashboard';
            }, 1000);
        } else {
            showNotification(data.message || 'Invalid OTP', 'error');
            // Clear OTP inputs
            document.querySelectorAll('.otp-input').forEach(input => input.value = '');
            document.querySelectorAll('.otp-input')[0].focus();
        }
    } catch (error) {
        showNotification('Network error. Please try again.', 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
});

// Countdown Timer
let countdownInterval;

function startCountdown() {
    let seconds = 60;
    const countdownElement = document.getElementById('countdown');
    const timerElement = document.querySelector('.timer');

    clearInterval(countdownInterval);

    countdownInterval = setInterval(() => {
        seconds--;
        countdownElement.textContent = seconds;

        if (seconds <= 0) {
            clearInterval(countdownInterval);
            timerElement.style.display = 'none';
        }
    }, 1000);
}

// Resend OTP
async function resendOTP() {
    const email = document.getElementById('verifyEmail').value;

    showNotification('Resending OTP...', 'info');

    try {
        const response = await fetch('/api/send-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        });

        const data = await response.json();

        if (data.success) {
            showNotification('OTP resent successfully!', 'success');
            startCountdown();
            document.querySelector('.timer').style.display = 'block';
            // Clear previous OTP inputs
            document.querySelectorAll('.otp-input').forEach(input => input.value = '');
            document.querySelectorAll('.otp-input')[0].focus();
        } else {
            showNotification(data.message || 'Failed to resend OTP', 'error');
        }
    } catch (error) {
        showNotification('Network error. Please try again.', 'error');
    }
}

// Show Notification
function showNotification(message, type) {
    // Remove existing notifications
    const existing = document.querySelector('.alert');
    if (existing) {
        existing.remove();
    }

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
    `;

    const container = document.querySelector('.forms-container');
    container.insertBefore(alert, container.firstChild);

    // Auto remove after 5 seconds
    setTimeout(() => {
        alert.style.animation = 'slideUp 0.3s ease-out reverse';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// Password Strength Indicator
document.getElementById('signupPassword')?.addEventListener('input', function (e) {
    const password = e.target.value;
    // Add password strength indicator logic here if needed
});

// Form Validation
document.getElementById('signupFormElement')?.addEventListener('submit', function (e) {
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        e.preventDefault();
        showNotification('Passwords do not match!', 'error');
        return false;
    }

    if (password.length < 6) {
        e.preventDefault();
        showNotification('Password must be at least 6 characters long!', 'error');
        return false;
    }
});

// Check if container is scrollable and show indicator
function checkScrollable() {
    const container = document.querySelector('.auth-container');
    if (!container) return;

    const isScrollable = container.scrollHeight > container.clientHeight;

    if (isScrollable) {
        showScrollIndicator();

        // Hide indicator when user scrolls
        container.addEventListener('scroll', function () {
            const scrollIndicator = document.querySelector('.scroll-indicator');
            if (scrollIndicator) {
                const isAtBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 50;
                if (isAtBottom) {
                    scrollIndicator.style.display = 'none';
                }
            }
        });
    }
}

function showScrollIndicator() {
    // Remove existing indicator
    const existing = document.querySelector('.scroll-indicator');
    if (existing) existing.remove();

    const indicator = document.createElement('div');
    indicator.className = 'scroll-indicator';
    indicator.innerHTML = '<i class="fas fa-chevron-down"></i> Scroll down';
    document.body.appendChild(indicator);

    // Auto hide after 3 seconds
    setTimeout(() => {
        if (indicator.parentElement) {
            indicator.style.opacity = '0';
            indicator.style.transition = 'opacity 0.5s';
            setTimeout(() => indicator.remove(), 500);
        }
    }, 3000);
}

// Re-check scrollable when form changes
function showSignup() {
    hideAllForms();
    document.getElementById('signupForm').classList.remove('hidden');
    setTimeout(checkScrollable, 100);
}

function showLogin() {
    hideAllForms();
    document.getElementById('loginForm').classList.remove('hidden');
    setTimeout(checkScrollable, 100);
}

// Clear error messages on input
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input');

    inputs.forEach(input => {
        input.addEventListener('input', function () {
            // Remove flash messages
            const flashMessages = document.querySelector('.flash-messages');
            if (flashMessages) {
                flashMessages.innerHTML = '';
            }

            // Also remove any specific alerts injected by JS
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => alert.remove());
        });
    });
});
