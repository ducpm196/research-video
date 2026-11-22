const w = 200, pad = 20, bd = 5;
const cb = w + 2 * (pad + bd), bb = w;
const specA = [1, 0, 1], specB = [0, 2, 1];
console.log(`content_box_w=${cb}`); console.log(`border_box_w=${bb}`);
console.log(`id_beats_2class=${Number(specA[0] > specB[0])}`);
