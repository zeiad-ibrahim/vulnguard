// Navigation function to switch pages
function navigateTo(page) {
    window.location.href = page;
}
function logout() {
    // Clear user session (simple example)
    localStorage.removeItem('loggedInUser');
    alert('You have been logged out.');
    window.location.href = 'login.html';
}

