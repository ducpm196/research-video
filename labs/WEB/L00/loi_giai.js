const stages = ['TCP', 'TLS', 'HTTP'], ttfb = rtt => stages.length * rtt;
console.log(`ttfb_50ms=${ttfb(50)}`);
console.log(`remote_200ms_4api=${ttfb(200) + 4 * 200}`);
console.log(`roundtrips_handshake=${stages.length}`);
