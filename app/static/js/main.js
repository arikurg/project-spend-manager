// ==================== AUTH UTILITIES ====================

async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/me');
        return response.ok;
    } catch (error) {
        return false;
    }
}

async function updateNavigation() {
    const isLoggedIn = await checkAuthStatus();
    const navLinks = document.getElementById('navLinks');
    const authLinks = document.getElementById('authLinks');
    
    if (isLoggedIn) {
        navLinks.style.display = 'flex';
        authLinks.style.display = 'none';
    } else {
        navLinks.style.display = 'none';
        authLinks.style.display = 'flex';
    }
}

async function logout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (error) {
        console.error('Error:', error);
    }
}

// Update navigation on page load
document.addEventListener('DOMContentLoaded', updateNavigation);

