/* AgroTrip — interactions générales : menu mobile + slider */

document.addEventListener("DOMContentLoaded", function () {

  /* ----- Menu mobile ----- */
  const toggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => nav.classList.toggle("open"));
    nav.querySelectorAll("a").forEach(a =>
      a.addEventListener("click", () => nav.classList.remove("open"))
    );
  }

  /* ----- Slider automatique ----- */
  const slider = document.getElementById("slider");
  if (!slider) return;

  const slides = slider.querySelectorAll(".slide");
  const dots = slider.querySelectorAll(".dot");
  if (slides.length <= 1) return;

  let current = 0;
  let timer = null;

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle("active", i === current));
    dots.forEach((d, i) => d.classList.toggle("active", i === current));
  }

  function next() { show(current + 1); }
  function prev() { show(current - 1); }

  function start() { timer = setInterval(next, 5500); }
  function restart() { clearInterval(timer); start(); }

  const btnNext = document.getElementById("slide-next");
  const btnPrev = document.getElementById("slide-prev");
  if (btnNext) btnNext.addEventListener("click", () => { next(); restart(); });
  if (btnPrev) btnPrev.addEventListener("click", () => { prev(); restart(); });

  dots.forEach(dot =>
    dot.addEventListener("click", () => {
      show(parseInt(dot.dataset.index, 10));
      restart();
    })
  );

  start();
});
