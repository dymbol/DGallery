arc=/tmp/DGallery_code.tgz

if [ -e $arc ] ; then
  rm -f $arc
fi

cd /home/dymbol/GIT/DGallery/DymbolGallery
tar -zcvf /tmp/DGallery_code.tgz .
