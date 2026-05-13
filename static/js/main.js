/* =====================================================
   PyAnalyzer - Main Application JavaScript
   AI Assistant & UI Functionality
   ===================================================== */

document.addEventListener('DOMContentLoaded', function() {
    initApp();
    initAIWidget();
    initThemeToggle();
    initAnimations();
});

// Initialize application
function initApp() {
    console.log('🚀 PyAnalyzer Initialized');
}

// ==================== AI WIDGET ====================
function initAIWidget() {
    const toggle = document.getElementById('aiToggle');
    const close = document.getElementById('aiClose');
    const panel = document.getElementById('aiPanel');
    const input = document.getElementById('aiInput');
    const sendBtn = document.getElementById('aiSend');
    
    if (!toggle || !panel) return;
    
    // Toggle panel
    toggle.addEventListener('click', () => {
        panel.classList.toggle('active');
        if (panel.classList.contains('active')) {
            setTimeout(() => input.focus(), 300);
        }
    });
    
    close.addEventListener('click', () => {
        panel.classList.remove('active');
    });
    
    // Send message
    const sendMessage = () => {
        const message = input.value.trim();
        if (!message) return;
        
        addUserMessage(message);
        input.value = '';
        
        // Show typing
        showTyping();
        
        // Get AI response
        fetch('/api/ai-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
            hideTyping();
            addBotMessage(data.response);
        })
        .catch(() => {
            hideTyping();
            addBotMessage("I'm here to help! Try asking about Python errors.");
        });
    };
    
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}

function addUserMessage(message) {
    const messages = document.getElementById('aiMessages');
    const div = document.createElement('div');
    div.className = 'ai-message ai-message-user';
    div.innerHTML = `
        <div class="ai-avatar-sm"><i class="fas fa-user"></i></div>
        <div class="ai-message-content">${escapeHtml(message)}</div>
    `;
    messages.appendChild(div);
    scrollToBottom();
}

function addBotMessage(message) {
    const messages = document.getElementById('aiMessages');
    const div = document.createElement('div');
    div.className = 'ai-message ai-message-bot';
    div.innerHTML = `
        <div class="ai-avatar-sm"><i class="fas fa-robot"></i></div>
        <div class="ai-message-content">${formatMessage(message)}</div>
    `;
    messages.appendChild(div);
    scrollToBottom();
}

function showTyping() {
    const messages = document.getElementById('aiMessages');
    const div = document.createElement('div');
    div.className = 'ai-message ai-message-bot';
    div.id = 'aiTyping';
    div.innerHTML = `
        <div class="ai-avatar-sm"><i class="fas fa-robot"></i></div>
        <div class="ai-typing">
            <span></span><span></span><span></span>
        </div>
    `;
    messages.appendChild(div);
    scrollToBottom();
}

function hideTyping() {
    const typing = document.getElementById('aiTyping');
    if (typing) typing.remove();
}

function scrollToBottom() {
    const messages = document.getElementById('aiMessages');
    messages.scrollTop = messages.scrollHeight;
}

function formatMessage(message) {
    // Convert URLs to links
    message = message.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    // Convert code blocks
    message = message.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Convert line breaks to paragraphs
    message = message.split('\n').map(line => {
        if (line.trim()) return `<p>${line}</p>`;
        return '';
    }).join('');
    
    return message;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== THEME TOGGLE ====================
function initThemeToggle() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    toggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
        showToast(`Switched to ${newTheme} mode`, 'info');
    });
}

function updateThemeIcon(theme) {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    const icon = toggle.querySelector('i');
    if (icon) {
        icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

// ==================== ANIMATIONS ====================
function initAnimations() {
    // Add animation classes to elements
    const animateElements = document.querySelectorAll('.card, .stat-card, .feature-card, .error-card');
    
    animateElements.forEach((el, index) => {
        el.classList.add('animate-fadeInUp');
        el.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Counter animation
    const counters = document.querySelectorAll('[data-count]');
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.count);
        animateCounter(counter, target, 1500);
    });
}

function animateCounter(element, target, duration) {
    let current = 0;
    const increment = target / (duration / 16);
    const step = () => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
        } else {
            element.textContent = Math.floor(current);
            requestAnimationFrame(step);
        }
    };
    step();
}

// ==================== TOAST NOTIFICATIONS ====================
function showToast(message, type = 'info', duration = 3500) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = '';
    switch(type) {
        case 'success': icon = '<i class="fas fa-check-circle" style="color: var(--success);"></i>'; break;
        case 'error': icon = '<i class="fas fa-times-circle" style="color: var(--error);"></i>'; break;
        case 'warning': icon = '<i class="fas fa-exclamation-triangle" style="color: var(--warning);"></i>'; break;
        default: icon = '<i class="fas fa-info-circle" style="color: var(--info);"></i>';
    }
    
    toast.innerHTML = `
        ${icon}
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(400px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// ==================== COPY TO CLIPBOARD ====================
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

// ==================== GLOBAL FUNCTIONS ====================
window.showToast = showToast;
window.copyToClipboard = copyToClipboard;

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K for AI focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('aiToggle')?.click();
    }
});