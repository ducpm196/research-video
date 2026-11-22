const out = [1]; let syncDone = 0;
setTimeout(() => { out.push(2);
  console.log(`sync_done=${syncDone}`);
  console.log('event_loop_order=' + out.join(','));
  console.log(`micro_before_macro=${Number(out.indexOf(3) < out.indexOf(2))}`);
}, 0);
Promise.resolve().then(() => out.push(3));
out.push(4); syncDone = Number(out.length === 2);
