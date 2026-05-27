document.addEventListener('DOMContentLoaded', function () {
  if (typeof SweetScroll !== 'undefined') {
    new SweetScroll({});
  }

  document.querySelectorAll('.flip-card').forEach(function (card) {
    card.addEventListener('click', function () {
      card.classList.toggle('is-flipped');
    });
  });
});
