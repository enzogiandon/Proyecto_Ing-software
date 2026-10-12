import { tsParticles } from "https://cdn.jsdelivr.net/npm/@tsparticles/engine/+esm";
import { loadSlim } from "https://cdn.jsdelivr.net/npm/@tsparticles/slim/+esm";

document.addEventListener('DOMContentLoaded', async function () {
    await loadSlim(tsParticles);

    await tsParticles.load({
        id: "particles-js",
        options: {
            particles: {
                number: { value: 200, density: { enable: true, area: 800 } },
                color: { value: "#ffffff" },
                shape: { type: "circle" },
                opacity: { value: 0.4 },
                size: { value: { min: 1, max: 3 } },
                links: { enable: true, distance: 200, color: "#ffffff", opacity: 0.4, width: 1 },
                move: { enable: true, speed: 2 }
            },
            interactivity: {
                events: {
                    onHover: { enable: true, mode: "repulse" },
                    onClick: { enable: true, mode: "bubble" },
                    resize: true
                },
                modes: {
                    repulse: { distance: 70, duration: 0.5 },
                    bubble: {
                        distance: 100,
                        size: 6,
                        duration: 0.3,
                        opacity: 0.8
                    }
                }
            }
        }
    });
});

