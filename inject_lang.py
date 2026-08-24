import json, re

# ---- All Easter Egg data ----
vi_data = {
  "easter_universal": [
    "B\u1eadt \u0111i\u1ec1u h\u00f2a, \u0111\u1eafp ch\u0103n v\u00e0 th\u01b0\u1edfng th\u1ee9c th\u00f4i!",
    "Ph\u1ea1 b\u1eafp rang, r\u00f3t n\u01b0\u1edbc v\u00e0 chu\u1ea9n b\u1ecb \u0111\u1eafm ch\u00ecm v\u00e0o phim nh\u00e9!",
    "L\u00ean k\u00e8o b\u1eafp n\u01b0\u1edbc ngay v\u00e0 lu\u00f4n!",
    "\u0110\u00e3 t\u1edbi gi\u1edd xem phim r\u1ed3i, kh\u00f4ng ph\u1ea3i gi\u1edd l\u00e0m vi\u1ec7c!",
    "Phim hay \u0111\u1ee3i b\u1ea1n \u0111\u1ea5y, t\u1eaft m\u1ecd s\u0111t \u0111i v\u00e0 t\u1eadp trung n\u00e0o!",
    "Chu\u1ea9n b\u1ecb kh\u0103n gi\u1ea5y phong khi\u1ebfn c\u1ea3m x\u00fac b\u1ecb cu\u1ed1n theo phim nh\u00e9!",
    "R\u1ea1p chi\u1ebfu phim t\u01b0 gia \u0111\u00e3 s\u1eb5n s\u00e0ng, ch\u1ec9 c\u00f2n thi\u1ebfu b\u1ea1n th\u00f4i!",
    "T\u1eaft h\u1ebft th\u00f4ng b\u00e1o r\u00e1c, phim n\u00e0y x\u1ee9ng \u0111\u00e1ng c\u00f3 s\u1ef1 ch\u00fa \u00fd to\u00e0n ph\u1ea7n!",
    "G\u1ecdi h\u1ed9i b\u1ea1n \u0111\u1ebfn xem chung cho vui n\u00e0o!",
    "Ng\u00e0y h\u00f4m nay bi\u1ebft l\u00e0m g\u00ec ch\u01b0a? Xem phim th\u00f4i!"
  ],
  "easter_universal_midnight": [
    "Khuya r\u1ed3i, t\u1eaft m\u00e1y \u0111i ng\u1ee7 \u0111\u1ec3 b\u1ea3o v\u1ec7 s\u1ee9c kh\u1ecfe nh\u00e9! \ud83d\udecf\ufe0f",
    "Th\u1ee9c \u0111\u00eam h\u00f3i \u0111\u1ea7u \u0111\u1ea5y b\u1ea1n \u01a1i, \u0111i ng\u1ee7 l\u1eb9!",
    "Phim hay nh\u01b0ng s\u1ee9c kh\u1ecfe quan tr\u1ecdng h\u01a1n nha!",
    "M\u1eaft \u0111ang m\u1edd r\u1ed3i, mai xem ti\u1ebfp c\u0169ng kh\u00f4ng mu\u1ed9n!",
    "\u0110\u1ed3ng h\u1ed3 b\u00e1o s\u00e1ng v\u1eabn c\u00f2n \u0111\u00f3, li\u1ec7u h\u1ed3n r\u1ed3i ng\u1ee7 \u0111i!",
    "Admin c\u0169ng \u0111\u00e3 ng\u1ee7, b\u1ea1n c\u0169ng n\u00ean ng\u1ee7 th\u00f4i!",
    "Ph\u1ea1 phim v\u00e0o b\u1ed3 nh\u1edb \u0111i, s\u00e1ng mai tho\u1ea3i m\u00e1i coi ti\u1ebfp!",
    "Khuya r\u1ed3i \u0111\u00f3 nh\u00e9, c\u01a1 th\u1ec3 c\u1ea7n ngh\u1ec9 ng\u01a1i 8 ti\u1ebfng m\u1ed7i ng\u00e0y!"
  ],
  "easter_genre_action": [
    "Kh\u00f3i l\u1eeda m\u1ecf m\u1ecf, chu\u1ea9n b\u1ecb tinh th\u1ea7n! \ud83d\udca5",
    "\u0110\u00e1nh \u0111\u1ea5m n\u1ea3y l\u1eeda, c\u0103ng c\u1ef1c c\u0103ng c\u1ef1c!",
    "Ph\u00e1t s\u00fang \u00e2m thanh n\u1ed5i \u0111\u1ec3 c\u1ea3m nh\u1eadn \u0111\u1eb9 nh\u00e9!",
    "B\u00e1m gh\u1ebf, c\u1ea3nh h\u00e0nh \u0111\u1ed9ng ngay s\u1eafp n\u1ed5 t\u01b0ng!",
    "Anh h\u00f9ng \u0111\u00e3 s\u1eb5n s\u00e0ng, ch\u1ec9 ch\u1edd b\u1ea1n m\u1edf phim!",
    "Xe ph\u00f3ng, s\u00fang n\u1ea5p, phi v\u1ee5 b\u1eaft \u0111\u1ea7u!",
    "Xem m\u00e0 \u0111\u1ee7ng h\u00f4 h\u00e1o ph\u1ea3i tr\u1eadn th\u1ea5t kh\u01b0!",
    "C\u1ea3nh chi\u1ebfn n\u00e0y tri\u1ec7u \u0111\u00f4 m\u1edbi d\u1ef1ng n\u1ed5i, tr\u00e2n tr\u1ecdng m\u00e0 xem nh\u00e9!"
  ],
  "easter_genre_romance": [
    "Chu\u1ea9n b\u1ecb kh\u0103n gi\u1ea5y \u0111i, c\u1ea9u l\u01b0\u01a1ng ng\u1eadp m\u1eb7t! \ud83e\udd70",
    "T\u00ecnh y\u00eau m\u00e0u h\u1ed3ng m\u1ed9ng m\u01a1, \u0111\u00e1ng y\u00eau l\u1eafm!",
    "Ng\u1ecdt l\u1ecbm tim, \u0111\u01b0\u1ee3ng \u0111\u1eb9 v\u00e3i ch\u1ee9!",
    "H\u00e0nh tr\u00ecnh t\u00ecnh y\u00eau c\u1ee7a 2 nh\u00e2n v\u1eadt n\u00e0y \u0111ang ch\u1edd b\u1ea1n ch\u1ee9ng ki\u1ebfn!",
    "\u0110\u1ea9y thuy\u1ec1n, \u0111\u1ea9y thuy\u1ec1n, \u0111\u1ea9y cho m\u1ea1nh v\u00e0o!",
    "Coi phim t\u00ecnh c\u1ea3m nh\u1edb \u0111\u00f9ng g\u1ecdi b\u1ea1n trai/g\u00e1i \u0111ang xem nh\u00e9!",
    "Phim n\u00e0y \u0111em ra ng\u00e0y Valentine xem ch\u1ea9n lu\u00f4n!",
    "Hy v\u1ecdng b\u1ea1n c\u0169ng c\u00f3 ai \u0111\u00f3 ng\u1ed3i c\u1ea1nh xem c\u00f9ng \u2665"
  ],
  "easter_genre_comedy": [
    "C\u01b0\u1eddi s\u00e1i qu\u00e0i h\u00e0m! \ud83d\ude02",
    "Kh\u00f4ng n\u00ean xem l\u00fac \u0111ang nhai c\u01a1m!",
    "Gi\u1ea3i tr\u00ed c\u1ef1c m\u1ea1nh, \u0111\u1ed9 h\u00e0i \u0111\u1ea3m b\u1ea3o!",
    "Ph\u00f2ng kh\u00e1ch s\u1eafp v\u1eadng ti\u1ebfng c\u01b0\u1eddi r\u1ed3i \u0111\u00f3!",
    "L\u00e2u r\u1ed3i m\u1edbi c\u00f3 b\u1ed9 phim h\u00e0i \u0111\u1ec9nh nh\u01b0 v\u1eady!",
    "C\u00f3 nh\u1eefng lo\u1ea1i ph\u00f9 th\u1ee7y khi\u1ebfn b\u1ea1n c\u01b0\u1eddi, \u0111\u00f3 ch\u00ednh l\u00e0 \u0111\u1ea1o di\u1ec5n phim n\u00e0y!",
    "\u0110\u1ea5u nh\u1ecb v\u1eadng ti\u1ebfng c\u01b0\u1eddi l\u01b0u \u00fd h\u00e0ng x\u00f3m \u0111\u00f3!",
    "Xem phim n\u00e0y c\u1ea7m b\u1ea3m \u0111\u1ea3m b\u1ea3o mood t\u1ed1t c\u1ea3 tu\u1ea7n!"
  ],
  "easter_genre_historical": [
    "Th\u00e2m cung b\u00ed s\u1eed, xuy\u00ean kh\u00f4ng th\u00f4i!",
    "Cung \u0111\u1ea5u c\u0103ng th\u1eb3ng, ai s\u1ebd th\u1eafng \u0111\u00e2y?",
    "Ph\u1ee5c d\u1ef1ng l\u1ecbch s\u1eed t\u1edbn h\u00e0ng t\u1ef7, nh\u1eefng m\u00e0u s\u1eafc \u0111\u1eb9 lu\u00f4n!",
    "\u00c1o qu\u1ea7n c\u1ed5 trang \u0111\u1eb9 m\u1eaft l\u1eafm, xem m\u00e0 m\u00ea!",
    "B\u1ech \u1ea9n cung \u0111\u00ecnh m\u1edbt ng\u01b0\u1eddi ch\u1ea3 bi\u1ebft, t\u1ef1 xem m\u00e0 c\u1ea3m nh\u1eabn!",
    "Trinh \u0111\u00ecnh v\u01b0\u01a1ng gi\u1ea3 l\u1ea1i b\u1eaft \u0111\u1ea7u, l\u01b0u \u00fd gi\u1eef n\u1eef tinh n\u1ed9!",
    "H\u1ea1u cung tam thi\u00ean m\u1ef9 n\u1eef, ai s\u1ebd gi\u00e0nh chi\u1ebfn th\u1eafng cu\u1ed1i c\u00f9ng?"
  ],
  "easter_genre_psychological": [
    "Plot twist l\u1eadt b\u00e0n, nh\u1edb \u0111\u1ed9i m\u0169 b\u1ea3o hi\u1ec3m! \ud83e\udde0",
    "Sang ch\u1ea5n t\u00e2m l\u00fd c\u1ef1c m\u1ea1nh, c\u1ea7n h\u1ed3i ph\u1ee5c ch\u01b0a?",
    "Hack n\u00e3o c\u1ef1c m\u1ea1nh, ai c\u0169ng b\u1ecb l\u1eeba!",
    "Xem phim n\u00e0y xong s\u1ebd kh\u00f3 ng\u1ee7 v\u00ec c\u1ee9 ngh\u0129 m\u00e3i!",
    "T\u00e2m l\u00fd ph\u00fcc t\u1ea1p, nh\u01b0ng r\u1ea5t th\u1ea3 m\u00e3n khi hi\u1ec3u ra!",
    "Nh\u00e2n v\u1eadt n\u00e0y th\u1eadt s\u1ef1 l\u00e0 ai? B\u1ea1n c\u00f3 bi\u1ebft kh\u00f4ng?",
    "Phim t\u00e2m l\u00fd lu\u00f4n c\u00f3 th\u1ee9 g\u00ec \u1ea9n gi\u1ea5u ph\u00eda sau, tin t\u00f4i \u0111i!"
  ],
  "easter_genre_crime": [
    "S\u1ef1 th\u1eadt ch\u1ec9 c\u00f3 m\u1ed9t! Ph\u00e1 \u00e1n th\u00f4i!",
    "C\u1ea3nh s\u00e1t t\u1edbi \u0111\u00e2y, gi\u01a1 tay l\u00ean!",
    "\u0110\u1ea5u tr\u00ed c\u0103ng n\u00e3o, ai l\u00e0 hung th\u1ee7?",
    "L\u00e0m th\u00e1m t\u1eed m\u1ed9t ng\u00e0y, b\u1eaft t\u1ed9i ph\u1ea1m m\u1ed9t gi\u1edd!",
    "Phim h\u00ecnh s\u1ef1 hay nh\u01b0 n\u00e0y hi\u1ebfm l\u1eafm \u0111\u00f3!",
    "L\u1ed1i \u0111i c\u1ee7a k\u1ebb \u1ea5c \u0111\u00e3 l\u1ed9 ra r\u1ed3i, ch\u1ec9 c\u1ea7n t\u00ecm b\u1eb1ng ch\u1ee9ng th\u00f4i!",
    "Phim h\u00ecnh s\u1ef1 kh\u00f4ng bao gi\u1edd c\u0169, ch\u1ec9 c\u00f3 ng\u01b0\u1eddi xem c\u0169 th\u00f4i!"
  ],
  "easter_genre_scifi": [
    "C\u00e1nh c\u1ed5ng v\u0169 tr\u1ee5 \u0111\u00e3 m\u1edf! \ud83d\ude80",
    "Robot x\u00e2m l\u0103ng hay con ng\u01b0\u1eddi x\u00e2m l\u0103ng Robot?",
    "Du h\u00e0nh th\u1eddi gian ph\u1ee9c t\u1ea1p l\u1eafm, kh\u00f4ng ph\u1ea3i mu\u1ed1n tr\u1edf v\u1ec1 qu\u00e1 kh\u1ee9 l\u00e0 \u0111\u01b0\u1ee3c!",
    "Tr\u00ed tu\u1ec7 nh\u00e2n t\u1ea1o c\u00f3 c\u1ea3m x\u00fac th\u00ec sao... Xem phim n\u00e0y \u0111\u1ec3 bi\u1ebft!",
    "C\u00f4ng ngh\u1ec7 l\u00f5i l\u00e0 \u0111\u00e2y, khoa h\u1ecdc \u0111i tr\u01b0\u1edbc 100 n\u0103m!",
    "Ng\u01b0\u1eddi ngo\u00e0i h\u00e0nh tinh c\u00f3 l\u1edbp l\u1edb h\u01a1n ch\u00fang ta kh\u00f4ng?",
    "Phim vi\u1ec5n t\u01b0\u1edfng g\u1ecdi th\u1ee9c l\u00f2ng \u01b0\u1edbm m\u01a1 kh\u00e1m ph\u00e1 v\u0169 tr\u1ee5 trong b\u1ea1n!"
  ],
  "easter_genre_horror": [
    "\u0110\u1eebng nh\u00ecn ra sau l\u01b0ng... \ud83d\udc7b",
    "Ma t\u1edbi k\u00eca!",
    "Xem \u0111\u00eam nh\u1edb ch\u00f9m m\u1ec1n k\u00edn nh\u00e9!",
    "Jump scare \u0111\u1ea7u ti\u00ean \u0111\u1ebfn l\u00fac n\u00e0o, ch\u00fa \u00fd nh\u00e9!",
    "\u00c2m thanh t\u1eadp trung g\u00e2y \u1ee9ng l\u1eafm, nh\u1edb m\u1edf to l\u00ean!",
    "Phim n\u00e0y xem m\u00e0 c\u1eeda nh\u00e0 kh\u00f3a ch\u01b0a?",
    "Nh\u00e2n v\u1eadt n\u00e0y s\u1eafp ch\u1ebft r\u1ed3i, ai c\u0169ng bi\u1ebft nh\u01b0ng cu\u1ed1i cu\u1ed9c xem ti\u1ebfp!",
    "Ban \u0111\u00eam m\u00e0 v\u00e0o nh\u00e0 b\u1ecf kh\u00f4ng \u0111\u01b0\u1ee3c ngh\u0129 t\u1edbi phim n\u00e0y l\u00e0m g\u00ec!"
  ],
  "easter_genre_animation": [
    "V\u1ec1 l\u1ea1i tu\u1ed5i th\u01a1 n\u00e0o! \ud83c\udf08",
    "Th\u1ebf gi\u1edbi di\u1ec7u k\u1ef3 \u0111ang ch\u1edd \u0111\u00f3n!",
    "Hoat hinh kh\u00f4ng ch\u1ec9 d\u00e0nh cho tr\u1ebb em \u0111\u00e2u nh\u00e9!",
    "\u1ea2nh s\u00e1ng m\u00e0u s\u1eafc d\u1ec7 th\u01b0\u01a1ng l\u1eafm, d\u1eef li\u1ec7u tay ngh\u00e8 l\u00e0m r\u00f5!",
    "Nh\u00e2n v\u1eadt ho\u1ea1t h\u00ecnh lu\u00f4n c\u00f3 b\u00e0i h\u1ecdc \u00fd ngh\u0129a sau m\u1ed7i c\u00e2u chuy\u1ec7n!",
    "Studio \u1ea3o di\u1ec7u v\u00e0 c\u00f4ng s\u1ee9c t\u1ea1o ra t\u1eebng khung h\u00ecnh \u0111\u1ea9y l\u00e0 phi\u1ec7t!",
    "K\u1ef3 l\u00e2n, r\u1ed3ng v\u00e0 c\u1ea7u v\u1ed3ng \u0111ang ch\u1edd b\u1ea1n kh\u00e1m ph\u00e1!"
  ],
  "easter_genre_lgbt": [
    "Love is love! \ud83c\udff3\ufe0f\u200d\ud83c\udf08",
    "Ng\u1ecdt ng\u00e0o qu\u00e1, \u0111\u1ea9y thuy\u1ec1n th\u00f4i!",
    "C\u1ea7u v\u1ed3ng r\u1ef1c r\u1ee1, t\u00ecnh y\u00eau kh\u00f4ng c\u00f3 gi\u1edbi h\u1ea1n!",
    "BL/GL, ch\u1ec9 bi\u1ebft l\u00e0 ngon!",
    "Hai anh/ch\u1ecb \u0111\u00e0o hoa th\u1ebf n\u00e0y kh\u00f3 c\u01b0\u1ee1ng qu\u00e1!",
    "Fan ship b\u00e0y r\u1ed3i, n\u00e0o t\u1ea5t c\u1ea3 c\u00f9ng loa!",
    "Phim n\u00e0y l\u00e0m t\u00f4i tin v\u00e0o t\u00ecnh y\u00eau c\u01a1!",
    "M\u00e0u c\u1ea7u v\u1ed3ng \u0111\u1eb9 qu\u00e1, nh\u01b0 phim n\u00e0y v\u1eady!"
  ],
  "easter_progress_party": [
    "T\u1eadp m\u1edbi v\u1eeba th\u1ed5i v\u1eeba x\u01a1i ngay n\u00e0o! \ud83d\udd25",
    "\u0110\u1ee3i m\u00e3i m\u1edbi ra, c\u00e0y l\u1eb9 k\u1ebb b\u1ecb spoil!",
    "Admin \u0111\u00e3 upload xong, c\u00f2n \u0111\u1ee3i g\u00ec n\u1eefa?",
    "T\u1eadp m\u1edbi n\u00f3ng h\u1ed5i! Nhanh v\u00e0o xem \u0111i!",
    "Th\u1ee9c \u0111\u1ee3i m\u00e0y t\u1eadp m\u1edbi, cu\u1ed1i c\u00f9ng ra r\u1ed3i!",
    "\u0102n m\u1eebng n\u00e0o, t\u1eadp m\u1edbi \u0111\u00e3 c\u00f3 r\u1ed3i!"
  ],
  "easter_progress_cry": [
    "Ch\u01b0a g\u00ec \u0111\u00e3 h\u1ebft phim... \ud83d\ude2d",
    "S\u1ebd nh\u1edb c\u00e1c nh\u00e2n v\u1eadt l\u1eafm \u0111\u00e2y!",
    "T\u1ea1m bi\u1ec7t b\u1ed9 phim tuy\u1ec7t v\u1eddi, \u0111\u00e3 \u0111\u1ed3ng h\u00e0nh c\u00f9ng nhau m\u1ed9t h\u1ed3i!",
    "Chia tay nh\u00e2n v\u1eadt th\u1eadt s\u1ef1 l\u01b0u luy\u1ebfn!",
    "Xem xong v\u1ea5n kh\u00f4ng d\u1ee9t ra \u0111\u01b0\u1ee3c... Phim hay th\u1eadt!",
    "Mong r\u1eb1ng s\u1ebd c\u00f3 m\u00f9a ti\u1ebfp theo..."
  ],
  "easter_progress_rage": [
    "\u0110ang h\u1ed1i Admin v\u1eaft gi\u00f2 l\u00ean c\u1ed5 Mux! Ch\u1edd x\u00edu nh\u00e9!",
    "Admin \u0111ang b\u1eadn pha m\u00ec t\u00f4m, t\u1eeb t\u1eeb upload phim!",
    "Ph\u1ea7n m\u1ec1m Mux \u0111ang render, kiên nh\u1eabn ch\u00fat nh\u00e9!",
    "T\u1eadp m\u1edbi \u0111\u00e3 l\u00ean s\u00f3ng TV nh\u01b0ng App ch\u01b0a c\u1eadp nh\u1eadt, c\u1ed1 ch\u1edd m\u1ed9t ch\u00fat!",
    "H\u00e3y ki\u00ean nh\u1eabn! Admin \u0111ang l\u00e0m vi\u1ec7c!",
    "C\u01a1n gi\u1eadn qua \u0111i, phim s\u1eafp c\u00f3 r\u1ed3i!"
  ],
  "easter_progress_chill": [
    "Ch\u1eb7ng \u0111\u01b0\u1eddng c\u00f2n d\u00e0i, c\u1ee9 th\u00f4ng th\u1ea3 chill v\u00e0 t\u1eadn h\u01b0\u1edfng nh\u00e9 \ud83e\udd64",
    "Ph\u00f9 thay! Phim nhi\u1ec1u t\u1eadp \u0111\u1ea3m b\u1ea3o gi\u1ea3i tr\u00ed d\u00e0i d\u00e0i!",
    "C\u00f3 nhi\u1ec1u th\u1eddi gian, h\u00e3y h\u01b0\u1edfng th\u1ee9 t\u1eebng t\u1eadp th\u1eadt ch\u1eadm!",
    "Ph\u1ea7n m\u1edf \u0111\u1ea7u l\u00f4i cu\u1ed1n, c\u00e0ng v\u1ec1 cu\u1ed1i c\u00e0ng h\u1ea5p d\u1eabn h\u01a1n!",
    "Kh\u00f4ng c\u1ea7n v\u1ed9i, phim v\u1eabn c\u00f2n \u0111\u00f3 ch\u1ee9 kh\u00f4ng m\u1ea5t!"
  ],
  "easter_progress_tense": [
    "Drama \u0111ang c\u0103ng, h\u1ed3i h\u1ed9p ch\u1edd xem tu\u1ea7n sau gi\u1ea3i quy\u1ebft \u00e2n o\u00e1n th\u1ebf n\u00e0o! \ud83d\ude31",
    "G\u1ea7n cu\u1ed1i r\u1ed3i, t\u1ea5t c\u1ea3 s\u1eafp \u0111\u01b0\u1ee3c h\u00e9 l\u1ed9!",
    "N\u00fat th\u1eaft \u0111ang t\u1edbi \u0111i\u1ec3m g\u00e1o, kh\u00f4ng th\u1ec3 b\u1ecf l\u1ee1 ph\u1ea7n n\u00e0y!",
    "C\u1eafn m\u00f3ng tay h\u1ed3i h\u1ed9p xem ai th\u1eafng ai!",
    "Ai s\u1ebd s\u1ed1ng s\u00f3t \u0111\u1ebfn cu\u1ed1i phim \u0111\u00e2y?",
    "Plot twist ch\u01b0a ra h\u1ebft, c\u00f2n nhi\u1ec1u m\u00f3n ng\u1ea7u \u0111ang \u0111\u1ee3i b\u1ea1n!"
  ]
}

en_data = {
  "easter_universal": [
    "Popcorn ready? Let's go!", "Turn off notifications and enjoy the film!", "Cinema mode activated at home!",
    "Grab your snacks, the show is about to begin!", "Perfect time to watch something great!", "Lights off, volume up!",
    "Your couch is calling you!", "This is the moment you've been waiting for!", "Invite friends or enjoy solo!",
    "Today's best plan: watch this movie!"
  ],
  "easter_universal_midnight": [
    "It's late, protect your health and sleep! \ud83d\udecf\ufe0f", "Eyes drooping? Time to stop and rest!",
    "The movie will still be there tomorrow, get some sleep!", "Your alarm clock is still set, be careful!",
    "Even the admin is sleeping now, you should too!", "Save the episode for morning, rest well!",
    "Your body needs 8 hours of sleep every night!"
  ],
  "easter_genre_action": [
    "Smoke and fire incoming, brace yourself! \ud83d\udca5", "Epic fight scenes ahead!", "Turn up the surround sound for this one!",
    "Hold on to your seat, it's about to explode!", "The hero is ready, just press play!", "Cars, guns, mission starts now!",
    "This scene cost millions to make, appreciate it!", "Action overload incoming!"
  ],
  "easter_genre_romance": [
    "Grab your tissues, the sweetness is overwhelming! \ud83e\udd70", "Love is in the air!", "Heart fluttering guaranteed!",
    "This couple's journey is yours to witness!", "Ship them hard, ship them loud!", "Don't watch this on a first date, too much pressure!",
    "Perfect Valentine's Day movie!", "Hope you have someone to watch this with \u2665"
  ],
  "easter_genre_comedy": [
    "Prepare to laugh your head off! \ud83d\ude02", "Don't watch while eating, you might choke!", "Maximum entertainment mode on!",
    "Your room is about to fill with laughter!", "Rare comedy gem right here!", "Good vibes all week guaranteed!",
    "Laughter is the best medicine, enjoy!"
  ],
  "easter_genre_historical": [
    "Ancient secrets and palace drama await!", "Time to travel back in history!", "Epic historical costumes incoming!",
    "Who will survive the palace politics?", "The court drama is about to unfold!",
    "Thousands spent on costumes, appreciate every frame!", "Ancient rivalries, modern feelings!"
  ],
  "easter_genre_psychological": [
    "Plot twist incoming, wear your helmet! \ud83e\udde0", "Your mind will be blown!", "This film will have you thinking for days!",
    "Who is this character really? Find out!", "Psychology this complex is deeply satisfying!",
    "Every frame hides a clue, pay attention!", "Don't trust anyone in this movie!"
  ],
  "easter_genre_crime": [
    "The truth is singular! Solve the case!", "Hands up, detective mode activated!", "Who's the real culprit? Brain engaged!",
    "One day as a detective, catching criminals in an hour!", "Rare quality crime thriller right here!",
    "The villain's trail has been exposed, find the evidence!", "Crime films never get old, only viewers do!"
  ],
  "easter_genre_scifi": [
    "The gates of the universe are open! \ud83d\ude80", "Robots invading or humans invading robots?",
    "Time travel is complicated, trust me!", "What if AI had feelings? Watch this to find out!",
    "Technology 100 years ahead, right here!", "Are aliens smarter than us?", "Sci-fi awakens the explorer in you!"
  ],
  "easter_genre_horror": [
    "Don't look behind you... \ud83d\udc7b", "Ghost incoming!", "Watch at night with blanket ready!",
    "When is the first jump scare? Stay alert!", "Surround sound is terrifying for this one!",
    "Is your door locked? Just checking!", "We all know this character is about to die, yet we keep watching!",
    "Don't think of this movie when coming home after dark!"
  ],
  "easter_genre_animation": [
    "Back to childhood magic! \ud83c\udf08", "A wonderful world awaits!", "Animation is not just for kids!",
    "Every frame hand-crafted with love!", "Animated characters always have life lessons!", "The artistry is incredible!",
    "Unicorns, dragons and rainbows are waiting!"
  ],
  "easter_genre_lgbt": [
    "Love is love! \ud83c\udff3\ufe0f\u200d\ud83c\udf08", "Sweet and heartwarming, sail the ship!", "Rainbow colors, love without limits!",
    "BL/GL, just pure good content!", "These two are just too adorable!", "Shippers unite!",
    "This film makes me believe in love!", "Beautiful as a rainbow, just like this film!"
  ],
  "easter_progress_party": [
    "New episode hot off the press! \ud83d\udd25", "Finally out! Watch before spoilers hit!",
    "Admin uploaded, what are you waiting for?", "New episode sizzling hot, dive in now!",
    "Stayed up waiting, finally arrived!", "Celebration time, new episode is here!"
  ],
  "easter_progress_cry": [
    "It's over already... \ud83d\ude2d", "Will miss these characters so much!",
    "Farewell to an amazing series, it's been a journey!", "Saying goodbye to these characters is bittersweet!",
    "Can't shake this feeling after watching... it was that good!", "Hoping for another season..."
  ],
  "easter_progress_rage": [
    "Nagging admin to upload! Please wait!", "Admin is busy making instant noodles, film coming soon!",
    "Rendering software is processing, be patient!", "Episode aired on TV but app not updated yet, hang tight!",
    "Have patience! Admin is working on it!", "Anger passes, the film will be ready!"
  ],
  "easter_progress_chill": [
    "Long journey ahead, take it easy and enjoy! \ud83e\udd64", "Many episodes means long entertainment!",
    "Plenty of time, savor each episode slowly!", "Great opening, gets even better towards the end!",
    "No rush, the film isn't going anywhere!"
  ],
  "easter_progress_tense": [
    "Drama escalating, anxiously waiting for next week's resolution! \ud83d\ude31",
    "Near the end, everything is about to be revealed!", "The climax is here, can't miss this part!",
    "Biting nails waiting to see who wins!", "Who will survive until the finale?",
    "More plot twists coming, there's still more in store!"
  ]
}

# Read both files
with open("assets/langs/vi.json", "r", encoding="utf-8") as f:
    vi_orig = json.load(f)
with open("assets/langs/en.json", "r", encoding="utf-8") as f:
    en_orig = json.load(f)

vi_orig.update(vi_data)
en_orig.update(en_data)

with open("assets/langs/vi.json", "w", encoding="utf-8") as f:
    json.dump(vi_orig, f, ensure_ascii=False, indent=2)
with open("assets/langs/en.json", "w", encoding="utf-8") as f:
    json.dump(en_orig, f, ensure_ascii=False, indent=2)

print("Done injecting Easter Egg strings into both language files.")
