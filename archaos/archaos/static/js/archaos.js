const swiper = new Swiper(".swiper", {
  direction: "horizontal",
  loop: true,
  grabCursor: true,
  preloadImages: false,
  lazy: true,
  keyboard: {
    enabled: true,
  },
  pagination: {
    el: ".swiper-pagination",
    type: "bullets",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  on: {
    init: function () {
      // On initialization, preload the first image
      const firstSlide = this.slides[0];
      const firstImg = firstSlide.querySelector("img");
      if (firstImg) {
        firstImg.loading = "eager";
      }
    },
    slideChange: function () {
      const currentSlideIndex = this.activeIndex;
      const nextSlideIndex = currentSlideIndex + 1;
      const currentSlide = this.slides[currentSlideIndex];
      const nextSlide = this.slides[nextSlideIndex];

      // Change the current slide image to eager
      const currentImg = currentSlide.querySelector("img");
      if (currentImg) {
        currentImg.loading = "eager";
      }

      // Preload the next slide image by setting loading to eager
      const nextImg = nextSlide ? nextSlide.querySelector("img") : null;
      if (nextImg) {
        nextImg.loading = "eager";
      }
    }
  }
});