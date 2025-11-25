/**
 * Modern Resume - Interactive JavaScript
 */

(function() {
    'use strict';

    // ===== Smooth Scrolling =====
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Remove active class from all links
                navLinks.forEach(l => l.classList.remove('active'));
                // Add active class to clicked link
                this.classList.add('active');
                
                // Smooth scroll to section
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu if open
                const navbarNav = document.getElementById('navbarNav');
                if (navbarNav && navbarNav.classList.contains('active')) {
                    navbarNav.classList.remove('active');
                }
            }
        });
    });

    // ===== Mobile Navigation Toggle =====
    const navToggler = document.getElementById('navToggler');
    const navbarNav = document.getElementById('navbarNav');
    
    if (navToggler && navbarNav) {
        navToggler.addEventListener('click', function() {
            navbarNav.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // ===== Active Navigation on Scroll =====
    const sections = document.querySelectorAll('.section');
    
    function updateActiveNav() {
        const scrollPos = window.scrollY + 200;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveNav);
    
    // ===== Intersection Observer for Animations =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe timeline items and cards
    const animatedElements = document.querySelectorAll('.timeline-item, .education-card, .award-card, .skill-icon');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // ===== Parallax Effect for Gradient Orbs =====
    const orbs = document.querySelectorAll('.gradient-orb');
    
    window.addEventListener('mousemove', function(e) {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 20;
            const x = mouseX * speed;
            const y = mouseY * speed;
            
            orb.style.transform = `translate(${x}px, ${y}px)`;
        });
    });

    // ===== Skill Icon Hover Effects =====
    const skillIcons = document.querySelectorAll('.skill-icon');
    
    skillIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        });
    });

    // ===== Tech Tag Click Animation =====
    const techTags = document.querySelectorAll('.tech-tag');
    
    techTags.forEach(tag => {
        tag.addEventListener('click', function() {
            this.style.animation = 'pulse 0.5s ease';
            setTimeout(() => {
                this.style.animation = '';
            }, 500);
        });
    });

    // ===== Social Link Ripple Effect =====
    const socialLinks = document.querySelectorAll('.social-link');
    
    socialLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // ===== Typing Effect for Hero Title (Optional Enhancement) =====
    function typeWriter(element, text, speed = 100) {
        let i = 0;
        element.innerHTML = '';
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }

    // ===== Initialize on Load =====
    window.addEventListener('load', function() {
        // Set first nav link as active
        if (navLinks.length > 0) {
            navLinks[0].classList.add('active');
        }
        
        // Trigger initial scroll check
        updateActiveNav();
        
        // Add loaded class to body for animations
        document.body.classList.add('loaded');
    });

    // ===== Scroll to Top on Page Refresh =====
    window.addEventListener('beforeunload', function() {
        window.scrollTo(0, 0);
    });

    // ===== Performance: Debounce Scroll Events =====
    function debounce(func, wait = 10) {
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
    
    const debouncedScroll = debounce(updateActiveNav, 10);
    window.addEventListener('scroll', debouncedScroll);

    // ===== Add Pulse Animation Keyframes Dynamically =====
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        body.loaded .hero-content > * {
            animation-play-state: running;
        }
    `;
    document.head.appendChild(style);

    // ===== Console Message =====
    console.log('%c👋 Hello! Welcome to my resume website', 'color: #667eea; font-size: 16px; font-weight: bold;');
    console.log('%cBuilt with ❤️ using HTML, CSS, and JavaScript', 'color: #a0aec0; font-size: 12px;');

})();

// ===== Counter Animation for Statistics =====
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60fps
    let current = 0;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };

    updateCounter();
}

// Observe stats section for counter animation
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(num => {
                if (num.textContent === '0') {
                    animateCounter(num);
                }
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsContainer = document.querySelector('.stats-container');
if (statsContainer) {
    statsObserver.observe(statsContainer);
}

// ===== Project Filtering =====
const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

// Count projects by technology
function updateFilterCounts() {
    filterButtons.forEach(btn => {
        const filter = btn.getAttribute('data-filter');
        let count = 0;

        if (filter === 'all') {
            count = projectCards.length;
        } else {
            projectCards.forEach(card => {
                const techTags = card.querySelectorAll('.project-tech-tag');
                const hasTech = Array.from(techTags).some(tag => 
                    tag.textContent.trim() === filter
                );
                if (hasTech) count++;
            });
        }

        const countSpan = btn.querySelector('.filter-count');
        if (countSpan) {
            countSpan.textContent = `(${count})`;
        }
    });
}

// Filter projects
function filterProjects(filter) {
    projectCards.forEach(card => {
        if (filter === 'all') {
            card.classList.remove('hidden');
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            }, 10);
        } else {
            const techTags = card.querySelectorAll('.project-tech-tag');
            const hasTech = Array.from(techTags).some(tag => 
                tag.textContent.trim() === filter
            );

            if (hasTech) {
                card.classList.remove('hidden');
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                }, 10);
            } else {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    card.classList.add('hidden');
                }, 300);
            }
        }
    });
}

// Add click event to filter buttons
filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        filterButtons.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        
        // Get filter value and filter projects
        const filter = btn.getAttribute('data-filter');
        filterProjects(filter);
    });
});

// Initialize filter counts on load
if (filterButtons.length > 0) {
    updateFilterCounts();
}
