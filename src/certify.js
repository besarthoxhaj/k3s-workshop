/**
 *
 *
 *
 */
(async () => {
  const http = require('http');
  const acme = require('acme-client');
  const fs = require('fs');
  const path = require('path');
  const store = {};

  /**
   *
   *
   *
   */
  const directoryUrl = acme.directory.letsencrypt.production;
  const accountKey = await acme.crypto.createPrivateKey();
  const client = new acme.Client({ directoryUrl, accountKey });

  /**
   *
   *
   *
   */
  const server = http.createServer((req, res) => {
    if (req.url.startsWith('/.well-known/acme-challenge/')) {
      return res.end(store[req.url.split('/').pop()]);
    }
    res.end('Hello World\n');
  });

  /**
   *
   *
   *
   */
  async function onCertificate() {
    const [key, csr] = await acme.forge.createCsr({ commonName: 'mlx.today', altNames: [] });
    const cert = await client.auto({
      csr,
      email: 'besartshyti@gmail.com',
      termsOfServiceAgreed: true,
      challengeCreateFn: (_, challenge, keyAuthorization) => store[challenge.token] = keyAuthorization,
      challengeRemoveFn: (_, challenge) => { delete store[challenge.token]; },
    });

    /**
     *
     *
     *
     */
    fs.writeFileSync(path.join(__dirname, 'tls.cert.pem'), cert);
    fs.writeFileSync(path.join(__dirname, 'tls.key.pem'), key);
  }

  /**
   *
   *
   *
   */
  server.listen(80, () => console.log('Running'));
  await onCertificate();
  server.close();
})();