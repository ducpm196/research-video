mkdir -p cua_hang/kho cua_hang/bao_cao
touch cua_hang/kho/ao.txt cua_hang/kho/quan.txt cua_hang/kho/non.txt
echo "ao 5" > cua_hang/bao_cao/tong.txt
echo "quan 3" >> cua_hang/bao_cao/tong.txt
cp cua_hang/kho/ao.txt cua_hang/kho/ao_sao.txt
mv cua_hang/kho/non.txt cua_hang/kho/mu.txt
rm cua_hang/kho/quan.txt
find cua_hang | sort
cat cua_hang/bao_cao/tong.txt
