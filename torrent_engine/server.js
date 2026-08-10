const express = require('express');
const cors = require('cors');
const torrentStream = require('torrent-stream');
const memoryChunkStore = require('memory-chunk-store');

const app = express();
app.use(cors());

// Giữ lại các instance torrent đang chạy
const engines = {};

// Các trackers cực mạnh để vét Seeders
const extraTrackers = [
  'udp://tracker.opentrackr.org:1337/announce',
  'udp://open.demonii.com:1337/announce',
  'udp://tracker.openbittorrent.com:80',
  'udp://tracker.coppersurfer.tk:6969',
  'udp://glotorrents.pw:6969/announce',
  'udp://tracker.leechers-paradise.org:6969',
  'udp://p4p.arenabg.com:1337',
  'udp://tracker.internetwarriors.net:1337',
  'wss://tracker.btorrent.xyz',
  'wss://tracker.openwebtorrent.com'
];

app.get('/:infohash/:idx', (req, res) => {
  const infoHash = req.params.infohash;
  const fileIdx = parseInt(req.params.idx, 10);
  
  // Lấy danh sách trackers từ query param (?tr=...)
  let dynamicTrackers = [];
  if (req.query.tr) {
    if (Array.isArray(req.query.tr)) {
      dynamicTrackers = req.query.tr;
    } else {
      dynamicTrackers = [req.query.tr];
    }
  }

  // Kết hợp trackers cố định và trackers từ Torrentio
  const allTrackers = [...new Set([...extraTrackers, ...dynamicTrackers])];
  
  // Tạo magnet link
  const magnetURI = `magnet:?xt=urn:btih:${infoHash}`;

  let engine = engines[infoHash];

  if (!engine) {
    // Khởi tạo torrent-stream với bộ nhớ RAM và 500 kết nối
    engine = torrentStream(magnetURI, {
      connections: 500, // Max peers
      storage: memoryChunkStore, // 100% RAM, 0 SSD writes
      trackers: allTrackers // Inject custom trackers
    });
    
    engines[infoHash] = engine;
    
    engine.on('ready', () => {
      console.log(`[Torrent Engine] ${infoHash} is ready!`);
    });
    
    // Tự dọn dẹp sau 1 tiếng không có stream
    setTimeout(() => {
      if (engines[infoHash]) {
        engines[infoHash].destroy();
        delete engines[infoHash];
      }
    }, 60 * 60 * 1000);
  }

  if (engine.files && engine.files.length > 0) {
    serveFile(engine, fileIdx, req, res);
  } else {
    engine.on('ready', () => {
      serveFile(engine, fileIdx, req, res);
    });
  }
});

function serveFile(engine, fileIdx, req, res) {
  // Lấy file theo index, nếu index out of bound thì lấy file lớn nhất
  let file = engine.files[fileIdx];
  if (!file) {
    file = engine.files.reduce((a, b) => a.length > b.length ? a : b);
  }

  // torrent-stream tự động focus vào file được gọi `createReadStream()`
  file.select();

  const total = file.length;
  const range = req.headers.range;

  if (range) {
    const parts = range.replace(/bytes=/, "").split("-");
    const partialstart = parts[0];
    const partialend = parts[1];

    const start = parseInt(partialstart, 10);
    const end = partialend ? parseInt(partialend, 10) : total - 1;
    const chunksize = (end - start) + 1;

    res.writeHead(206, {
      'Content-Range': 'bytes ' + start + '-' + end + '/' + total,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mp4'
    });

    const stream = file.createReadStream({ start: start, end: end });
    stream.pipe(res);
    
    req.on('close', () => {
      stream.destroy();
    });
  } else {
    res.writeHead(200, {
      'Content-Length': total,
      'Content-Type': 'video/mp4'
    });
    const stream = file.createReadStream();
    stream.pipe(res);
    
    req.on('close', () => {
      stream.destroy();
    });
  }
}

// API thống kê
app.get('/stats', (req, res) => {
  const stats = Object.keys(engines).map(hash => {
    const eng = engines[hash];
    return {
      infoHash: hash,
      downloadSpeed: eng.swarm ? eng.swarm.downloadSpeed() : 0,
      uploadSpeed: eng.swarm ? eng.swarm.uploadSpeed() : 0,
      peers: eng.swarm ? eng.swarm.wires.length : 0,
      downloaded: eng.swarm ? eng.swarm.downloaded : 0
    };
  });
  
  const totalDownloadSpeed = stats.reduce((acc, curr) => acc + curr.downloadSpeed, 0);
  const totalUploadSpeed = stats.reduce((acc, curr) => acc + curr.uploadSpeed, 0);

  res.json({
    totalDownloadSpeed,
    totalUploadSpeed,
    torrents: stats
  });
});

const PORT = 11470;
app.listen(PORT, '127.0.0.1', () => {
  console.log(`Custom Torrent-Stream Server running at http://127.0.0.1:${PORT}`);
});
