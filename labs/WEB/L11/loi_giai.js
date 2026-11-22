const lin = c => (c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
const lum = hex => 0.2126*lin(parseInt(hex.slice(1,3),16)/255)+0.7152*lin(parseInt(hex.slice(3,5),16)/255)+0.0722*lin(parseInt(hex.slice(5,7),16)/255);
const cr = (h1, h2) => { const [a, b] = [lum(h1), lum(h2)].sort((x,y)=>y-x); return (a+0.05)/(b+0.05); };
const r1 = cr('#777777', '#ffffff'), r2 = cr('#767676', '#ffffff');
console.log(`ratio_777=${r1.toFixed(2)}`); console.log(`ratio_767676=${r2.toFixed(2)}`);
console.log(`aa_pass_pair=${Number(r1 >= 4.5)},${Number(r2 >= 4.5)}`);
