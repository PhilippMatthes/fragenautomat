(function() {
  const converter = new showdown.Converter();
  for (let div of document.querySelectorAll('div.markdown')) {
    const markdown = div.dataset.markdown;
    div.innerHTML = converter.makeHtml(markdown);
  }
}());
