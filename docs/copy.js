// Adds a Copy button to every .cmd block on the page.
document.querySelectorAll('.cmd').forEach(function (box) {
  var pre = box.querySelector('pre');
  var button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy';
  button.textContent = 'Copy';
  button.addEventListener('click', function () {
    var done = function () {
      button.textContent = 'Copied';
      setTimeout(function () { button.textContent = 'Copy'; }, 1500);
    };
    var fallback = function () {
      var range = document.createRange();
      range.selectNodeContents(pre);
      var selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Selected';
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(pre.textContent).then(done, fallback);
    } else {
      fallback();
    }
  });
  box.appendChild(button);
});
