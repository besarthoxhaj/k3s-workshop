/**
 *
 *
 *
 */
const fs = require('fs');
const express = require('express');
const app = express();
const html = fs.readFileSync('./static.html', 'utf8');


/**
 *
 *
 *
 */
app.get('/', (req, res) => {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end(html);
});


/**
 *
 *
 *
 */
app.listen(3012, () => {
  console.log(`Server started on port 3012 NODE_ENV=${process.env.NODE_ENV}`);
});
