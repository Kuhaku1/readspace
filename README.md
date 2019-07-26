# docker 运行指南

docker run -d -p 8000:8080 -v /root/nginx/www/ReadBooks/statics:/app/statics -v /root/nginx/www/ReadBooks/medias:/app/medias -v /root/nginx/www/ReadBooks/logging:/app/logging -e MYSQL_SERVER_ADDRESS=172.31.82.128 -e REDIS_SERVER_ADDRESS=172.31.82.128 readbooks:1.0.1
