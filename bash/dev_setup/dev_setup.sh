#! /bin/bash

# Development Environment Automated Installer (Ubuntu)
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

install_chrome() {
    display_message "Installing Chrome"
    wget -P ~/Downloads https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i ~/Downloads/google-chrome-stable_current_amd64.deb
    rm -r ~/Downloads/google-chrome-stable_current_amd64.deb
    display_message "Done"
}

install_vscode() {
    display_message "Installing VSCode"
    sudo apt-get install wget gpg -y
    wget -qO- -P ~/Downloads https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > ~/Downloads/packages.microsoft.gpg
    sudo install -D -o root -g root -m 644 ~/Downloads/packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
    rm -f ~/Downloads/packages.microsoft.gpg
    sudo apt install apt-transport-https -y
    sudo apt update
    sudo apt install code -y
    display_message "Done"
}

install_hack_nerd_font() {
    display_message "Installing Hack Nerd Font"
    wget -P ~/Downloads https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hack.zip
    sudo apt install unzip -y
    if [[ ! -d ~/.fonts/hack ]]; then
        mkdir -p ~/.fonts/hack
    fi
    unzip ~/Downloads/Hack.zip -d ~/.fonts/hack -x README.md LICENSE.md
    fc-cache -fv
    rm -f ~/Downloads/Hack.zip
    display_message "Done"
}

install_additional_packages() {
    display_message "Installing Additional Packages"
    package_list=("curl" "vim" "ubuntu-restricted-extras")
    sudo apt --ignore-missing -y install "${package_list[@]}"
    display_message "Done"
}

install_vscode_extensions() {
    display_message "Installing VSCode Extensions"
    extension_list=("ms-python.python" "zhuangtongfa.material-theme"
"pkief.material-icon-theme" "esbenp.prettier-vscode" "dbaeumer.vscode-eslint"
"dsznajder.es7-react-js-snippets")
    for extension in ${extension_list[@]}; do
        code --install-extension ${extension} --force
    done
    display_message "Done"
}

add_vscode_user_settings() {
    display_message "Adding VSCode User Settings"
    if [[ ! -f ~/.config/Code/User/settings.json ]]; then
        cp ./settings.json ~/.config/Code/User/settings.json
    fi
    display_message "Done"
}

install_nvm() {
    display_message "Installing NVM"
    latest_version_number=$(get_latest_version "nvm-sh/nvm");
    wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/${latest_version_number}/install.sh | bash
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

main() {
    display_message "Running Developer System Setup"
    #install_chrome
    #install_hack_nerd_font
    #install_additional_packages
    #install_vscode
    #install_vscode_extensions
    #add_vscode_user_settings
    #install_nvm
    #install_docker
    #install_custom_prompt
    #display_message "Done Setup Script"
}

# Run Script
main
