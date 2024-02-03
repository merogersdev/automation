#! /bin/bash

# Version 2.1
# Arch Linux Installation Script
# Last tested with: archlinux-2024.02.01-x86_64.iso 

status_message() {
    # Fancy colored status message
    # eg. status_message "info" "this is a status message"
    type=$1
    message=$2

	case $type in 
		"error" )
		echo -e "\e[91m-> $message\e[0m"
		;;
		"info" )
		echo -e "\e[94m-> $message\e[0m"
		;;
		"success" )
		echo -e "\e[92m-> $message\e[0m"
		;;	
		*) 
		echo "No status type specified"
		;;
	esac
}

check_efi_mode() {
    # Check for EFI mode, else script will exit
    if [ "$(ls -A /sys/firmware/efi/efivars)" ]; then
        status_message "success" "EFI Mode detected. Proceeding with install"
    else
        status_message "error" "Legacy BIOS mode detected. Installation aborted"
        exit 1
    fi
}

test_internet_connection() {
    # Makes sure there is an internet connection available to download packages
    if nc -zw1 google.ca 80; then
        status_message "success" "Internet connection detected"
    else
        status_message "error" "No internet connection"
        exit 2
    fi
}

partition_disk_ext4() {
    # Formats selected disk for ext4 scheme
    # eg. partition_disk_size "/dev/sda" "16GB"
    install_disk=$1
    swap_size=$2

    parted --script $install_disk \
        mklabel gpt \
        mkpart primary fat32 1MiB 512MiB \
        name 1 "EFI" \
        set 1 esp on \
        mkpart primary linux-swap 513MiB $swap_size \
        mkpart primary ext4 $swap_size 100% \
        name 3 "ROOT"

    efi_partition="${install_disk}1"
    swap_partition="${install_disk}2"
    root_partition="${install_disk}3"

    mkfs.fat -F32 $efi_partition
    mkswap $swap_partition
    mkfs.ext4 $root_partition

    status_message "info" "Mounting volumes on: $install_disk"

    mount "$root_partition" /mnt
    mkdir -p /mnt/boot
    mount "$efi_partition" /mnt/boot

    swapon $swap_partition
    status_message "success" "Sucessfully formatted $install_disk as ext4 scheme"
}

reflector_setup() {
    # Generates pacman mirrors based on country
    # eg. reflector_setup "CA,US"
    country=$1
    status_message "info" "Updating mirrors"
    arch-chroot /mnt pacman -Syu --noconfirm --needed
    status_message "info" "Generating best mirrors"
    reflector -c $country -n 20 --protocol https --sort rate --save /mnt/etc/pacman.d/mirrorlist
    status_message "info" "Updating mirrors"
    arch-chroot /mnt pacman -Syu --noconfirm --needed
    status_message "success" "Done"
}

install_base_packages() {
    # Installs base Arch packages and specified linux kernel eg. linux, linux-lts or linux-zen
    # eg. packstrap "linux"
    status_message "info" "Installing base packages"

    packages=(
    "base"
    "$1"
    "$1-headers"
    "linux-firmware"
    "base-devel"
    )

    pacstrap /mnt "${packages[@]}"
    status_message "success" "Done"
}

install_additional_packages() {
    # Installs additional packages and utilities beyond the base system
    status_message "info" "Installing additional packages"

    packages=(
    "vim" 
    "nano" 
    "ntfs-3g"
    "btrfs-progs"
    "networkmanager" 
    "alsa-utils" 
    "wget" 
    "curl" 
    "rsync"
    "grub"
    "efibootmgr"
    "reflector"
    "xorg"
    "sudo"
    "os-prober"
    "xdg-utils"
    "xdg-user-dirs"
    "git"
    "openssh"
    "inetutils"
    )

    arch-chroot /mnt pacman -S --noconfirm --needed "${packages[@]}"
    status_message "success" "Done"
}

generate_fstab()  {
    # Saves mountpoints to FSTAB file
    status_message "info" "Generating FSTAB"
    genfstab -U /mnt >> /mnt/etc/fstab
    status_message "success" "Done"
}

set_time_date() {
    # Sets timezone and syncs hardware clock
    # eg. set_time_date "America/Regina"
    timezone=$1
    status_message "info" "Setting timezone"
    arch-chroot /mnt ln -sf /usr/share/zoneinfo/$timezone /etc/localtime
    status_message "info" "Setting hardware clock"
    arch-chroot /mnt hwclock --systohc
    status_message "success" "Done"
}

set_locale() {
    # Generates locale and language based on locale
    # eg. set_locale "en_US.UTF-8"
    locale=$1
    status_message "info" "Setting locale as: $locale"
    echo "$locale UTF-8" >> /mnt/etc/locale.gen
    arch-chroot /mnt locale-gen
    echo "LANG=$locale" >> /mnt/etc/locale.conf
    status_message "success" "Done"
}

set_console_keymap() {
    # Sets keyboard type - typically "us"
    # eg. set_console_keymap "us"
    keymap=$1
    status_message "info" "Setting console keymap as: $keymap"
    echo "KEYMAP=$keymap" >> /mnt/etc/vconsole.conf
    status_message "success" "Done"
}

set_hostname() {
    # Sets hostname for system
    # eg. set_hostname "arch"
    hostname=$1
    status_message "info" "Setting hostname as: $hostname"
    echo "$hostname" >> /mnt/etc/hostname
    status_message "success" "Done"
}

install_grub_bootloader() {
    # Installs Grub Boot Loader in EFI Mode
    status_message "info" "Installing Grub"
    arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
    sed -i "s/#GRUB_DISABLE_OS_PROBER=false/GRUB_DISABLE_OS_PROBER=false/" /mnt/etc/default/grub
    arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg
    status_message "success" "Done"
}

enable_networkmanager() {
    # Enables Network Manager
    status_message "info" "Enabling NetworkManager"
    arch-chroot /mnt systemctl enable NetworkManager
    status_message "success" "Done"
}

install_cpu_microcode() {
    # Installs CPU microcode for AMD or Intel systems
    # eg. install_cpu_microcode "amd"
    brand=$1
    status_message "info" "Installing $brand microcode"
    arch-chroot /mnt pacman -S --noconfirm --needed "$brand-ucode"
    status_message "success" "Done"
}

create_super_user()  {
    # Creates super user and adds to wheel group
    # create_super_user "arch"
    user=$1
    status_message "info" "Creating Super User"
    arch-chroot /mnt useradd -mG wheel -s /bin/bash $user
    status_message "info" "Setting permissions for super user: $user"
    touch /mnt/etc/sudoers.d/99_wheel
    cat << EOF > /mnt/etc/sudoers.d/99_wheel
%wheel ALL=(ALL) ALL
Defaults rootpw
EOF

    echo -e "Set password for $user: "
    arch-chroot /mnt /bin/passwd $user
    status_message "success" "Done"
}

set_root_password() {
    # Sets root password
    echo -e "Set Root password: "
    arch-chroot /mnt /bin/passwd
    status_message "success" "Done"
}

install_kde_desktop() {
    # Installs packages typical of a minimal KDE Plasma Desktop, and enables SDDM display manager
    status_message "info" "Install KDE Plasma Desktop Environment"

    kde_packages=(
        "plasma-desktop"
        "plasma-pa"
        "plasma-nm"
        "plasma-wayland-session"
        "dolphin"
        "ark"
        "konsole"
        "sddm-kcm"
        "dolphin-plugins"
        "kscreen"
        "kde-gtk-config"
        "kinfocenter"
        "kwrite"
        "plasma-browser-integration"
        "plasma-systemmonitor"
        "systemsettings"
        "powerdevil"
        "breeze-gtk"
        "discover"
        "firefox"
        "packagekit-qt5"
        "flatpak"
        "sddm")

    arch-chroot /mnt pacman -S --noconfirm --needed "${kde_packages[@]}"
    arch-chroot /mnt systemctl enable sddm
    status_message "success" "Done"
}

install_gnome_desktop() {
    # Installs packages typical of a Gnome Desktop, and enables GDM display manager
    status_message "info" "Installing Gnome Desktop Environment"

    gnome_packages=(
        "gnome"
        "gedit"
        "gnome-multi-writer"
        "fragments"
        "firefox"
        "flatpak"
        "gdm")

    arch-chroot /mnt pacman -S --noconfirm --needed "${gnome_packages[@]}"
    arch-chroot /mnt systemctl enable gdm
    status_message "success" "Done"
}

pacman_tweaks() {
    # Adds parallel downloads and some visual flair to pacman
    pacman_conf="/mnt/etc/pacman.conf"
    status_message "info" "Tweaks for Pacman"
    sudo sed -i "/#ParallelDownloads = 5/c\ParallelDownloads = 10" $pacman_conf
    sudo sed -i "/Color/s/^#//g" $pacman_conf
    sudo sed -i "/Color/a ILoveCandy" $pacman_conf
    status_message "success" "Done"   
}

main() {
    status_message "info" "Arch Linux Install Script"
    check_efi_mode
    loadkeys "us"
    timedatectl set-ntp true
    partition_disk_ext4 "/dev/sda" "1GB"
    install_base_packages "linux"
    pacman_tweaks
    reflector_setup "CA,US"
    install_additional_packages
    generate_fstab
    set_time_date "America/Regina"
    set_locale "en_US.UTF-8"
    set_console_keymap "us"
    set_hostname "arch"
    install_grub_bootloader
    enable_networkmanager
    install_cpu_microcode "amd"
    create_super_user "arch"
    set_root_password
    install_kde_desktop
    #install_gnome_desktop
    umount -Rl /mnt
    status_message "success" "Finished installing Arch. You may now reboot"
}

main