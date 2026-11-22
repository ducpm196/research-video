const RFC = { GET:[1,1], PUT:[0,1], DELETE:[0,1], POST:[0,0] };
let bal = 250; const seen = new Set();
const pay = (k, v) => { if (!seen.has(k)) { seen.add(k); bal -= v; } };
pay('k1', 100); pay('k1', 100);
console.log('get_safe_idem=' + RFC.GET.join(','));
console.log('put_safe_idem=' + RFC.PUT.join(','));
console.log(`post_with_idem_key_bal=${bal}`);
