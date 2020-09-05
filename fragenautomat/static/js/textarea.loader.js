(function() {
  const textareas = document.getElementsByTagName('textarea');

  function updateHeight(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.max(36, textarea.scrollHeight)}px`;
  }

  for (let textarea of textareas) {
    textarea.addEventListener('input', () => updateHeight(textarea));
  }
})();
