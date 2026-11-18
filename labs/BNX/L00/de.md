# Lab BNX L00 — Hai nhánh cùng sửa một dòng lãi suất

Làm trong Git Bash. Viết tệp `lab.sh` (số liệu là số minh hoạ). Bốn dòng đầu cho sẵn, chép nguyên văn: chúng đặt tên người viết rồi chuyển vào một thư mục tạm.

```bash
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=Binh GIT_AUTHOR_EMAIL=binh@vd.vn
export GIT_COMMITTER_NAME=Binh GIT_COMMITTER_EMAIL=binh@vd.vn
cd `mktemp -d`
```

Tiếp theo, bạn viết các lệnh sau:

1. Tạo kho (`git init -q -b main`), tạo tệp `lai.txt` chứa dòng `lai=7`, đưa vào vùng chờ (`git add`) và chốt với lời nhắn `goc` (`git commit -q -m goc`; luôn có `-m`, nếu không Git mở trình soạn thảo và chờ bạn).
2. Tạo nhánh `giam`. Trên nhánh này: sửa `lai.txt` thành `lai=6` rồi chốt; sau đó tạo tệp `ghi_chu.txt` (nội dung tuỳ ý), đưa vào vùng chờ và chốt. Nhánh `giam` có 2 lần chốt riêng.
3. Về nhánh `main`, sửa `lai.txt` thành `lai=8` rồi chốt. Gộp nhánh `giam` vào `main` bằng `git merge giam > /dev/null` (dấu `> /dev/null` giấu thông báo xung đột để đầu ra chỉ còn ba dòng cuối).
4. Giải xung đột: ghi lại `lai.txt` chỉ còn `lai=8` (không còn dấu mốc), đưa vào vùng chờ rồi chốt gộp.
5. Cuối chương trình, in ba dòng bằng ba lệnh sau (cho sẵn, chép nguyên văn):

```bash
cat lai.txt
echo "so commit: $(git rev-list --count HEAD)"
echo "so cha: $(git cat-file -p HEAD | grep -c '^parent')"
```

Chạy: `bash lab.sh`. Chấm: `bash labs/cham.sh BNX L00 lab.sh`.
