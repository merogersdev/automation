# VM App Deployment Scripts

## Summary

Automate setup and deployment of full-stack apps to VM services like AWS EC2, Azure, Digital Ocean...etc.

## Usage

1. Copy init.sh to the running vm instance or as a startup script.
2. Update the 'domain_name' and 'email_address' variables to reflect your preferred domain name and email address you wish for Certbot to use for your SSL certificate. Run `./init.sh`
3. SSH into your VM and copy the contents of `~/.ssh/id_ed25519.pub` to your GitHub SSH Keys. This will allow the VM to update the deployed app to the newest version.
4. In the VM, navigate to the `~/app` folder. Clone the application's repository using the SSH method eg. `git clone git@github.com:merogersdev/dev-portfolio.git`
5. Navigate to backend folder eg. `cd ./backend` and copy `env.example` to `.env` and populate the necessary environment variables.
6. Run `deploy.sh` to deploy app.
