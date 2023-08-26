FROM node:latest as frontend

WORKDIR /build

COPY frontend/ /build

RUN npm install

RUN ./node_modules/.bin/tsc

FROM node:latest as results

WORKDIR /build

COPY results /build

RUN npm install

RUN ./node_modules/.bin/gulp

FROM nginx:latest

COPY --from=frontend /build/assets /var/www/assets

COPY --from=frontend /build/*.html /var/www/

COPY --from=results /build/dist/ChannelsDB /var/www/detail

COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
