FROM nginx

ARG NGINX_CONFIG
WORKDIR /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY ./$NGINX_CONFIG /etc/nginx/conf.d/

EXPOSE 80
EXPOSE 443