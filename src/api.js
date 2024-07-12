/**
 *
 *
 *
 */
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { Pool } = require('pg');


/**
 *
 *
 *
 */
const hostname = process.env.NODE_ENV === 'production' ? 'pg-service.workshop' : 'localhost';
const pool = new Pool({ connectionString: `postgresql://ab93lka1z1a:bxlao9koslq51@${hostname}:5432` });
const LOG_PRED = `INSERT INTO fct_prediction (img_json, prediction, label) VALUES ($1, $2, $3) RETURNING *;`;


/**
 *
 *
 *
 */
const app = express();
app.set('trust proxy', true);
app.use(express.json());
app.use(onReqLog);


/**
 *
 *
 *
 */
app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', req.headers.origin);
  res.header('Access-Control-Allow-Credentials', true);
  res.header('Access-Control-Max-Age', 864000);
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  next();
});


/**
 *
 *
 *
 */
const PREDICTOR = process.env.NODE_ENV === 'production'
  ? 'http://predictor-service.workshop/prediction'
  : 'http://localhost:5015/prediction';


/**
 *
 *
 *
 */
app.get('*', (req, res) => {
  res.writeHead(200, {'Content-Type': 'application/json'});
  res.end(JSON.stringify({message: 'Hello World'}) + '\n');
});


/**
 *
 *
 *
 */
app.post('/predict', async (req, res) => {
  const headers = { 'Content-Type': 'application/json' };
  const { data } = await axios.post(PREDICTOR, req.body, { headers });
  const client = await pool.connect();
  const args = [JSON.stringify(req.body['pix']), data['prediction'], req.body['label']];
  await client.query(LOG_PRED, args);
  client.release();
  res.status(200).json({ prediction: data['prediction'] });
});


/**
 *
 *
 *
 */
app.listen(3011, async () => {
  const client = await pool.connect();
  const { rows } = await client.query('SELECT NOW()');
  console.log(`rows[0].now`, rows[0].now);
  console.log(`Server started on port 3011 NODE_ENV=${process.env.NODE_ENV}`);
});


/**
 *
 *
 *
 */
const FILE = 'de2ci4a.txt';
const BASE = process.env.WRITE_PATH ?? __dirname;
const CURR_PATH = path.join(BASE, FILE);
const SEC = Math.floor(Math.random() * 10) + 10;
const TS = SEC * 1000;
console.log(`Writing to ${CURR_PATH} every ${SEC}s`);


/**
 *
 *
 *
 */
let COUNT = 0;


/**
 *
 *
 *
 */
function onWrite() {
  COUNT += 1;
  const currTs = new Date().toLocaleTimeString('en-US', { hour12: false });
  const num = COUNT.toString().padStart(3, '0');
  fs.appendFileSync(CURR_PATH, `[${currTs}] - ${num}\n`);
  const prev = fs.readFileSync(CURR_PATH, 'utf8');
  console.log(`${prev}\n====================\n`);
};


/**
 *
 *
 *
 */
function onReqLog(req, res, next) {
  const ts = new Date().toLocaleTimeString('en-US', { hour12: false });
  console.log(`[${ts}] - ${req.hostname} ${req.method} ${req.originalUrl}`);
  next();
};
