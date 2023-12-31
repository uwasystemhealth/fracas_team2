#!/bin/bash
Help()
{
   # Display Help
   echo "Setup script to install and run uwam-fracas in the background & on start-up."
   echo "If required flags aren't provided, script will prompt you to input required details for setup"
   echo
   echo "NOTE: This script was designed for production deployment, on a clean Ubuntu Virtual Machine"
   echo "      and may not work (or break) other setups."
   echo 
   echo "Syntax: setup [-h]"
   echo "options:"
   echo "-h    Print this Help."
}
# Used for yarn builds on low memory
# uncomment to use
# export NODE_OPTIONS=--max_old_space_size=256
# export GENERATE_SOURCEMAP=false
#
# Update & install packages needed for setup
set -e
PARENT_DIRECTORY=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
echo "############################"
echo "Starting UWAM-FRACAS Install"
echo "############################"
echo
echo "NOTE: This script was design and tested to run on Ubuntu or Debian."
echo "      Only requires to be run once and then managed via systemctl."
echo "      restart.sh & stop.sh scripts are also provided."
echo
echo
echo
echo "Ensure your domain is already forwarding to the public IP address of this machine"
read -p "Enter the domain name for the app: " DOMAIN
echo
echo "This system requires an email account to send email for signup and password requests"
read -p "Enter the SMTP server name (e.g. smtp.gmail.com if using gmail): " EMAIL_SERVER
echo
read -p "Enter the email account : " EMAIL_ACCOUNT
echo
read -p "Enter the email password : " EMAIL_PASSWORD
echo
echo An initial admin user "admin@admin.com" will be setup for access
read -s -p "Enter the password for this account: " ADMIN_PASSWORD
echo
echo "Thank you, proceeding with the install"
sleep 2
echo "Installing required progams for setup"
sleep 3
apt update
apt upgrade -y
apt install sed python3-pip python3.10-venv ca-certificates curl gnupg nginx certbot python3-certbot-nginx -y
sleep 3
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=18
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
apt update
apt install nodejs -y
corepack enable

# Setting up flask backend environment
echo "##################"
echo "Setting up Backend"
echo "##################"
cd $PARENT_DIRECTORY
sed -e "s@<DOMAIN>@$DOMAIN@g" -e "s@<EMAIL_SERVER>@$EMAIL_SERVER@g" -e "s@<EMAIL_ACCOUNT>@$EMAIL_ACCOUNT@g" -e "s@<EMAIL_PASSWORD>@$EMAIL_PASSWORD@g" ./setup/backend-env.txtn > ./backend/.env
cd ./backend
python3 -m venv venv
source venv/bin/activate
echo "Installing flask dependencies"
pip3 install -r requirements.txt
export ADMIN_PASSWORD
flask quickstart
unset ADMIN_PASSWORD
deactivate

# Install frontend dependencies
echo "###################"
echo "Setting up Frontend"
echo "###################"
cd $PARENT_DIRECTORY
sed -e "s@<DOMAIN>@$DOMAIN@g" ./setup/.env.production > ./frontend/.env.production
cd ./frontend
yarn install
echo
sleep 2

echo "########################################"
echo "Setting up Web server & SSL Certificates"
echo "########################################"
cd $PARENT_DIRECTORY
# Setup nginx
rm /etc/nginx/sites-enabled/default
if test -f /etc/nginx/sites-enabled/default; then
    rm /etc/nginx/sites-enabled/default
fi
sed -e "s@<DOMAIN>@$DOMAIN@g" ./setup/fracas-nginx.conf > /etc/nginx/sites-enabled/fracas-nginx.conf
systemctl start nginx.service
systemctl enable nginx.service

echo "Setting up certbot for SSL/HTTPS access w/ autorenew certs"
certbot --nginx --noninteractive --agree-tos --register-unsafely-without-email -d $DOMAIN
(crontab -l 2>/dev/null; echo "0 0 * * * /usr/bin/certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -

echo "Creating services for frontend and backend auto restart"
sed -e "s@<FRACAS_DIRECTORY>@$PARENT_DIRECTORY@g" ./setup/frontend.service > /etc/systemd/system/frontend.service
sed -e "s@<FRACAS_DIRECTORY>@$PARENT_DIRECTORY@g" ./setup/backend.service > /etc/systemd/system/backend.service

systemctl daemon-reload
systemctl start backend.service
systemctl enable backend.service

systemctl start frontend.service
systemctl enable frontend.service
echo
echo "#################"
echo "Install Completed"
echo "#################"
echo 
echo "Install completed. App will automatically run on reboot"
echo "Please wait for a minute or two whilst the front-end is compiling, on initial run"
echo "visit $DOMAIN with admin@admin.com, to see if everything is working"
echo
echo "Exiting setup.."
