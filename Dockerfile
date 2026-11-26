FROM nginx:1.27-alpine

# Replace the default site config with ours
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/app.conf

# Only the files the app needs
COPY index.html styles.css questions.js /usr/share/nginx/html/

EXPOSE 80
HEALTHCHECK CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
