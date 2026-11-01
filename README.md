# LexiUp: file chay web va du phong

## Chay tren GitHub Pages

- Chi can `index.html`. Giao dien, chuc nang hoc va kho tu IELTS deu da nhung trong file nay.
- Khong can Node.js, file JSON hay thu muc `backups/` de nguoi dung mo web.
- Upload file len repository chua tu dong bat GitHub Pages; can cau hinh Pages cho repository neu chua co.
- Font truc tuyen va phuong an am thanh qua mang co the can Internet; web uu tien giong doc cua trinh duyet khi co.

## Cac file du phong moi

- `backups/index.snapshot-2026-11-02.html`: ban sao nguyen ven cua web hien tai.
- `backups/snapshot-2026-11-02.json`: ma SHA-256 va thong ke de doi chieu ban sao HTML va du lieu JSON.
- `data/vocabulary-export.json`: xuat du 2.902 muc tu trong HTML, gom 1.033 muc duoc chon cho kho IELTS (188 B1, 652 B2, 193 C1).

JSON giu nguyen ID, nghia nen tang, vi du, collocation, ho so nghia IELTS rieng va dau chon `metadata.ieltsSelection`. Khong duoc doi ID cua tu da hoc khi chinh sua ve sau. Danh sach JSON la ban xuat de bao tri, khong phai file duoc web tai dong: sua JSON se chua tu cap nhat `index.html`; can dong bo lai noi dung vao HTML.

Co the luu `data/` tren GitHub de du phong nguon; web khong can thu muc nay de chay. `.gitignore` bo qua `backups/` va cache de tranh dua ban HTML du phong len hosting ngoai y muon. Muon du phong chong hong o dia, hay giu them mot ban o noi khac; hai file tren cung may khong phai hai ban sao doc lap.

## Tien do hoc la du lieu rieng

Ban sao HTML va JSON nay KHONG chua tien do, tu tu them hoac cai dat rieng trong trinh duyet. Dung chuc nang xuat sao luu cua web de luu nhung du lieu do. Khi doi dia chi web hoac trinh duyet, can nhap lai file sao luu tien do.

Day la cac file du phong MOI, tao tu phien ban con lai ngay 02/11/2026. Khong phai phuc hoi ban HTML goc, cac bang bien tap, nguon Reading hay script da xoa truoc do.
