git --version | cut -d' ' -f1-2
javac -version 2>&1 | cut -d. -f1
python --version | cut -d. -f1
ls . > /dev/null; echo "ls: $?"
ls khong_co 2> /dev/null; echo "ls loi: $?"
echo "so du" > tep.txt
grep -q tien tep.txt; echo "grep: $?"
mkdir tien_ich
echo 'echo xin chao tu tien_ich' > tien_ich/chao_ban
chmod +x tien_ich/chao_ban
PATH="$PWD/tien_ich:$PATH"
chao_ban
