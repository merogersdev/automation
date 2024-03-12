#! /usr/bin/bash
# Version 1.0

# Git pull
git pull origin main

# Cleanup build if exists
if [ -d /var/www/html/build ]; then
  rm -r /var/www/html/build
fi

# Stop all PM2 processes
pm2 stop all

# Frontend install and build
cd ./frontend
npm i
npm run build

# move build to /var/www/html/
mv ./build /var/www/html/

# launch backend with pm2
cd ../backend
npm i
pm2 start server.js --name "Backend"
pm2 save