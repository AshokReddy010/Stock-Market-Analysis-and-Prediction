FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY public ./public
COPY src ./src
ARG REACT_APP_API_URL=http://localhost:8000
ENV REACT_APP_API_URL=$REACT_APP_API_URL NODE_OPTIONS=--openssl-legacy-provider CI=false
RUN npx react-scripts build

FROM nginx:1.27-alpine
COPY --from=build /app/build /usr/share/nginx/html
# single-page app: unknown paths serve index.html so client-side routes work on refresh
RUN printf 'server {\n  listen 80;\n  root /usr/share/nginx/html;\n  location / { try_files $uri /index.html; }\n}\n' > /etc/nginx/conf.d/default.conf
EXPOSE 80
