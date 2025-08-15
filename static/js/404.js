document.addEventListener('DOMContentLoaded', function() {
    // Create particle effects on mouse move
    let particleCount = 0;
    const maxParticles = 30;
    
    document.addEventListener('mousemove', function(e) {
        if (particleCount >= maxParticles) return;
        
        if (Math.random() > 0.95) {
            createParticle(e.clientX, e.clientY);
        }
    });
    
    function createParticle(x, y) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '8px';
        particle.style.height = '8px';
        particle.style.backgroundColor = 'var(--primary)';
        particle.style.borderRadius = '50%';
        particle.style.setProperty('--tx', (Math.random() - 0.5) * 100 + 'px');
        
        document.body.appendChild(particle);
        particleCount++;
        
        setTimeout(() => {
            particle.remove();
            particleCount--;
        }, 4000);
    }
    
    // Add random glitch effect to 404 number
    const glitchElement = document.querySelector('.glitch');
    if (glitchElement) {
        setInterval(() => {
            if (Math.random() > 0.95) {
                glitchElement.style.animation = 'none';
                setTimeout(() => {
                    glitchElement.style.animation = '';
                }, 100);
            }
        }, 3000);
    }
    
    // Add hover effect to floating icons
    const floatingIcons = document.querySelectorAll('.floating-icon');
    floatingIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.5) rotate(360deg)';
            this.style.opacity = '0.5';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.opacity = '';
        });
    });
    
    // Matrix-like effect in console
    console.log('%c🔍 404 - Page Not Found', 'color: #3b82f6; font-size: 24px; font-weight: bold;');
    console.log('%cLooks like you found the secret console message!', 'color: #10b981; font-size: 14px;');
    console.log('%cThe page you were looking for has vanished into the digital void...', 'color: #ef4444; font-size: 12px;');
    
    // Easter egg: Konami code
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    let konamiIndex = 0;
    
    document.addEventListener('keydown', function(e) {
        if (e.key === konamiCode[konamiIndex]) {
            konamiIndex++;
            if (konamiIndex === konamiCode.length) {
                activateEasterEgg();
                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }
    });
    
    function activateEasterEgg() {
        document.body.style.animation = 'rotate 2s ease-in-out';
        setTimeout(() => {
            document.body.style.animation = '';
            alert('🎉 You found the secret! The page is still not here though... 😅');
        }, 2000);
    }
});