
(function() {
  for (let button of document.querySelectorAll('button.collapse')) {
    const targetSelector = button.dataset.target;
    button.onclick = function() {
      for (let target of document.querySelectorAll(targetSelector)) {
        target.classList.toggle('is-hidden');
      }
    }
  }
}());
