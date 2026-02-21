// Medicine Tracker JavaScript functionality
document.addEventListener('DOMContentLoaded', function () {
    console.log('Medicine Tracker loaded');

    // Modal functionality
    const addMedicineModal = document.getElementById('addMedicineModal');
    const addMedicineBtn = document.getElementById('addMedicineBtn');
    const cancelBtn = document.getElementById('cancelModalBtn');

    // Show modal function
    function showAddMedicineModal() {
        if (addMedicineModal) {
            addMedicineModal.style.display = 'flex';
            // Focus on the first input field
            const firstInput = document.getElementById('medicineName');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }

    // Hide modal function
    function hideAddMedicineModal() {
        if (addMedicineModal) {
            addMedicineModal.style.display = 'none';
            // Reset form when hiding
            const form = document.getElementById('addMedicineForm');
            if (form) {
                form.reset();
            }
            // Hide timing options
            const timingOptions = document.getElementById('timingOptions');
            if (timingOptions) {
                timingOptions.style.display = 'none';
                timingOptions.innerHTML = '';
            }
        }
    }

    // Add event listeners for modal
    if (addMedicineBtn) {
        addMedicineBtn.addEventListener('click', showAddMedicineModal);
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', hideAddMedicineModal);
    }

    // Test button for adding reminders
    const testReminderBtn = document.getElementById('testReminderBtn');
    if (testReminderBtn) {
        testReminderBtn.addEventListener('click', function () {
            // Test adding a reminder
            const testTimings = [
                { value: 'after_breakfast', label: 'After Breakfast' },
                { value: 'after_dinner', label: 'After Dinner' }
            ];

            addToTodaysReminders('Test Medicine 500mg', '1 tablet with water', testTimings);
            showNotification('Test reminders added successfully!', 'success');
        });
    }

    // Handle keyboard shortcuts for modal
    document.addEventListener('keydown', function (e) {
        if (addMedicineModal && addMedicineModal.style.display === 'flex') {
            if (e.key === 'Escape') {
                hideAddMedicineModal();
            }
        }
    });

    // Close modal when clicking outside
    if (addMedicineModal) {
        addMedicineModal.addEventListener('click', function (e) {
            if (e.target === addMedicineModal) {
                hideAddMedicineModal();
            }
        });
    }

    // Mark as taken functionality
    const markTakenButtons = document.querySelectorAll('.mark-taken-btn');
    markTakenButtons.forEach(button => {
        button.addEventListener('click', function () {
            const medicineName = this.getAttribute('data-medicine');
            // Add visual feedback
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Taken!';
            this.classList.add('btn-success');
            this.classList.remove('btn-primary');
            this.disabled = true;

            // Show success message
            showNotification(`${medicineName} marked as taken!`, 'success');

            // Reset after 3 seconds
            setTimeout(() => {
                this.innerHTML = originalText;
                this.classList.remove('btn-success');
                this.classList.add('btn-primary');
                this.disabled = false;
            }, 3000);
        });
    });

    // Done button functionality (for reminders)
    const doneButtons = document.querySelectorAll('.done-btn');
    doneButtons.forEach(button => {
        button.addEventListener('click', function () {
            const reminderName = this.getAttribute('data-reminder');
            const reminderCard = this.closest('[style*="border-left"]');

            if (!reminderCard) return;

            // Show success message
            showNotification(`${reminderName} completed!`, 'success');

            // Add completion animation
            reminderCard.style.transition = 'all 0.5s ease';
            reminderCard.style.transform = 'translateX(100%)';
            reminderCard.style.opacity = '0';

            // Remove the reminder after animation
            setTimeout(() => {
                reminderCard.remove();

                // Check if there are any reminders left in the reminders section
                const reminderSection = reminderCard.closest('[style*="background: white"][style*="margin-top: 2rem"]');
                if (reminderSection) {
                    const remainingReminders = reminderSection.querySelectorAll('[style*="border-left: 3px solid"]');

                    if (remainingReminders.length === 0) {
                        // Show "No reminders" message
                        showNoRemindersMessage(reminderSection);
                    }
                }
            }, 500);
        });
    });

    // Function to show "No reminders" message
    function showNoRemindersMessage(reminderSection) {
        const reminderList = reminderSection.querySelector('[style*="flex-direction: column"]');

        if (reminderList) {
            reminderList.innerHTML = `
                <div class="no-reminders-message" style="text-align: center; padding: 3rem 1rem; color: #6b7280;">
                    <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <h4 style="margin: 0 0 0.5rem 0; color: #10b981; font-weight: 600;">
                        All Done! 🎉
                    </h4>
                    <p style="margin: 0; font-size: 0.9rem;">
                        You've completed all your medicine reminders for today.
                    </p>
                    <div style="margin-top: 1.5rem;">
                        <button class="btn btn-outline-primary btn-sm" onclick="location.reload()">
                            <i class="fas fa-refresh"></i> Refresh Reminders
                        </button>
                    </div>
                </div>
            `;
        }
    }

    // Edit button functionality
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const medicineName = this.getAttribute('data-medicine');
            showNotification(`Edit functionality for ${medicineName} coming soon!`, 'info');
        });
    });

    // Reorder button functionality
    const reorderButtons = document.querySelectorAll('.reorder-btn');
    reorderButtons.forEach(button => {
        button.addEventListener('click', function () {
            const medicineName = this.getAttribute('data-medicine');
            showReorderModal(medicineName, this);
        });
    });

    // Reorder modal functionality
    function showReorderModal(medicineName, buttonElement) {
        // Create reorder modal
        const reorderModal = document.createElement('div');
        reorderModal.id = 'reorderModal';
        reorderModal.style.cssText = `
            display: flex;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
            align-items: center;
            justify-content: center;
        `;

        reorderModal.innerHTML = `
            <div style="background: white; border-radius: 12px; padding: 2rem; max-width: 400px; width: 90%;">
                <h3 style="margin-bottom: 1.5rem; color: #1a1a2e;">
                    <i class="fas fa-shopping-cart"></i> Reorder ${medicineName}
                </h3>
                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">
                        How many days of stock do you want to order?
                    </label>
                    <input type="number" id="stockDays" class="form-control" placeholder="Enter days (e.g., 30)" min="1" max="365" style="font-size: 1.1rem; padding: 0.75rem;">
                    <small style="color: #6b7280; margin-top: 0.5rem; display: block;">
                        This will calculate the required quantity based on your dosage
                    </small>
                </div>
                <div style="display: flex; gap: 1rem;">
                    <button type="button" id="confirmReorder" class="btn btn-primary" style="flex: 1;">
                        <i class="fas fa-check"></i> Confirm Order
                    </button>
                    <button type="button" id="cancelReorder" class="btn btn-outline-secondary" style="flex: 1;">
                        Cancel
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(reorderModal);

        // Focus on input
        const stockInput = document.getElementById('stockDays');
        stockInput.focus();

        // Handle confirm order
        document.getElementById('confirmReorder').addEventListener('click', function () {
            const days = parseInt(stockInput.value);

            if (!days || days < 1) {
                showNotification('Please enter a valid number of days', 'error');
                return;
            }

            if (days > 365) {
                showNotification('Maximum 365 days allowed', 'error');
                return;
            }

            // Process the reorder
            processReorder(medicineName, days, buttonElement);

            // Remove modal
            reorderModal.remove();
        });

        // Handle cancel
        document.getElementById('cancelReorder').addEventListener('click', function () {
            reorderModal.remove();
        });

        // Handle Enter key
        stockInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                document.getElementById('confirmReorder').click();
            }
        });

        // Handle Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                reorderModal.remove();
            }
        });

        // Close modal when clicking outside
        reorderModal.addEventListener('click', function (e) {
            if (e.target === reorderModal) {
                reorderModal.remove();
            }
        });
    }

    function processReorder(medicineName, days, buttonElement) {
        // Calculate estimated quantity (this would normally come from server)
        const estimatedQuantity = calculateQuantity(medicineName, days);

        // Show success notification
        showNotification(`Order confirmed! ${estimatedQuantity} units of ${medicineName} for ${days} days`, 'success');

        // Update the medicine card to show restocked status
        updateMedicineStock(medicineName, buttonElement, days);
    }

    function calculateQuantity(medicineName, days) {
        // Simple calculation based on typical dosages
        const dosageMap = {
            'Vitamin D3': 1, // 1 per day
            'Paracetamol': 3, // 3 per day
            'Amoxicillin': 2 // 2 per day
        };

        const dailyDosage = dosageMap[medicineName] || 1;
        return dailyDosage * days;
    }

    function updateMedicineStock(medicineName, buttonElement, days) {
        // Find the medicine card
        const medicineCard = buttonElement.closest('[style*="border-left"]');
        if (!medicineCard) return;

        // Update stock information - find the paragraph containing "Stock:"
        const stockInfo = Array.from(medicineCard.querySelectorAll('p')).find(p =>
            p.textContent.includes('Stock:')
        );
        if (stockInfo) {
            const newStock = calculateQuantity(medicineName, days);
            stockInfo.innerHTML = `<strong>Stock:</strong> ${newStock} units remaining ✅`;
            stockInfo.style.color = '#10b981'; // Green color
        }

        // Update status badge
        const statusBadge = medicineCard.querySelector('span[style*="background"]');
        if (statusBadge) {
            statusBadge.style.background = '#d1fae5';
            statusBadge.style.color = '#065f46';
            statusBadge.textContent = 'Well Stocked';
        }

        // Replace reorder button with a regular edit button
        const originalText = buttonElement.innerHTML;
        buttonElement.innerHTML = '<i class="fas fa-edit"></i> Edit';
        buttonElement.classList.remove('btn-warning', 'reorder-btn');
        buttonElement.classList.add('btn-outline-primary', 'edit-btn');

        // Remove the reorder functionality and add edit functionality
        const newButton = buttonElement.cloneNode(true);
        buttonElement.parentNode.replaceChild(newButton, buttonElement);

        // Add edit functionality to the new button
        newButton.addEventListener('click', function () {
            const medicineName = this.getAttribute('data-medicine');
            showNotification(`Edit functionality for ${medicineName} coming soon!`, 'info');
        });

        // Show temporary success state
        newButton.style.background = '#10b981';
        newButton.style.color = 'white';
        newButton.innerHTML = '<i class="fas fa-check"></i> Restocked!';

        setTimeout(() => {
            newButton.style.background = '';
            newButton.style.color = '';
            newButton.innerHTML = '<i class="fas fa-edit"></i> Edit';
        }, 3000);
    }

    // Add medicine form submission
    const addMedicineForm = document.getElementById('addMedicineForm');
    if (addMedicineForm) {
        // Handle frequency change to show timing options
        const frequencySelect = document.getElementById('medicineFrequency');
        const timingOptions = document.getElementById('timingOptions');

        if (frequencySelect && timingOptions) {
            frequencySelect.addEventListener('change', function () {
                const frequency = parseInt(this.value);
                if (frequency > 0) {
                    showTimingOptions(frequency);
                } else {
                    timingOptions.style.display = 'none';
                }
            });
        }

        addMedicineForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Get form values
            const medicineName = document.getElementById('medicineName').value.trim();
            const dosage = document.getElementById('medicineDosage').value.trim();
            const duration = document.getElementById('medicineDuration').value;
            const frequency = document.getElementById('medicineFrequency').value;

            // Get selected timings
            const selectedTimings = getSelectedTimings();

            // Validate inputs
            if (!medicineName || !dosage || !duration || !frequency) {
                showNotification('Please fill in all fields', 'error');
                return;
            }

            if (selectedTimings.length !== parseInt(frequency)) {
                showNotification(`Please select exactly ${frequency} timing(s)`, 'error');
                return;
            }

            if (duration < 1 || duration > 365) {
                showNotification('Duration must be between 1 and 365 days', 'error');
                return;
            }

            // Create new medicine card
            addNewMedicineCard(medicineName, dosage, duration, frequency);

            // Add to today's reminders
            addToTodaysReminders(medicineName, dosage, selectedTimings);

            // Show success message
            showNotification(`Medicine "${medicineName}" added successfully with ${selectedTimings.length} daily reminder(s)!`, 'success');

            // Hide modal and reset form
            hideAddMedicineModal();
            addMedicineForm.reset();
            timingOptions.style.display = 'none';
        });
    }

    // Function to show timing options based on frequency
    function showTimingOptions(frequency) {
        const timingOptions = document.getElementById('timingOptions');
        if (!timingOptions) return;

        const timingChoices = [
            { value: 'before_breakfast', label: 'Before Breakfast', icon: 'fa-sun' },
            { value: 'after_breakfast', label: 'After Breakfast', icon: 'fa-coffee' },
            { value: 'before_lunch', label: 'Before Lunch', icon: 'fa-sun' },
            { value: 'after_lunch', label: 'After Lunch', icon: 'fa-utensils' },
            { value: 'before_dinner', label: 'Before Dinner', icon: 'fa-moon' },
            { value: 'after_dinner', label: 'After Dinner', icon: 'fa-moon' },
            { value: 'bedtime', label: 'At Bedtime', icon: 'fa-bed' },
            { value: 'morning', label: 'Morning', icon: 'fa-sun' }
        ];

        let html = `<p style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.75rem; font-weight: 500;">Select ${frequency} timing(s) for taking this medicine:</p>`;
        html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.5rem;">';

        timingChoices.forEach(timing => {
            html += `
                <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer; padding: 0.5rem; border-radius: 6px; transition: all 0.2s; border: 1px solid #e5e7eb; background: white;" 
                       class="timing-option"
                       onmouseover="this.style.backgroundColor='#f3f4f6'; this.style.borderColor='#d1d5db'" 
                       onmouseout="this.style.backgroundColor='white'; this.style.borderColor='#e5e7eb'">
                    <input type="checkbox" name="timing" value="${timing.value}" style="margin: 0; accent-color: #3b82f6;">
                    <i class="fas ${timing.icon}" style="color: #6b7280; width: 14px; font-size: 0.85rem;"></i>
                    <span style="font-size: 0.85rem; font-weight: 500;">${timing.label}</span>
                </label>
            `;
        });

        html += '</div>';
        timingOptions.innerHTML = html;
        timingOptions.style.display = 'block';

        // Add event listeners to limit selection and provide visual feedback
        const checkboxes = timingOptions.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function () {
                const checkedBoxes = timingOptions.querySelectorAll('input[type="checkbox"]:checked');
                const label = this.closest('.timing-option');

                if (this.checked) {
                    if (checkedBoxes.length > frequency) {
                        this.checked = false;
                        showNotification(`You can only select ${frequency} timing(s)`, 'warning');
                        return;
                    }
                    // Highlight selected option
                    label.style.backgroundColor = '#dbeafe';
                    label.style.borderColor = '#3b82f6';
                    label.style.color = '#1e40af';
                } else {
                    // Remove highlight
                    label.style.backgroundColor = 'white';
                    label.style.borderColor = '#e5e7eb';
                    label.style.color = '';
                }

                // Update selection counter
                updateSelectionCounter(checkedBoxes.length, frequency);
            });
        });

        // Add selection counter
        const counterDiv = document.createElement('div');
        counterDiv.id = 'selectionCounter';
        counterDiv.style.cssText = 'margin-top: 0.75rem; padding: 0.5rem; background: #f0f9ff; border-radius: 6px; text-align: center; font-size: 0.85rem; color: #0369a1;';
        counterDiv.innerHTML = `<i class="fas fa-info-circle"></i> Select ${frequency} timing(s) - 0 selected`;
        timingOptions.appendChild(counterDiv);
    }

    // Function to update selection counter
    function updateSelectionCounter(selected, required) {
        const counter = document.getElementById('selectionCounter');
        if (!counter) return;

        const isComplete = selected === required;
        const color = isComplete ? '#065f46' : '#0369a1';
        const bgColor = isComplete ? '#d1fae5' : '#f0f9ff';
        const icon = isComplete ? 'fa-check-circle' : 'fa-info-circle';

        counter.style.color = color;
        counter.style.backgroundColor = bgColor;
        counter.innerHTML = `<i class="fas ${icon}"></i> Select ${required} timing(s) - ${selected} selected ${isComplete ? '✓' : ''}`;
    }

    // Function to get selected timings
    function getSelectedTimings() {
        const timingOptions = document.getElementById('timingOptions');
        if (!timingOptions) return [];

        const checkedBoxes = timingOptions.querySelectorAll('input[type="checkbox"]:checked');
        return Array.from(checkedBoxes).map(checkbox => ({
            value: checkbox.value,
            label: checkbox.parentElement.querySelector('span').textContent
        }));
    }

    // Function to add medicine to today's reminders
    function addToTodaysReminders(medicineName, dosage, timings) {
        // Find the Today's Reminders section more reliably
        const reminderSection = Array.from(document.querySelectorAll('h3')).find(h3 =>
            h3.textContent.includes("Today's Reminders")
        )?.closest('[style*="background: white"]');

        if (!reminderSection) {
            console.log('Reminder section not found');
            return;
        }

        const reminderList = reminderSection.querySelector('[style*="flex-direction: column"]');
        if (!reminderList) {
            console.log('Reminder list not found');
            return;
        }

        // Check if there's a "no reminders" message and remove it
        const noRemindersMsg = reminderList.querySelector('.no-reminders-message');
        if (noRemindersMsg) {
            noRemindersMsg.remove();
        }

        console.log(`Adding ${timings.length} reminders for ${medicineName}`);

        // Add each timing as a separate reminder
        timings.forEach((timing, index) => {
            const reminderCard = createReminderCard(medicineName, dosage, timing);
            reminderList.appendChild(reminderCard);

            // Add slight delay for staggered animation
            setTimeout(() => {
                reminderCard.style.opacity = '1';
                reminderCard.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Show success notification for reminders
        showNotification(`${timings.length} reminder(s) added to Today's Reminders!`, 'info');
    }

    // Function to create a reminder card
    function createReminderCard(medicineName, dosage, timing) {
        const colors = {
            'before_breakfast': { bg: '#fef3c7', border: '#f59e0b', icon: '#92400e' },
            'after_breakfast': { bg: '#f0fdf4', border: '#10b981', icon: '#065f46' },
            'before_lunch': { bg: '#dbeafe', border: '#3b82f6', icon: '#1e40af' },
            'after_lunch': { bg: '#eff6ff', border: '#3b82f6', icon: '#1e40af' },
            'before_dinner': { bg: '#fce7f3', border: '#ec4899', icon: '#be185d' },
            'after_dinner': { bg: '#f3e8ff', border: '#8b5cf6', icon: '#6d28d9' },
            'bedtime': { bg: '#f1f5f9', border: '#64748b', icon: '#475569' },
            'morning': { bg: '#fef3c7', border: '#f59e0b', icon: '#92400e' }
        };

        const colorScheme = colors[timing.value] || colors['morning'];

        const reminderCard = document.createElement('div');
        reminderCard.style.cssText = `
            display: flex; 
            align-items: center; 
            gap: 1rem; 
            padding: 1rem; 
            background: ${colorScheme.bg}; 
            border-radius: 8px; 
            border-left: 3px solid ${colorScheme.border};
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        `;

        reminderCard.innerHTML = `
            <div style="width: 50px; height: 50px; background: ${colorScheme.border}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;">
                <i class="fas fa-pills"></i>
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0; font-weight: 600;">${medicineName} - ${timing.label}</h4>
                <p style="margin: 0.25rem 0 0 0; color: #6b7280; font-size: 0.9rem;">${dosage}</p>
            </div>
            <button class="btn btn-sm btn-primary done-btn" data-reminder="${medicineName} ${timing.label}">
                <i class="fas fa-check"></i> Done
            </button>
        `;

        // Add event listener to the done button
        const doneBtn = reminderCard.querySelector('.done-btn');
        if (doneBtn) {
            doneBtn.addEventListener('click', function () {
                const reminderName = this.getAttribute('data-reminder');

                // Show success message
                showNotification(`${reminderName} completed!`, 'success');

                // Add completion animation
                reminderCard.style.transition = 'all 0.5s ease';
                reminderCard.style.transform = 'translateX(100%)';
                reminderCard.style.opacity = '0';

                // Remove the reminder after animation
                setTimeout(() => {
                    reminderCard.remove();

                    // Check if there are any reminders left
                    const remainingReminders = reminderList.querySelectorAll('[style*="border-left: 3px solid"]');
                    if (remainingReminders.length === 0) {
                        showNoRemindersMessage(reminderSection);
                    }
                }, 500);
            });
        }

        return reminderCard;
    }

    // Function to add new medicine card to the grid
    function addNewMedicineCard(name, dosage, duration, frequency) {
        const medicineGrid = document.querySelector('[style*="grid-template-columns"]');
        if (!medicineGrid) return;

        // Calculate total stock needed
        const totalStock = parseInt(duration) * parseInt(frequency);

        // Generate random color for the border
        const colors = ['#2E8B57', '#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444'];
        const randomColor = colors[Math.floor(Math.random() * colors.length)];

        // Create new medicine card
        const newCard = document.createElement('div');
        newCard.style.cssText = `
            background: white; 
            border-radius: 12px; 
            padding: 1.5rem; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            border-left: 4px solid ${randomColor};
            animation: fadeInUp 0.5s ease-out;
        `;

        newCard.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <h3 style="margin: 0; font-weight: 600; color: #1a1a2e;">${name}</h3>
                    <p style="margin: 0.25rem 0; color: #6b7280; font-size: 0.9rem;">Custom Medicine</p>
                </div>
                <span style="background: #d1fae5; color: #065f46; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">Active</span>
            </div>
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <p style="margin: 0; font-size: 0.9rem;"><strong>Dosage:</strong> ${dosage}</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;"><strong>Duration:</strong> ${duration} days</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;"><strong>Stock:</strong> ${totalStock} units remaining</p>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-sm btn-primary mark-taken-btn" data-medicine="${name}" style="flex: 1;">
                    <i class="fas fa-check"></i> Mark Taken
                </button>
                <button class="btn btn-sm btn-outline-primary edit-btn" data-medicine="${name}" style="flex: 1;">
                    <i class="fas fa-edit"></i> Edit
                </button>
            </div>
        `;

        // Add the new card to the grid
        medicineGrid.appendChild(newCard);

        // Add event listeners to the new buttons
        const markTakenBtn = newCard.querySelector('.mark-taken-btn');
        const editBtn = newCard.querySelector('.edit-btn');

        if (markTakenBtn) {
            markTakenBtn.addEventListener('click', function () {
                const medicineName = this.getAttribute('data-medicine');
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Taken!';
                this.classList.add('btn-success');
                this.classList.remove('btn-primary');
                this.disabled = true;

                showNotification(`${medicineName} marked as taken!`, 'success');

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('btn-success');
                    this.classList.add('btn-primary');
                    this.disabled = false;
                }, 3000);
            });
        }

        if (editBtn) {
            editBtn.addEventListener('click', function () {
                const medicineName = this.getAttribute('data-medicine');
                showNotification(`Edit functionality for ${medicineName} coming soon!`, 'info');
            });
        }
    }

    // Function to show notifications
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            animation: slideIn 0.3s ease-out;
            min-width: 300px;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        `;

        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';

        notification.innerHTML = `
            <i class="fas ${icon}"></i>
            <span>${message}</span>
        `;

        document.body.appendChild(notification);

        // Add animation styles if not present
        if (!document.getElementById('notificationStyles')) {
            const style = document.createElement('style');
            style.id = 'notificationStyles';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        // Remove after delay
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in forwards';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
});