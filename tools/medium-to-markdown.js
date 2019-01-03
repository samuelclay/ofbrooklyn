const mediumToMarkdown = require('medium-to-markdown');
 
mediumToMarkdown.convertFromUrl('https://medium.com/@samuelclay/everything-you-need-to-build-your-own-turn-touch-smart-remote-inlaying-with-a-laser-6da2bb50c546')
.then(function (markdown) {
  console.log(markdown); //=> Markdown content of medium post
});