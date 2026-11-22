const stale = 700 > 600, etagClient = '"v42"', etagSrv = '"v42"';
const code = stale ? (etagClient === etagSrv ? 304 : 200) : 200;
console.log(`is_stale=${Number(stale)}`);
console.log(`status_code=${code}`);
console.log(`body_resent=${Number(code === 200)}`);
