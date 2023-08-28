FROM node:latest as frontend

WORKDIR /build

COPY ./frontend/package.json ./frontend/package-lock.json /build/

RUN npm install

COPY ./frontend /build

RUN ./node_modules/.bin/tsc

FROM node:latest as results

WORKDIR /build

COPY ./results/package.json ./results/package-lock.json /build/

RUN npm install

COPY ./results /build

RUN ./node_modules/.bin/gulp

FROM nginx:latest

COPY --from=frontend /build/assets /var/www/assets

COPY --from=frontend /build/*.html /var/www/

COPY --from=results /build/dist/ChannelsDB /var/www/detail

CMD ["nginx", "-g", "daemon off;"]
