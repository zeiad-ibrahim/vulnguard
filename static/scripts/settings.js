// Reference to the notifications toggle switch
const notificationsToggle = document.getElementById('notifications-toggle');

// Load saved notification preference from localStorage
window.onload = () => {
    const notificationsEnabled = localStorage.getItem('notificationsEnabled') === 'true';
    notificationsToggle.checked = notificationsEnabled;
};

// Event listener to save the toggle state to localStorage
notificationsToggle.addEventListener('change', () => {
    const isEnabled = notificationsToggle.checked;
    localStorage.setItem('notificationsEnabled', isEnabled);
    alert(`Notifications ${isEnabled ? 'Enabled' : 'Disabled'}`);
});
