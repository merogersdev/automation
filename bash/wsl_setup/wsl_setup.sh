#! /usr/bin/bash
# Version 1.0

display_message() {
    line='--------------------'
    echo $line
    echo $1
    echo $line
    echo
}

get_latest_version() {
    basename $(curl -fs -o/dev/null -w %{redirect_url} https://github.com/$1/releases/latest)
}

install_custom_prompt() {
    display_message "Installing Custom Prompt"
    if [[ ! -f ~/prompt.sh ]]; then
        wget -P ~/ https://raw.githubusercontent.com/merogersdev/automation/main/bash/prompt/prompt.sh
        chmod +x ~/prompt.sh
    fi

    cat << EOF | tee -a ~/.bashrc
# Custom Bash Prompt
if [ -f ~/prompt.sh ]
then
    . ~/prompt.sh
fi
EOF
    display_message "Done - Restart Terminal"
}

install_docker() {
    display_message "Installing Docker CE"
    sudo apt update
    sudo apt -y install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $USER
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    display_message "Done - Restart System"
}

install_nvm() {
    display_message "Installing NVM"
    latest_version_number=$(get_latest_version "nvm-sh/nvm");
    wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/${latest_version_number}/install.sh | bash
    display_message "Done - Restart Terminal"
}


main() {
    display_message "Running WSL Developer Environment Setup"
    install_nvm
    install_custom_prompt
    install_docker
    display_message "Done - Setup Script"
}

# Run script
main