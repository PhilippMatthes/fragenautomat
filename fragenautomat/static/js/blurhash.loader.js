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
}());
