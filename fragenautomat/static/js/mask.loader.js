
(function() {
  for (let a of document.querySelectorAll('a.mask')) {
    const targetSelector = a.dataset.target;
    a.onclick = function() {
      for (let target of document.querySelectorAll(targetSelector)) {
        target.classList.toggle('is-masked');
      }
    }
  }
}());
