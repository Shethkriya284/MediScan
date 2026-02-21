// Main JS file for interactions
document.addEventListener('DOMContentLoaded', () => {
    // Preloader - Only show if body has 'show-preloader' class
    const preloader = document.getElementById('preloader');
    if (document.body.classList.contains('show-preloader')) {
        setTimeout(() => {
            document.body.classList.add('loaded');
        }, 1500);
    } else {
        // Immediately hide if not needed
        if (preloader) preloader.style.display = 'none';
        document.body.classList.add('loaded');
    }

    console.log('MediScan App Loaded');

    // Example: Add simple animation to cards on load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
