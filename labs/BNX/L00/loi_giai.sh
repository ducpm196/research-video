export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=Binh GIT_AUTHOR_EMAIL=binh@vd.vn
export GIT_COMMITTER_NAME=Binh GIT_COMMITTER_EMAIL=binh@vd.vn
cd `mktemp -d`
git init -q -b main
echo "lai=7" > lai.txt
git add lai.txt
git commit -q -m goc
git switch -q -c giam
echo "lai=6" > lai.txt
git commit -q -am "giam lai"
echo "dot giam thang 3" > ghi_chu.txt
git add ghi_chu.txt
git commit -q -m "ghi chu"
git switch -q main
echo "lai=8" > lai.txt
git commit -q -am "tang lai"
git merge giam > /dev/null
echo "lai=8" > lai.txt
git add lai.txt
git commit -q -m "gop giam"
cat lai.txt
echo "so commit: $(git rev-list --count HEAD)"
echo "so cha: $(git cat-file -p HEAD | grep -c '^parent')"
