// Modern JavaScript: Async, Fetch, and Forms - Demonstrates syllabus concepts

class HealthTracker {
    constructor() {
        this.apiBase = '/api';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadRecentMetrics();
    }

    // Modern JavaScript: Event Listeners and DOM Manipulation
    setupEventListeners() {
        // Quick metric buttons
        document.querySelectorAll('.quick-metric-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleQuickMetric(e));
        });

        // Real-time form validation
        const forms = document.querySelectorAll('form[data-validate]');
        forms.forEach(form => {
            form.addEventListener('input', (e) => this.validateField(e.target));
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        });

        // Auto-save functionality
        const autoSaveInputs = document.querySelectorAll('[data-autosave]');
        autoSaveInputs.forEach(input => {
            input.addEventListener('blur', (e) => this.autoSave(e.target));
        });
    }

    // Modern JavaScript: Async/Await and Fetch API
    async loadRecentMetrics() {
        try {
            const response = await fetch(`${this.apiBase}/recent-metrics`);
            if (!response.ok) throw new Error('Failed to load metrics');
            
            const data = await response.json();
            if (data.success) {
                this.populateFormFields(data);
            }
        } catch (error) {
            console.error('Error loading metrics:', error);
            // Don't show error notification on initial load
        }
    }
    
    // Populate form fields with recent data
    populateFormFields(data) {
        const fields = ['heart_rate', 'bp_systolic', 'bp_diastolic', 'temperature', 'weight', 'sleep_hours'];
        fields.forEach(field => {
            const input = document.getElementById(field);
            if (input && data[field]) {
                input.value = data[field];
            }
        });
    }

    // Modern JavaScript: Promise-based API calls
    async saveMetric(metricData) {
        try {
            const response = await fetch(`${this.apiBase}/save-metric`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(metricData)
            });

            const result = await response.json();
            
            if (response.ok && result.success) {
                this.showNotification('Metric saved successfully!', 'success');
                // Reload page to show updated data
                setTimeout(() => window.location.reload(), 1000);
                return result;
            } else {
                throw new Error(result.message || 'Failed to save metric');
            }
        } catch (error) {
            console.error('Error saving metric:', error);
            this.showNotification(error.message, 'error');
            throw error;
        }
    }

    // DOM Manipulation: Dynamic content updates
    updateMetricsDisplay(data) {
        // This function is no longer needed for the current implementation
        // Data is displayed via server-side rendering
    }

    // DOM Manipulation: Creating elements
    createMetricCard(metric) {
        const card = document.createElement('div');
        card.className = 'metric-card fade-in';
        card.innerHTML = `
            <div class="metric-header">
                <i class="fas ${this.getMetricIcon(metric.type)}"></i>
                <h4>${metric.type}</h4>
            </div>
            <div class="metric-value">${metric.value} ${metric.unit}</div>
            <div class="metric-date">${this.formatDate(metric.date)}</div>
            <div class="metric-trend ${metric.trend}">
                <i class="fas fa-arrow-${metric.trend === 'up' ? 'up' : 'down'}"></i>
                ${metric.change}%
            </div>
        `;
        return card;
    }

    // Form Validation: Real-time validation
    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let message = '';

        // Validation rules
        switch (fieldName) {
            case 'heart_rate':
                isValid = value >= 40 && value <= 200;
                message = isValid ? '' : 'Heart rate must be between 40-200 bpm';
                break;
            case 'weight':
                isValid = value >= 30 && value <= 300;
                message = isValid ? '' : 'Weight must be between 30-300 kg';
                break;
            case 'temperature':
                isValid = value >= 95 && value <= 105;
                message = isValid ? '' : 'Temperature must be between 95-105°F';
                break;
            case 'sleep_hours':
                isValid = value >= 0 && value <= 24;
                message = isValid ? '' : 'Sleep hours must be between 0-24';
                break;
        }

        // Update UI
        this.updateFieldValidation(field, isValid, message);
        return isValid;
    }

    // DOM Manipulation: Validation feedback
    updateFieldValidation(field, isValid, message) {
        const container = field.closest('.form-group') || field.parentElement;
        const feedback = container.querySelector('.validation-feedback') || 
                        this.createValidationFeedback(container);

        // Remove existing classes
        field.classList.remove('is-valid', 'is-invalid');
        container.classList.remove('has-error', 'has-success');

        // Add appropriate classes
        if (isValid) {
            field.classList.add('is-valid');
            container.classList.add('has-success');
            feedback.textContent = '';
            feedback.style.display = 'none';
        } else {
            field.classList.add('is-invalid');
            container.classList.add('has-error');
            feedback.textContent = message;
            feedback.style.display = 'block';
        }
    }

    createValidationFeedback(container) {
        const feedback = document.createElement('div');
        feedback.className = 'validation-feedback';
        feedback.style.cssText = 'color: #dc2626; font-size: 0.875rem; margin-top: 0.25rem;';
        container.appendChild(feedback);
        return feedback;
    }

    // Event Handlers
    async handleFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        
        // Validate all fields
        const fields = form.querySelectorAll('input[name]');
        let isFormValid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isFormValid = false;
            }
        });

        if (!isFormValid) {
            this.showNotification('Please fix validation errors', 'error');
            return;
        }

        // Convert FormData to JSON
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        try {
            await this.saveMetric(data);
            form.reset();
            this.closeModal();
        } catch (error) {
            // Error already handled in saveMetric
        }
    }

    async handleQuickMetric(e) {
        const btn = e.target.closest('.quick-metric-btn');
        const metricType = btn.dataset.metric;
        const value = btn.dataset.value;

        const metricData = {
            type: metricType,
            value: value,
            timestamp: new Date().toISOString()
        };

        try {
            await this.saveMetric(metricData);
        } catch (error) {
            // Error already handled
        }
    }

    // Auto-save functionality
    async autoSave(field) {
        if (!field.value.trim()) return;
        
        const data = {
            field: field.name,
            value: field.value,
            timestamp: new Date().toISOString()
        };

        try {
            await fetch(`${this.apiBase}/autosave`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            
            // Show subtle save indicator
            this.showSaveIndicator(field);
        } catch (error) {
            console.error('Auto-save failed:', error);
        }
    }

    // Utility Functions
    getCSRFToken() {
        return document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || '';
    }

    getMetricIcon(type) {
        const icons = {
            'heart_rate': 'fa-heartbeat',
            'weight': 'fa-weight',
            'temperature': 'fa-thermometer-half',
            'sleep': 'fa-bed',
            'blood_pressure': 'fa-tint'
        };
        return icons[type] || 'fa-chart-line';
    }

    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // UI Feedback
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);

        // Close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
    }

    showSaveIndicator(field) {
        const indicator = document.createElement('span');
        indicator.className = 'save-indicator';
        indicator.innerHTML = '<i class="fas fa-check"></i> Saved';
        indicator.style.cssText = 'color: #16a34a; font-size: 0.75rem; margin-left: 0.5rem;';
        
        field.parentElement.appendChild(indicator);
        
        setTimeout(() => {
            indicator.remove();
        }, 2000);
    }

    animateCards() {
        const cards = document.querySelectorAll('.metric-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('animate-in');
            }, index * 100);
        });
    }

    closeModal() {
        const modal = document.getElementById('addMetricsModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HealthTracker();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HealthTracker;
}