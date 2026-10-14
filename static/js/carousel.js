// AURA Hero Banner Carousel - Minimalist Vanilla JS Implementation

document.addEventListener('DOMContentLoaded', function () {
  const carousel = document.getElementById('hero-carousel');
  if (!carousel) return;

  const slides = carousel.querySelectorAll('.carousel-slide');
  const indicators = document.querySelectorAll('.carousel-dot');
  const prevBtn = document.getElementById('carousel-prev');
  const nextBtn = document.getElementById('carousel-next');

  if (slides.length <= 1) {
    if (prevBtn) prevBtn.style.display = 'none';
    if (nextBtn) nextBtn.style.display = 'none';
    return;
  }

  let currentIndex = 0;
  let intervalId = null;
  const slideDuration = 5500; // 5.5s

  function showSlide(index) {
    if (index >= slides.length) index = 0;
    if (index < 0) index = slides.length - 1;

    slides.forEach((slide, i) => {
      if (i === index) {
        slide.classList.remove('opacity-0', 'pointer-events-none', 'z-0');
        slide.classList.add('opacity-100', 'z-10');
      } else {
        slide.classList.remove('opacity-100', 'z-10');
        slide.classList.add('opacity-0', 'pointer-events-none', 'z-0');
      }
    });

    indicators.forEach((dot, i) => {
      if (i === index) {
        dot.classList.add('bg-white', 'w-8');
        dot.classList.remove('bg-white/40', 'w-2.5');
      } else {
        dot.classList.remove('bg-white', 'w-8');
        dot.classList.add('bg-white/40', 'w-2.5');
      }
    });

    currentIndex = index;
  }

  function nextSlide() {
    showSlide(currentIndex + 1);
  }

  function prevSlide() {
    showSlide(currentIndex - 1);
  }

  function startAutoSlide() {
    stopAutoSlide();
    intervalId = setInterval(nextSlide, slideDuration);
  }

  function stopAutoSlide() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', function (e) {
      e.preventDefault();
      nextSlide();
      startAutoSlide();
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', function (e) {
      e.preventDefault();
      prevSlide();
      startAutoSlide();
    });
  }

  indicators.forEach((dot, i) => {
    dot.addEventListener('click', function () {
      showSlide(i);
      startAutoSlide();
    });
  });

  carousel.addEventListener('mouseenter', stopAutoSlide);
  carousel.addEventListener('mouseleave', startAutoSlide);

  // Initialize first slide and start autoplay
  showSlide(0);
  startAutoSlide();
});
