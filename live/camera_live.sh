#mkdir /tmp/stream
#raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0
raspistill --nopreview -w 1296 -h 730 -q 5 -o /var/ramfs/pic.jpg -tl 5 -t 9999999 --thumb none
