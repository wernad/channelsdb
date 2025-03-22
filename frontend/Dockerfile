FROM node:20-slim AS frontend
RUN mkdir -p build
WORKDIR /build

COPY frontend/package.json frontend/package-lock.json /build/

RUN npm install

COPY . /build

RUN npx tsc -p ./frontend/tsconfig.json
RUN ls -la /build

FROM node:20-slim AS results

WORKDIR /build

COPY ../results/package.json ../results/package-lock.json /build/

RUN npm install

COPY ../results /build

RUN npm run build

FROM nginx:1.26-alpine-slim

COPY --from=frontend /build/assets /var/www/assets

COPY --from=frontend /build/*.html /var/www/

COPY --from=results /build/dist/ChannelsDB /var/www/detail

CMD ["nginx", "-g", "daemon off;"]
