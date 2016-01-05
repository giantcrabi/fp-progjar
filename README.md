# FP Pemrograman Jaringan "Catapult War"

- Ide diinspirasi oleh game Battleship jaman dahulu

- Game ini dimainkan oleh 2 player secara bergiliran

- Cara bermain:
  1. Setiap player mempunyai 5 benteng
  2. Kelima benteng tersebut diletakkan di area game seluas 15x15 petak, satu benteng menempati satu petak
  3. Area game pemain dan lawan ditukar, namun lawan tidak dapat melihat letak benteng kita, begitu juga sebaliknya
  4. Player memilih 1 petak sebanyak 3x pada saat gilirannya(luas petak yang dapat dipilih
     dapat berubah sesuai power-up) untuk ditembak
  5. Jika petak yang dipilih ternyata ditempati oleh benteng lawan, maka benteng lawan akan hancur
  6. Selain itu terdapat item power-up yang tersebar di area game(secara tersembunyi), jika player memilih
     petak yang terdapat item power-up, maka catapult player tersebut akan mendapatkan power-up pada tembakan selanjutnya
  7. Player yang dapat menghancukan kelima benteng lawan terlebih dahulu adalah pemenangnya

- Power-up:
  1. Firebomb: luas tembakan catapult bertambah 4 petak(kiri, kanan, atas, bawah dari petak yang dipilih) sekali tembak
  2. Crossbomb: luas tembakan catapult bertambah 4 petak(setiap diagonal bertambah 1 petak dari petak yang dipilih) sekali tembak
  3. Napalm: luas tembakan catapult bertambah 8 petak(setiap petak di samping petak yang dipilih bertambah 1 petak membentuk persegi) sekali tembak
  4. Guillotine: luas tembakan catapult seluas satu area horizontal(15 petak) dari area game dalam sekali tembak
  5. Rocket: luas tembakan catapult seluas satu area vertikal(15 petak) dari area game dalam sekali tembak

