/* ============================================
   ClinicPro Management System - SKY GLASS
   Enhanced Glassy Animations & Interactions v2.0
   Developer: Mohammed Usman | GitHub: issu321
   ============================================ */

function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.content : '';
}

async function fetchWithAuth(url, options = {}) {
    const defaultOptions = {
        headers: {
            'X-CSRF-Token': getCsrfToken(),
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...options.headers
        }
    };
    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
        defaultOptions.body = JSON.stringify(options.body);
    } else if (options.body) {
        defaultOptions.body = options.body;
    }
    try {
        showLoading();
        const response = await fetch(url, { ...defaultOptions, ...options });
        hideLoading();
        return response;
    } catch (error) {
        hideLoading();
        showToast('Network error. Please check your connection.', 'error');
        throw error;
    }
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    };
    toast.innerHTML = `
        <div class="toast-icon"><i class="fas ${icons[type] || icons.info}"></i></div>
        <div class="toast-message">${message}</div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

function formatCurrency(amount, currencyCode) {
    if (amount === null || amount === undefined) return '';
    const num = parseFloat(amount);
    if (isNaN(num)) return '';
    return `${currencyCode} ${num.toFixed(2)}`;
}

function confirmAction(message) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay active';
        modal.style.animation = 'fadeIn 0.3s ease';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 420px;">
                <div class="modal-header">
                    <h3 class="modal-title"><i class="fas fa-question-circle" style="color: #fbbf24; margin-right: 8px;"></i>Confirm Action</h3>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">&times;</button>
                </div>
                <p style="margin-bottom: 24px; color: var(--text-secondary); line-height: 1.6;">${message}</p>
                <div class="modal-footer">
                    <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove(); window._confirmResult = false;">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                    <button class="btn btn-danger" onclick="this.closest('.modal-overlay').remove(); window._confirmResult = true;">
                        <i class="fas fa-check"></i> Confirm
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
                document.body.style.overflow = '';
                window._confirmResult = false;
            }
        });
        const checkResult = setInterval(() => {
            if (window._confirmResult !== undefined) {
                clearInterval(checkResult);
                const result = window._confirmResult;
                delete window._confirmResult;
                document.body.style.overflow = '';
                resolve(result);
            }
        }, 100);
    });
}

async function populateDropdown(url, elementId, valueField, textField, selectedValue = '') {
    const select = document.getElementById(elementId);
    if (!select) return;
    try {
        const response = await fetch(url);
        const data = await response.json();
        select.innerHTML = '<option value="">Select...</option>';
        data.data.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valueField];
            option.textContent = textField ? `${item[valueField]} - ${item[textField]}` : item[valueField];
            if (item[valueField] === selectedValue) option.selected = true;
            select.appendChild(option);
        });
    } catch (error) {
        showToast('Failed to load dropdown data', 'error');
    }
}

async function loadCurrencies(selectedCode = '') {
    await populateDropdown('/api/currencies', 'currency', 'code', 'name', selectedCode);
}

async function loadTimezones(selectedTz = '') {
    const select = document.getElementById('timezone');
    if (!select) return;
    try {
        const response = await fetch('/api/timezones');
        const data = await response.json();
        select.innerHTML = '<option value="">Select Timezone...</option>';
        data.data.forEach(tz => {
            const option = document.createElement('option');
            option.value = tz;
            option.textContent = tz;
            if (tz === selectedTz) option.selected = true;
            select.appendChild(option);
        });
    } catch (error) {
        showToast('Failed to load timezones', 'error');
    }
}

async function loadCountries(selectedCountry = '') {
    await populateDropdown('/api/countries', 'country', 'name', null, selectedCountry);
}

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('active');
}

function initMobileNav() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navOverlay = document.getElementById('navOverlay');
    if (!navToggle || !navMenu) return;
    navToggle.addEventListener('click', () => {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        if (navOverlay) navOverlay.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });
    if (navOverlay) {
        navOverlay.addEventListener('click', () => {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
            navOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    navMenu.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                if (navOverlay) navOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        const content = modal.querySelector('.modal-content');
        if (content) {
            content.style.animation = 'none';
            content.offsetHeight;
            content.style.animation = '';
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function initModals() {
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
}

function initTabs() {
    document.querySelectorAll('.tabs').forEach(tabContainer => {
        const buttons = tabContainer.querySelectorAll('.tab-btn');
        const panels = tabContainer.closest('.tab-wrapper')?.querySelectorAll('.tab-panel');
        buttons.forEach((btn, index) => {
            btn.addEventListener('click', () => {
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                if (panels) {
                    panels.forEach(p => {
                        p.classList.remove('active');
                        p.style.opacity = '0';
                    });
                    if (panels[index]) {
                        panels[index].classList.add('active');
                        setTimeout(() => {
                            panels[index].style.opacity = '1';
                        }, 50);
                    }
                }
            });
        });
    });
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'var(--danger)';
            input.style.boxShadow = '0 0 0 3px rgba(239, 83, 80, 0.15)';
            input.style.animation = 'shake 0.5s ease';
            input.addEventListener('input', function handler() {
                this.style.borderColor = '';
                this.style.boxShadow = '';
                this.style.animation = '';
                this.removeEventListener('input', handler);
            }, { once: true });
        }
    });
    return isValid;
}

const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-8px); }
        40% { transform: translateX(8px); }
        60% { transform: translateX(-4px); }
        80% { transform: translateX(4px); }
    }
`;
document.head.appendChild(shakeStyle);

function formatPhone(phone) {
    if (!phone) return '';
    return phone.replace(/\D/g, '');
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function initSearchFilter(searchInputId, itemsContainerSelector, itemSelector, searchFields) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;
    const container = document.querySelector(itemsContainerSelector);
    if (!container) return;
    searchInput.addEventListener('input', debounce((e) => {
        const query = e.target.value.toLowerCase().trim();
        const items = container.querySelectorAll(itemSelector);
        items.forEach(item => {
            let text = '';
            searchFields.forEach(field => {
                const el = item.querySelector(field);
                if (el) text += ' ' + el.textContent.toLowerCase();
            });
            item.style.display = text.includes(query) ? '' : 'none';
            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            if (text.includes(query)) {
                item.style.opacity = '1';
                item.style.transform = 'scale(1)';
            } else {
                item.style.opacity = '0';
                item.style.transform = 'scale(0.95)';
            }
        });
    }, 300));
}

function initParticles() {
    const container = document.getElementById('heroParticles');
    if (!container) return;
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (8 + Math.random() * 12) + 's';
        const size = 2 + Math.random() * 5;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.opacity = 0.2 + Math.random() * 0.5;
        container.appendChild(particle);
    }
}

function showSkeleton(container, count = 3) {
    container.innerHTML = '';
    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = 'glass-card';
        skeleton.style.padding = '24px';
        skeleton.style.animationDelay = (i * 0.1) + 's';
        skeleton.innerHTML = `
            <div class="skeleton" style="height: 22px; width: 60%; margin-bottom: 14px;"></div>
            <div class="skeleton" style="height: 14px; width: 80%; margin-bottom: 10px;"></div>
            <div class="skeleton" style="height: 14px; width: 40%;"></div>
        `;
        container.appendChild(skeleton);
    }
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
    } catch (err) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Copied to clipboard!', 'success');
    }
}

function initPasswordToggle() {
    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', () => {
            const input = document.querySelector(toggle.dataset.target);
            if (input) {
                input.type = input.type === 'password' ? 'text' : 'password';
                const icon = toggle.querySelector('i');
                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
                icon.style.transform = 'scale(1.2)';
                setTimeout(() => icon.style.transform = '', 200);
            }
        });
    });
}

function smoothScrollTo(element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function handleFormErrors(form, errors) {
    Object.keys(errors).forEach(field => {
        const input = form.querySelector(`[name="${field}"]`);
        if (input) {
            input.style.borderColor = 'var(--danger)';
            input.style.boxShadow = '0 0 0 3px rgba(239, 83, 80, 0.15)';
            input.style.animation = 'shake 0.5s ease';
            const errorDiv = document.createElement('div');
            errorDiv.className = 'form-error';
            errorDiv.style.cssText = 'color: var(--danger); font-size: 0.8rem; margin-top: 6px; display: flex; align-items: center; gap: 4px;';
            errorDiv.innerHTML = `<i class="fas fa-exclamation-circle" style="font-size: 0.7rem;"></i> ${errors[field]}`;
            input.parentNode.appendChild(errorDiv);
            input.addEventListener('input', function handler() {
                this.style.borderColor = '';
                this.style.boxShadow = '';
                this.style.animation = '';
                const err = this.parentNode.querySelector('.form-error');
                if (err) {
                    err.style.opacity = '0';
                    setTimeout(() => err.remove(), 300);
                }
                this.removeEventListener('input', handler);
            }, { once: true });
        }
    });
}

function initLazyImages() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    img.style.opacity = '0';
                    img.onload = () => {
                        img.style.transition = 'opacity 0.5s ease';
                        img.style.opacity = '1';
                    };
                    observer.unobserve(img);
                }
            });
        });
        document.querySelectorAll('img.lazy').forEach(img => imageObserver.observe(img));
    }
}

function initResponsiveTables() {
    document.querySelectorAll('.table-responsive').forEach(wrapper => {
        const table = wrapper.querySelector('table');
        if (!table || window.innerWidth >= 768) return;
    });
}

function initPullToRefresh(callback) {
    if (!('ontouchstart' in window)) return;
    let startY = 0;
    let isRefreshing = false;
    document.addEventListener('touchstart', (e) => {
        if (window.scrollY === 0) {
            startY = e.touches[0].clientY;
        }
    }, { passive: true });
    document.addEventListener('touchmove', (e) => {
        if (window.scrollY === 0 && !isRefreshing) {
            const diff = e.touches[0].clientY - startY;
            if (diff > 100) {
                isRefreshing = true;
                callback();
                setTimeout(() => { isRefreshing = false; }, 2000);
            }
        }
    }, { passive: true });
}

function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.style.opacity = '1';
                el.style.transform = 'translateY(0) scale(1)';
                if (el.classList.contains('company-card') || el.classList.contains('glass-card')) {
                    el.style.transition = 'opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1), transform 0.7s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.7s ease';
                } else {
                    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                }
                observer.unobserve(el);
            }
        });
    }, {
        threshold: 0.08,
        rootMargin: '0px 0px -40px 0px'
    });
    const revealSelectors = '.glass-card, .stat-card, .feature-card, .company-card, .mobile-card, .company-select-card';
    document.querySelectorAll(revealSelectors).forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px) scale(0.97)';
        const delay = (index % 6) * 0.08;
        el.style.transitionDelay = `${delay}s`;
        observer.observe(el);
    });
}

function initParallax() {
    const parallaxElements = document.querySelectorAll('.hero-section, .auth-container');
    window.addEventListener('scroll', debounce(() => {
        const scrolled = window.pageYOffset;
        parallaxElements.forEach(el => {
            if (el) {
                el.style.backgroundPositionY = (scrolled * 0.3) + 'px';
            }
        });
    }, 16));
}

function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    let lastScroll = 0;
    window.addEventListener('scroll', debounce(() => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 50) {
            navbar.style.background = 'rgba(10, 22, 40, 0.9)';
            navbar.style.backdropFilter = 'blur(30px)';
            navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
            navbar.style.borderBottomColor = 'rgba(100, 181, 246, 0.1)';
        } else {
            navbar.style.background = 'rgba(10, 22, 40, 0.6)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.boxShadow = 'none';
            navbar.style.borderBottomColor = 'var(--glass-border)';
        }
        lastScroll = currentScroll;
    }, 50));
}

function initHoverTilt() {
    if (window.matchMedia('(pointer: coarse)').matches) return;
    document.querySelectorAll('.glass-card, .company-card, .feature-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 25;
            const rotateY = (centerX - x) / 25;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px) scale(1.01)`;
            card.style.transition = 'transform 0.1s ease-out';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });
}

function initMagneticCards() {
    if (window.matchMedia('(pointer: coarse)').matches) return;
    document.querySelectorAll('.company-card, .stat-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            card.style.transform = `translate(${x * 0.02}px, ${y * 0.02}px) translateY(-4px)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

function initGlitterText() {
    document.querySelectorAll('.page-title, .hero-title, .auth-title').forEach(el => {
        el.style.backgroundSize = '200% auto';
        el.style.animation = 'glitterShift 4s ease-in-out infinite';
    });
}

const glitterStyle = document.createElement('style');
glitterStyle.textContent = `
    @keyframes glitterShift {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }
`;
document.head.appendChild(glitterStyle);

function initCardStagger() {
    const grids = document.querySelectorAll('.company-grid, .stats-grid, .features-grid, .company-select-grid');
    grids.forEach(grid => {
        const cards = grid.children;
        Array.from(cards).forEach((card, i) => {
            card.style.animationDelay = `${i * 0.08}s`;
            card.classList.add('fade-in');
        });
    });
}

function initRippleEffect() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height);
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${e.clientX - rect.left - size/2}px;
                top: ${e.clientY - rect.top - size/2}px;
                background: rgba(255,255,255,0.2);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

const rippleAnim = document.createElement('style');
rippleAnim.textContent = `
    @keyframes ripple {
        to { transform: scale(2.5); opacity: 0; }
    }
`;
document.head.appendChild(rippleAnim);

function initCursorGlow() {
    if (window.matchMedia('(pointer: coarse)').matches) return;
    const glow = document.createElement('div');
    glow.style.cssText = `
        position: fixed;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(100,181,246,0.04) 0%, transparent 70%);
        pointer-events: none;
        z-index: 9999;
        transform: translate(-50%, -50%);
        transition: opacity 0.3s ease;
        opacity: 0;
    `;
    document.body.appendChild(glow);
    let mouseTimeout;
    document.addEventListener('mousemove', (e) => {
        glow.style.left = e.clientX + 'px';
        glow.style.top = e.clientY + 'px';
        glow.style.opacity = '1';
        clearTimeout(mouseTimeout);
        mouseTimeout = setTimeout(() => {
            glow.style.opacity = '0';
        }, 100);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initModals();
    initTabs();
    initPasswordToggle();
    initLazyImages();
    initResponsiveTables();
    initParticles();
    initScrollReveal();
    initParallax();
    initNavbarScroll();
    initHoverTilt();
    initMagneticCards();
    initGlitterText();
    initCardStagger();
    initRippleEffect();
    initCursorGlow();
    hideLoading();
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.6s ease';
    requestAnimationFrame(() => {
        document.body.style.opacity = '1';
    });
});

window.addEventListener('popstate', () => {
    const activeModals = document.querySelectorAll('.modal-overlay.active');
    activeModals.forEach(modal => {
        modal.classList.remove('active');
    });
    document.body.style.overflow = '';
});

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/sw.js').catch(() => {});
}

/* ============================================
   ClinicPro Management System - ULTRA LIGHT
   Enhanced Glassy Animations & Interactions v5.0
   Developer: Mohammed Usman | GitHub: issu321
   ============================================ */

function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.content : '';
}

async function fetchWithAuth(url, options = {}) {
    const defaultOptions = {
        headers: {
            'X-CSRF-Token': getCsrfToken(),
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...options.headers
        }
    };
    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
        defaultOptions.body = JSON.stringify(options.body);
    } else if (options.body) {
        defaultOptions.body = options.body;
    }
    try {
        showLoading();
        const response = await fetch(url, { ...defaultOptions, ...options });
        hideLoading();
        return response;
    } catch (error) {
        hideLoading();
        showToast('Network error. Please check your connection.', 'error');
        throw error;
    }
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icons = { success: 'fa-check-circle', error: 'fa-times-circle', warning: 'fa-exclamation-circle', info: 'fa-info-circle' };
    
    toast.style.background = 'rgba(255, 255, 255, 0.98)';
    toast.style.color = '#0f172a';
    toast.style.boxShadow = '0 10px 25px rgba(14, 165, 233, 0.15)';
    toast.style.border = '1px solid rgba(14, 165, 233, 0.15)';
    toast.style.backdropFilter = 'blur(20px)';

    toast.innerHTML = `
        <div class="toast-icon" style="color: var(--${type}); font-size: 1.2rem;"><i class="fas ${icons[type] || icons.info}"></i></div>
        <div class="toast-message" style="font-weight: 700;">${message}</div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

function formatCurrency(amount, currencyCode) {
    if (amount === null || amount === undefined) return '';
    const num = parseFloat(amount);
    if (isNaN(num)) return '';
    return `${currencyCode} ${num.toFixed(2)}`;
}

function confirmAction(message) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay active';
        modal.style.animation = 'fadeIn 0.3s ease';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 420px; background: rgba(255,255,255,0.98); color: #0f172a; border-radius: 24px; border: 1px solid rgba(14, 165, 233, 0.2);">
                <div class="modal-header">
                    <h3 class="modal-title"><i class="fas fa-question-circle" style="color: #f59e0b; margin-right: 8px;"></i>Confirm Action</h3>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()" style="color: #64748b;">&times;</button>
                </div>
                <p style="margin-bottom: 24px; color: #334155; font-weight: 600; line-height: 1.6;">${message}</p>
                <div class="modal-footer">
                    <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove(); window._confirmResult = false;">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                    <button class="btn btn-danger" onclick="this.closest('.modal-overlay').remove(); window._confirmResult = true;">
                        <i class="fas fa-check"></i> Confirm
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
                document.body.style.overflow = '';
                window._confirmResult = false;
            }
        });
        const checkResult = setInterval(() => {
            if (window._confirmResult !== undefined) {
                clearInterval(checkResult);
                const result = window._confirmResult;
                delete window._confirmResult;
                document.body.style.overflow = '';
                resolve(result);
            }
        }, 100);
    });
}

async function populateDropdown(url, elementId, valueField, textField, selectedValue = '') {
    const select = document.getElementById(elementId);
    if (!select) return;
    try {
        const response = await fetch(url);
        const data = await response.json();
        select.innerHTML = '<option value="">Select...</option>';
        data.data.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valueField];
            option.textContent = textField ? `${item[valueField]} - ${item[textField]}` : item[valueField];
            if (item[valueField] === selectedValue) option.selected = true;
            select.appendChild(option);
        });
    } catch (error) {
        showToast('Failed to load dropdown data', 'error');
    }
}

async function loadCurrencies(selectedCode = '') {
    await populateDropdown('/api/currencies', 'currency', 'code', 'name', selectedCode);
}

async function loadTimezones(selectedTz = '') {
    const select = document.getElementById('timezone');
    if (!select) return;
    try {
        const response = await fetch('/api/timezones');
        const data = await response.json();
        select.innerHTML = '<option value="">Select Timezone...</option>';
        data.data.forEach(tz => {
            const option = document.createElement('option');
            option.value = tz;
            option.textContent = tz;
            if (tz === selectedTz) option.selected = true;
            select.appendChild(option);
        });
    } catch (error) {
        showToast('Failed to load timezones', 'error');
    }
}

async function loadCountries(selectedCountry = '') {
    await populateDropdown('/api/countries', 'country', 'name', null, selectedCountry);
}

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('active');
}

function initMobileNav() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navOverlay = document.getElementById('navOverlay');
    if (!navToggle || !navMenu) return;
    navToggle.addEventListener('click', () => {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        if (navOverlay) navOverlay.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });
    if (navOverlay) {
        navOverlay.addEventListener('click', () => {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
            navOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    navMenu.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                if (navOverlay) navOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function initModals() {
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
}

function initTabs() {
    document.querySelectorAll('.tabs').forEach(tabContainer => {
        const buttons = tabContainer.querySelectorAll('.tab-btn');
        const panels = tabContainer.closest('.tab-wrapper')?.querySelectorAll('.tab-panel');
        buttons.forEach((btn, index) => {
            btn.addEventListener('click', () => {
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                if (panels) {
                    panels.forEach(p => {
                        p.classList.remove('active');
                        p.style.opacity = '0';
                    });
                    if (panels[index]) {
                        panels[index].classList.add('active');
                        setTimeout(() => { panels[index].style.opacity = '1'; }, 50);
                    }
                }
            });
        });
    });
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'var(--danger)';
            input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.15)';
            input.style.animation = 'shake 0.5s ease';
            input.addEventListener('input', function handler() {
                this.style.borderColor = '';
                this.style.boxShadow = '';
                this.style.animation = '';
                this.removeEventListener('input', handler);
            }, { once: true });
        }
    });
    return isValid;
}

const shakeStyle = document.createElement('style');
shakeStyle.textContent = `@keyframes shake { 0%, 100% { transform: translateX(0); } 20%, 60% { transform: translateX(-6px); } 40%, 80% { transform: translateX(6px); } }`;
document.head.appendChild(shakeStyle);

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => { clearTimeout(timeout); func(...args); };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function initSearchFilter(searchInputId, itemsContainerSelector, itemSelector, searchFields) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;
    const container = document.querySelector(itemsContainerSelector);
    if (!container) return;
    searchInput.addEventListener('input', debounce((e) => {
        const query = e.target.value.toLowerCase().trim();
        const items = container.querySelectorAll(itemSelector);
        items.forEach(item => {
            let text = '';
            searchFields.forEach(field => {
                const el = item.querySelector(field);
                if (el) text += ' ' + el.textContent.toLowerCase();
            });
            item.style.display = text.includes(query) ? '' : 'none';
            if (text.includes(query)) {
                item.style.opacity = '1';
                item.style.transform = 'scale(1)';
            } else {
                item.style.opacity = '0';
                item.style.transform = 'scale(0.95)';
            }
        });
    }, 300));
}

function initParticles() {
    const container = document.getElementById('heroParticles');
    if (!container) return;
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (12 + Math.random() * 15) + 's';
        const size = 3 + Math.random() * 5;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        // Ensure particles stay entirely behind content to prevent any clipping overlaps
        particle.style.zIndex = '-1';
        particle.style.background = 'rgba(14, 165, 233, 0.15)';
        particle.style.position = 'absolute';
        particle.style.borderRadius = '50%';
        container.appendChild(particle);
    }
}

function showSkeleton(container, count = 3) {
    container.innerHTML = '';
    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = 'glass-card';
        skeleton.style.padding = '24px';
        skeleton.innerHTML = `
            <div class="skeleton" style="height: 22px; width: 60%; margin-bottom: 14px; background: #cbd5e1;"></div>
            <div class="skeleton" style="height: 14px; width: 80%; margin-bottom: 10px; background: #cbd5e1;"></div>
            <div class="skeleton" style="height: 14px; width: 40%; background: #cbd5e1;"></div>
        `;
        container.appendChild(skeleton);
    }
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
    } catch (err) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Copied to clipboard!', 'success');
    }
}

function initPasswordToggle() {
    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', () => {
            const input = document.querySelector(toggle.dataset.target);
            if (input) {
                input.type = input.type === 'password' ? 'text' : 'password';
                const icon = toggle.querySelector('i');
                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
            }
        });
    });
}

function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.style.opacity = '1';
                el.style.transform = 'translateY(0) scale(1)';
                el.style.transition = 'opacity 0.6s cubic-bezier(0.25, 0.8, 0.25, 1), transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.5s ease';
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -20px 0px' });

    const revealSelectors = '.glass-card, .stat-card, .feature-card, .company-card, .mobile-card, .company-select-card';
    document.querySelectorAll(revealSelectors).forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(40px) scale(0.95)';
        const delay = (index % 8) * 0.05; 
        el.style.transitionDelay = `${delay}s`;
        observer.observe(el);
    });
}

function initHoverTilt() {
    if (window.matchMedia('(pointer: coarse)').matches) return;
    document.querySelectorAll('.glass-card, .company-card, .feature-card, .stat-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 30; 
            const rotateY = (centerX - x) / 30;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px) scale(1.02)`;
            card.style.transition = 'transform 0.1s cubic-bezier(0.25, 0.8, 0.25, 1)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
        });
    });
}

function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    window.addEventListener('scroll', debounce(() => {
        if (window.pageYOffset > 20) {
            navbar.style.background = 'rgba(255, 255, 255, 0.9)';
            navbar.style.boxShadow = '0 10px 30px rgba(14, 165, 233, 0.08)';
            navbar.style.borderBottomColor = 'rgba(14, 165, 233, 0.15)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.85)';
            navbar.style.boxShadow = 'none';
            navbar.style.borderBottomColor = 'rgba(255, 255, 255, 0.8)';
        }
    }, 10));
}

function initRippleEffect() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height);
            ripple.style.cssText = `
                position: absolute; width: ${size}px; height: ${size}px;
                left: ${e.clientX - rect.left - size/2}px; top: ${e.clientY - rect.top - size/2}px;
                background: rgba(255,255,255,0.4); border-radius: 50%;
                transform: scale(0); animation: ripple 0.6s ease-out; pointer-events: none;
            `;
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

const rippleAnim = document.createElement('style');
rippleAnim.textContent = `@keyframes ripple { to { transform: scale(2.5); opacity: 0; } }`;
document.head.appendChild(rippleAnim);

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initModals();
    initTabs();
    initPasswordToggle();
    initParticles();
    initScrollReveal();
    initHoverTilt();
    initNavbarScroll();
    initRippleEffect();
    hideLoading();
    
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.8s ease';
    requestAnimationFrame(() => {
        document.body.style.opacity = '1';
    });
});