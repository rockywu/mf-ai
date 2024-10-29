server {
    listen       80 default_server;
    server_name  _ ${APP_DOMAIN};

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;
    autoindex on;
    index index.html index.htm;

    location / {
        root   /www/web/dist;
        index  index.html index.htm;
		try_files $uri $uri/ /index.html;
    }
    
    location /v1 {
        alias   /www/web/build;
        index  index.html index.htm;
        try_files $uri $uri/ /v1/index.html;

    }

    location ~ ^/packscreens.*$ {
        root   /www/web/dist;
        index  packscreen.html;
		try_files $uri $uri/ /packscreen.html;
    }

    location ~ ^/bigscreen.*$ {
        root   /www/web/dist;
        index  bigscreen.html;
		try_files $uri $uri/ /bigscreen.html;
    }

    location ~ ^/pageinfo.*$ {
        root   /www/web/dist;
        index  single.html;
		try_files $uri $uri/ /single.html;
    }

    location ~ ^/api/.*$ {
        rewrite ^/api/(.*)$ /$1 break;
        proxy_pass http://api:3000;
    }

    location ~ ^/PushAlarm/.*$ {
        rewrite ^/PushAlarm/(.*)$ /PushAlarm/$1 break;
        proxy_pass http://api:3000;
    }

    location ~ ^/assets/.*$ {
        root   /code;
        #rewrite ^/(.*)$ /$1 break;
        #proxy_pass http://api:3000;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}

server {
    listen       80;
    server_name  api.${APP_DOMAIN} assets.${APP_DOMAIN};

    location / {
        proxy_pass   http://api:3000/;
    }
}

