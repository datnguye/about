// Homepage Specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const storySections = document.querySelectorAll('.story-section');

    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px 80px 0px'
        };

        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    obs.unobserve(entry.target);
                }
            });
        }, observerOptions);

        storySections.forEach(section => observer.observe(section));

        setTimeout(() => {
            storySections.forEach(section => section.classList.add('visible'));
        }, 2500);
    } else {
        storySections.forEach(section => section.classList.add('visible'));
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }
        });
    });

    // Optional: Add typing animation restart on scroll
    const typingElements = document.querySelectorAll('.typing-text');
    if (typingElements.length > 0) {
        const typingObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Restart typing animation
                    entry.target.style.animation = 'none';
                    entry.target.offsetHeight; // Trigger reflow
                    entry.target.style.animation = 'typewriter 3s steps(40) 1s forwards, blink 1s step-end infinite';
                }
            });
        }, { threshold: 0.5 });

        typingElements.forEach(element => {
            typingObserver.observe(element);
        });
    }

    // Add hover effects for cards
    document.querySelectorAll('.hover-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add click effects for buttons
    document.querySelectorAll('a[class*="rounded-full"]').forEach(button => {
        button.addEventListener('click', function(e) {
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'absolute inset-0 rounded-full bg-white opacity-25 transform scale-0 transition-transform duration-300';
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = size + 'px';
            ripple.style.height = size + 'px';
            ripple.style.left = (rect.width - size) / 2 + 'px';
            ripple.style.top = (rect.height - size) / 2 + 'px';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.style.transform = 'scale(2)';
                ripple.style.opacity = '0';
            }, 10);
            
            setTimeout(() => {
                if (ripple.parentNode) {
                    ripple.parentNode.removeChild(ripple);
                }
            }, 300);
        });
    });

    // Console easter egg
    console.log(`
    ╔══════════════════════════════════════════════════════════════╗
    ║  Welcome to Dat Nguyen's Data & AI Engineering Portfolio!   ║
    ║                                                              ║
    ║  SELECT * FROM developers WHERE is_awesome = true;           ║
    ║  -- Result: You found the easter egg! 🎉                    ║
    ║                                                              ║
    ║  Feel free to explore the code and connect with me!         ║
    ╚══════════════════════════════════════════════════════════════╝
    `);
});