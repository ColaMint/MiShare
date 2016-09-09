server {
    listen          80;
    server_name     www.mi-share.com;
    rewrite_log     on;
    charset         utf8;

    error_log       /var/log/nginx/www.mishare.com.error.log;
    access_log      /var/log/nginx/www.mishare.com.access.log;

    location /{
        include     uwsgi_params;
        proxy_pass  http://127.0.0.1:18888;
    }
}

