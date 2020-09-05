(function() {
  for (let img of document.querySelectorAll('img.blurhash')) {
    if (!img.dataset.blurhash) continue;
    const pixels = blurhash.decode(img.dataset.blurhash, 32, 32);
    const blurHashImage = blurhash.getImageDataAsImage(
      pixels, 32, 32, () => {}
    );

    img.src = blurHashImage.src;

    fetch(img.dataset.src).then(response => {
      response.arrayBuffer().then(buffer => {
        let binary = '';
        const bytes = [].slice.call(new Uint8Array(buffer));
        bytes.forEach((b) => binary += String.fromCharCode(b));
        img.src = `data:image/jpeg;base64,${window.btoa(binary)}`;
      });
    });
  }
})();

(function() {
  for (let form of document.querySelectorAll('form')) {
    const submitButton = form.querySelector('button');
    for (let input of form.querySelectorAll('input[type="file"]')) {
      const name = input.name;
      const blurhashInputName = `${name}_blurhash`;
      const blurhashInput = form.querySelector(
        `input[name="${blurhashInputName}"]`
      );
      const reader = new FileReader();

      input.addEventListener('change', function() {
        submitButton.classList.add('is-loading');
        submitButton.disabled = true;
        reader.readAsDataURL(input.files[0]);
      });

      reader.addEventListener('load', function() {
        const image = new Image();

        image.addEventListener('load', function() {
          const imageData = blurhash.getImageData(image);
          blurhash.encodePromise(
            imageData, image.width, image.height, 4, 3
          ).then(function(hash) {
            blurhashInput.value = hash;
            submitButton.disabled = false;
            submitButton.classList.remove('is-loading');
          });
        });

        image.src = reader.result;
      });
    }
  }
})();

