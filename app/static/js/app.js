/**
 * Smart Hospital Queue – Frontend JavaScript
 */

// Live clock
function updateClock() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const el = document.getElementById('live-clock');
    if (el) el.textContent = timeStr;
}

setInterval(updateClock, 1000);
updateClock();

// Auto-refresh queue page every 30 seconds
if (window.location.pathname.includes('/queue')) {
    setTimeout(() => {
        window.location.reload();
    }, 30000);
}

// Tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
});
