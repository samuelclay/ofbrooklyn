const mediumToMarkdown = require('medium-to-markdown');
 
mediumToMarkdown.convertFromUrl('https://medium.com/@samuelclay/everything-you-need-to-build-your-own-turn-touch-smart-remote-the-circuit-board-ab498dda1f5d')
.then(function (markdown) {
  console.log(markdown); //=> Markdown content of medium post
});