git init -q -b main repo
cd repo
git config user.name "Hoc Vien"
git config user.email "hv@example.com"
echo "ao 10" > kho.txt
git add kho.txt
git commit -q -m "tao kho"
echo "non 5" >> kho.txt
git commit -q -am "them non"
sed -i 's/ao 10/ao 12/' kho.txt
git commit -q -am "sua so luong ao"
git log --format=%s
git branch --show-current
git rev-list --count HEAD
