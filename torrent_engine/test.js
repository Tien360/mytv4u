const torrentStream = require('torrent-stream');
const memoryChunkStore = require('memory-chunk-store');

const infoHash = '08ada5a7a6183aae1e09d831df6748d566095a10'; // Ubuntu torrent infohash or similar
// Let's use a known infohash, e.g. a recent movie or ubuntu
const magnet = 'magnet:?xt=urn:btih:08ada5a7a6183aae1e09d831df6748d566095a10';

var engine = torrentStream(magnet, {
  storage: memoryChunkStore
});

engine.on('ready', function() {
  console.log('READY!');
  console.log('Files:', engine.files.map(f => f.name));
  process.exit(0);
});

engine.on('error', function(err) {
  console.log('ERROR:', err);
  process.exit(1);
});

setTimeout(() => {
  console.log('Timeout');
  process.exit(1);
}, 10000);
