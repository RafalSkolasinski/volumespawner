#!/bin/sh

echo "Creating user $USER ($USER_ID)"
useradd -u $USER_ID -s $SHELL jupyter
echo "jupyter:jupyter" | chpasswd && adduser jupyter sudo
sudo -E -u jupyter jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user=$JPY_USER \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL
