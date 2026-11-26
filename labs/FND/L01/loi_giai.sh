mkdir -p vp/kho/a vp/kho/b vp/ho_so
touch vp/kho/a/x.txt vp/kho/b/y.txt vp/kho/b/z.txt vp/ho_so/hd.txt
cd vp/kho/b
echo "buoc 1:"
ls
cd ../../ho_so
echo "buoc 2:"
ls
cd ../kho/a
echo "buoc 3:"
ls
echo "buoc 4:"
ls ..
