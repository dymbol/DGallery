#uwsgi --chdir=/home/dymbol/git/GoPG/DymbolGallery --module=DymbolGallery.wsgi:photos --env DJANGO_SETTINGS_MODULE=DymbolGallery.settings --master --pidfile=/tmp/project-master.pid --http-socket=127.0.0.1:49152   --processes=5    --harakiri=20  --max-requests=5000 --daemonize=yourproject.log  
uwsgi --http 192.168.122.124:8000 --chdir /opt/GoPG/DymbolGallery  --wsgi-file DymbolGallery.wsgi --master --processes 1 --workers 1 --threads 1 --daemonize=/opt/GoPG_conf/bdg.log  --static-map /static=/opt/GoPG/DymbolGallery/photos/static --pidfile /opt/GoPG_conf/bdg.pid 

