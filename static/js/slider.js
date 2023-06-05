const swiper= new Swiper('.swiper', {
  // Optional parameters
  slidesPerView: 6,
  breakpoints: {
        280: {
          slidesPerView: 1
        },
        500: {
          slidesPerView: 2
        },
        768: {
          slidesPerView: 3
        },
        1024: {
          slidesPerView: 4
        },
        1440: {
          slidesPerView: 6
        }
      },
  slidesPerGroup: 1,
  spaceBetween: 10,
  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

