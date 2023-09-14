#stage 1
FROM node:18 AS build-env
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build --prod

#stage 2
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build-env /app/dist/ai-net /usr/share/nginx/html
