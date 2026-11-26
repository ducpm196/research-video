const fs = require('fs');
const crypto = require('crypto');
const v = fs.readFileSync(0, 'utf8').trim().split('=')[1];
const ch = crypto.createHash('sha256').update(v).digest('base64url');
console.log(`challenge=${ch}`);
console.log(`len=${ch.length}`);
console.log(`no_padding=${Number(!ch.includes('='))}`);
