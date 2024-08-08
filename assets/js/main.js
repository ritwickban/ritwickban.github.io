document.addEventListener("DOMContentLoaded",function(){new SweetScroll({}),

particlesJS("particles-js", {
    particles: {
      number: { value: 300, density: { enable: true, value_area: 800 } },
      color: { value: "#ffffff" },
      shape: {
        type: "image",
        stroke: { width: 0, color: "#000000" },
        polygon: { nb_sides: 5 },
        image: {
          src:
            "https://cdn.pixabay.com/photo/2016/11/21/20/06/snow-1847358_1280.png",
          width: 100,
          height: 100
        }
      },
      opacity: {
        value: 0.5,
        random: false,
        anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false }
      },
      size: {
        value: 6,
        random: true,
        anim: { enable: false, speed: 30, size_min: 0.1, sync: false }
      },
      line_linked: {
        enable: false,
        distance: 50,
        color: "#ffffff",
        opacity: 0.4,
        width: 1
      },
      move: {
        enable: true,
        speed: 2.0,
        direction: "bottom-left",
        random: true,
        straight: false,
        out_mode: "out",
        bounce: false,
        attract: { enable: false, rotateX: 600, rotateY: 1200 }
      }
    },
    interactivity: {
      detect_on: "canvas",
      events: {
        onhover: { enable: true, mode: "bubble" },
        onclick: { enable: true, mode: "repulse" },
        resize: true
      },
      modes: {
        grab: { distance: 400, line_linked: { opacity: 1 } },
        bubble: { distance: 100, size: 0, duration: 2, opacity: 0, speed: 3 },
        repulse: { distance: 200, duration: 0.4 },
        push: { particles_nb: 4 },
        remove: { particles_nb: 2 }
      }
    },
    retina_detect: true
  })},!1);