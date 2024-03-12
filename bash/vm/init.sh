#! /usr/bin/bash
# Version 1.0

domain_name='example.com'
email_address='me@example.com'

# Update
apt update && apt upgrade -y

# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - &&\
apt-get install -y nodejs

# Install PM2
npm i pm2@latest -g

# Install Nginx
apt install nginx -y

# Custom Nginx config
cat << EOF > /etc/nginx/sites-available/default
server {
  listen 80 default_server;
  listen [::]:80 default_server;
  server_name $domain_name, www.$domain_name;
  
  index index.html index.htm index.nginx-debian.html;
  root /var/www/html/build;

  location /api {
    proxy_pass http://localhost:5000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade \$http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host \$host;
    proxy_cache_bypass \$http_upgrade;
  }

  location / {
    try_files \$uri \$uri/ =404;
  }
}
EOF

# Add main user to nginx user group
usermod -aG www-data ubuntu

# Change web dir to nginx user/group
sudo chown www-data:www-data /var/www/html

# Give group write permissions on web dir
chmod -R g+w /var/www/html


# Install certbot
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
nginx -t
systemctl reload nginx

# Run certbot
certbot  --noninteractive --agree-tos  --no-eff-email  --cert-name domain.com --nginx --no-redirect  -d $domain_name -d www.$domain_name -m $email_address

# Generate SSH key
ssh-keygen -t ed25519 -C $email_address -q -f "/home/ubuntu/.ssh/id_ed25519" -N ""

# Make app folder
cd ~
mkdir app