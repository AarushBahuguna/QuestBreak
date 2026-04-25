// QuestBreak AI — Frontend JavaScript
// Handles particles animation on landing page

document.addEventListener('DOMContentLoaded', () => {
    const particleContainer = document.getElementById('particles');
    if (particleContainer) {
        createParticles(particleContainer);
    }
});

function createParticles(container) {
    const count = 30;
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: ${Math.random() * 4 + 1}px;
            height: ${Math.random() * 4 + 1}px;
            background: rgba(124, 58, 237, ${Math.random() * 0.3 + 0.1});
            border-radius: 50%;
            top: ${Math.random() * 100}vh;
            left: ${Math.random() * 100}vw;
            pointer-events: none;
            z-index: 0;
            animation: float ${Math.random() * 10 + 10}s linear infinite;
        `;
        container.appendChild(particle);
    }

    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% { transform: translateY(0) translateX(0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) translateX(${Math.random() * 100 - 50}px); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}
