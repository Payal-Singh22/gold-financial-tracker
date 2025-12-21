// Main JavaScript file for Jewellery Billing System

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Format currency
function formatCurrency(amount) {
    return '₹ ' + parseFloat(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Format number with decimals
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// Calculate fine gold: Net weight × Tunch / 100
function calculateFineGold(netWeight, tunch) {
    return (parseFloat(netWeight) * parseFloat(tunch)) / 100;
}

// Calculate amount: Fine gold × Rate per gram
function calculateAmount(fineGold, ratePerGram) {
    return parseFloat(fineGold) * parseFloat(ratePerGram);
}

// Show loading spinner
function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    element.disabled = true;
}

// Hide loading spinner
function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

