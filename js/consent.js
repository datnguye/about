// Cookie Consent Management
(function() {
    const CONSENT_COOKIE_NAME = 'cookie_consent';
    const CONSENT_DURATION = 365; // days
    
    // Helper functions
    function setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = name + '=' + value + ';expires=' + expires.toUTCString() + ';path=/';
    }
    
    function getCookie(name) {
        const nameEQ = name + '=';
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
    
    function getConsentStatus() {
        const consent = getCookie(CONSENT_COOKIE_NAME);
        if (consent) {
            try {
                return JSON.parse(consent);
            } catch (e) {
                return null;
            }
        }
        return null;
    }
    
    function setConsentStatus(status) {
        setCookie(CONSENT_COOKIE_NAME, JSON.stringify(status), CONSENT_DURATION);
    }
    
    function showConsentPopup() {
        document.getElementById('cookie-consent-popup').style.display = 'block';
    }
    
    function hideConsentPopup() {
        document.getElementById('cookie-consent-popup').style.display = 'none';
    }
    
    function showPreferencesModal() {
        document.getElementById('cookie-preferences-modal').style.display = 'block';
        const consent = getConsentStatus();
        if (consent && consent.analytics) {
            document.getElementById('analytics-consent').checked = true;
        }
    }
    
    function hidePreferencesModal() {
        document.getElementById('cookie-preferences-modal').style.display = 'none';
    }
    
    function initializeAnalytics() {
        if (typeof gtag === 'function') {
            gtag('consent', 'update', {
                'analytics_storage': 'granted'
            });
        }
    }
    
    function disableAnalytics() {
        if (typeof gtag === 'function') {
            gtag('consent', 'update', {
                'analytics_storage': 'denied'
            });
        }
    }
    
    // Initialize consent
    function initializeConsent() {
        // Set default consent state
        if (typeof gtag === 'function') {
            gtag('consent', 'default', {
                'analytics_storage': 'denied'
            });
        }
        
        const consent = getConsentStatus();
        if (!consent) {
            showConsentPopup();
        } else {
            if (consent.analytics) {
                initializeAnalytics();
            }
        }
    }
    
    // Event listeners
    document.addEventListener('DOMContentLoaded', function() {
        initializeConsent();
        
        // Accept all cookies
        document.getElementById('cookie-consent-accept').addEventListener('click', function() {
            setConsentStatus({ necessary: true, analytics: true });
            initializeAnalytics();
            hideConsentPopup();
        });
        
        // Reject all cookies
        document.getElementById('cookie-consent-reject').addEventListener('click', function() {
            setConsentStatus({ necessary: true, analytics: false });
            disableAnalytics();
            hideConsentPopup();
        });
        
        // Manage preferences
        document.getElementById('cookie-consent-manage').addEventListener('click', function(e) {
            e.preventDefault();
            showPreferencesModal();
        });
        
        // Save preferences
        document.getElementById('cookie-save-preferences').addEventListener('click', function() {
            const analyticsConsent = document.getElementById('analytics-consent').checked;
            setConsentStatus({ necessary: true, analytics: analyticsConsent });
            
            if (analyticsConsent) {
                initializeAnalytics();
            } else {
                disableAnalytics();
            }
            
            hidePreferencesModal();
            hideConsentPopup();
        });
        
        // Close modal
        document.querySelector('.cookie-modal-close').addEventListener('click', function() {
            hidePreferencesModal();
        });
        
        // Close modal on outside click
        window.addEventListener('click', function(event) {
            const modal = document.getElementById('cookie-preferences-modal');
            if (event.target === modal) {
                hidePreferencesModal();
            }
        });
    });
})();