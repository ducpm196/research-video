const crypto = require('crypto');
const v = 'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk';
const ch = crypto.createHash('sha256').update(v).digest('base64url');
console.log(`challenge=${ch}`);
console.log(`len=${ch.length}`);
console.log(`no_padding=${Number(!ch.includes('='))}`);
