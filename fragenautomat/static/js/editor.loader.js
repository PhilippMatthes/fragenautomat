const descriptionTextarea = document.querySelector('textarea[name="description"]');
const descriptionTextareaTarget = document.querySelector('#description');
const solutionTextarea = document.querySelector('textarea[name="solution"]');
const solutionTextareaTarget = document.querySelector('#solution');

const converter = new showdown.Converter();

descriptionTextarea.addEventListener('input', function() {
  const markdown = descriptionTextarea.value;
  descriptionTextareaTarget.innerHTML = converter.makeHtml(markdown);
});

solutionTextarea.addEventListener('input', function() {
  const markdown = solutionTextarea.value;
  solutionTextareaTarget.innerHTML = converter.makeHtml(markdown);
});
