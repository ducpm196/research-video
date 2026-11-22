const page = 1000, size = 20, off = (page - 1) * size;
console.log(`offset_skipped=${off}`);
console.log(`offset_scanned=${off + size}`);
console.log(`cursor_scanned=${size}`);
