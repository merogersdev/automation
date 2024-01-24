#! /bin/bash

# Version 2.0
# Arch Linux Installation Script

status_message() {
	case "$1" in 
		"error" )
		echo -e "\e[91m-> $2\e[0m"
		;;
		"info" )
		echo -e "\e[94m-> $2\e[0m"
		;;
		"success" )
		echo -e "\e[92m-> $2\e[0m"
		;;	
		*) 
		echo "No status type specified"
		;;
	esac
}

check_efi_mode() {
  if [ "$(ls -A /sys/firmware/efi/efivars)" ]; then
    status_message "success" "EFI Mode detected. Proceeding with install"
  else
    status_message "error" "Legacy BIOS mode detected. Installation aborted"
    exit 1
  fi
}

test_internet_connection() {
  if nc -zw1 google.com 80; then
    status_message "success" "Internet connection detected"
  else
    status_message "error" "No internet connection"
    exit 2
  fi
}

partition_disk_ext4() {
  # Args: disk swapsize
  # eg. partition_disk_size "/dev/sda" "16GB"
  parted --script $1 \
      mklabel gpt \
      mkpart primary fat32 1MiB 512MiB \
      name 1 "EFI" \
      set 1 esp on \
      mkpart primary linux-swap 513MiB $2 \
      mkpart primary ext4 $2 100% \
      name 3 "ROOT"

  mkfs.fat -F32 "${1}1"
  mkswap "${1}2"
  mkfs.ext4 "${1}3"

  status_message "info" "Mounting volumes on: $1"

  mount "${1}3" /mnt
  mkdir -p /mnt/boot
  mount "${$}1" /mnt/boot

  swapon "${1}2"
  status_message "success" "Sucessfully formatted $1 as ext4"
}

partition_disk_btrfs() {
  # NOTE: Experimental
  # Args: disk swapsize
  # eg. partition_disk_btrfs "/dev/sda" "16GB"
  parted --script $1 \
      mklabel gpt \
      mkpart primary fat32 1MiB 350MiB \
      set 1 esp on \
      name 1 "EFI" \
      mkpart primary btrfs 351MiB 100% \
      name 2 "ROOT"

  mkfs.vfat "${$1}1"
  mkfs.btrfs "${$1}2"

  status_message "info" "Mounting volumes on: $1"

  mount "${$1}2" /mnt
  btrfs su cr /mnt/@
  btrfs su cr /mnt/@home
  btrfs su cr /mnt/@var
  umount /mnt

  mount -o noatime,compress=zstd,ssd,discard=async,space_cache=v2,subvol=@ "${$1}2" /mnt
  mkdir -p /mnt/{boot,home,var}
  mount -o noatime,compress=zstd,ssd,discard=async,space_cache=v2,subvol=@home "${$1}2" /mnt/home
  mount -o noatime,compress=zstd,ssd,discard=async,space_cache=v2,subvol=@var "${$1}2" /mnt/var
  mount "${$1}1" /mnt/boot

  status_message "success" "Sucessfully formatted $1 as btrfs"
}

packman_mirrors_setup() {
  # Args: Two letter country codes for package mirrors
  # eg. packman_mirrors_setup "CA,US"
  status_message "info" "Generating best mirrors"
  reflector --country "$1" --protocol http,https --sort rate -l 10 --save /mnt/etc/pacman.d/mirrorlist
  status_message "info" "Updating mirrors"
  arch-chroot /mnt pacman -Syu --noconfirm
}

install_base_packages() {
  # Args: linux kernel type eg. linux, linux-lts or linux-zen
  # eg. packstrap "linux"
  status_message "info" "Installing base packages"

  packages=(
  "base"
  "$1"
  "$1-headers"
  "linux-firmware"
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

  pacstrap /mnt "${packages[@]}"
}

generate_fstab()  {
  # Generates mount info file
  status_message "info" "Generating FSTAB"
  genfstab -U /mnt >> /mnt/etc/fstab
}

set_time_date() {
  # Args: Timezone
  # eg. set_time_date "America/Regina"
  status_message "info" "Setting timezone"
  arch-chroot /mnt ln -sf /usr/share/zoneinfo/$1 /etc/localtime
  status_message "info" "Setting hardware clock"
  arch-chroot /mnt hwclock --systohc
}

set_locale() {
  # Args: Locale and encoding
  # eg. set_locale "en_US.UTF-8"
  status_message "info" "Setting locale as: $1"
  echo "$1 UTF-8" >> /mnt/etc/locale.gen
  arch-chroot /mnt locale-gen
  echo "LANG=$1" >> /mnt/etc/locale.conf
}

set_console_keymap() {
  # Args: keyboard type
  # eg. set_console_keymap "us"
  status_message "info" "Setting console keymap as: $1"
  echo "KEYMAP=$1" >> /mnt/etc/vconsole.conf
}

set_hostname() {
  # Args: hostname for system
  # eg. my-computer
  status_message "info" "Setting hostname as: $1"
  echo "$1" >> /mnt/etc/hostname
}

install_bootloader() {
  status_message "info" "Installing Grub"
  arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
  sed -i "s/#GRUB_DISABLE_OS_PROBER=false/GRUB_DISABLE_OS_PROBER=false/" /mnt/etc/default/grub
  arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg
}

enable_networkmanager() {
  status_message "info" "Enabling NetworkManager"
  arch-chroot /mnt systemctl enable NetworkManager
}

install_cpu_microcode() {
  # Args: cputype
  # eg. install_cpu_microcode "amd"
  status_message "info" "Installing $1 microcode"
  arch-chroot /mnt pacman -S --noconfirm "$1-ucode"
}

enable_btrfs_module() {
  # Args: linux
  # eg enable_btrfs_module "linux"
  status_message "info" "Creating initial ramdisk environment with btrfs support"
  sed -i "s/MODULES=()/MODULES=(btrfs)/" /etc/mkinitcpio.conf
  arch-chroot /mnt mkinitcpio -p $1
}

create_super_user()  {
  # Args: user
  # create_super_user "arch"
  status_message "info" "Creating Super User"
  arch-chroot /mnt useradd -mG wheel -s /bin/bash $1
  status_message "info" "Setting permissions for super user: $1"
  touch /mnt/etc/sudoers.d/99_wheel
  cat << EOF > /mnt/etc/sudoers.d/99_wheel
%wheel ALL=(ALL) ALL
Defaults rootpw
EOF

  echo -e "Set password for $1: "
  arch-chroot /mnt /bin/passwd $1
}

set_root_password() {
  echo -e "Set Root password: "
  arch-chroot /mnt /bin/passwd
}

install_kde_desktop() {
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
    "arc-gtk-theme"
    "discover"
    "firefox"
    "packagekit-qt5"
    "flatpak"
    "base-devel"
    "sddm")

  arch-chroot /mnt pacman -S --noconfirm --needed "${kde_packages[@]}"
  arch-chroot /mnt systemctl enable sddm
}

install_gnome_desktop() {
  status_message "info" "Installing Gnome Desktop Environment"
  arch-chroot /mnt pacman -S --noconfirm --needed gnome-shell nautilus gnome-terminal fragments gedit gnome-calendar gnome-desktop gnome-keyring gnome-session gnome-disk-utility tilix gnome-tweak-tool gnome-control-center papirus-icon-theme gnome-software firefox flatpak base-devel gdm
  arch-chroot /mnt systemctl enable gdm
}

main() {
  status_message "info" "Arch Linux Install Script"
  check_efi_mode
  loadkeys "us"
  timedatectl set-ntp true
  partition_disk_ext4 "/dev/sda" "1GB"
  #partition_disk_btrfs "/dev/sda/" "16GB"
  packman_mirrors_setup "CA,US"
  packstrap "linux"
  generate_fstab
  set_time_date "America/Regina"
  set_locale "en_US.UTF-8"
  set_console_keymap "us"
  set_hostname "arch"
  install_bootloader
  enable_networkmanager
  install_cpu_microcode "amd"
  # enable_btrfs_module "linux"
  create_super_user "arch"
  set_root_password
  install_kde_desktop
  #install_gnome_desktop
  umount -Rl /mnt
  status_message "success" "Finished installing Arch. You may now reboot"
}

main