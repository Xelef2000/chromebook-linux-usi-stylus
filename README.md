# Fixing stylus orientation in Gnome

Some Chromebooks come with USI styluses. They work fine in the newest versions of KDE Plasma, but they have a rotation issue in GNOME. The issue is that the stylus does not rotate with the screen, so it is only usable in one orientation. To fix this, we have to add an libinput override.
This script tries to do this.

## Dependencies


### Fedora/CentOS/RHEL
``` bash 
sudo dnf install python-libevdev 
```

### Debian 
``` bash 
sudo apt update && sudo apt upgrade
sudo apt install python-libevdev 
```


### Arch Linux

``` bash 
sudo pacman -Su install python-libevdev 
```

## Usage


Then run the script.

```bash
sudo python fix-stylus.py
```

Reboot your device

``` bash
reboot
```

## Consider Upstreaming Your Changes to libwacom
Please consider upstreaming your changes to [libwacom](https://github.com/linuxwacom/wacom-hid-descriptors) and [wacom-hid-descriptors](https://github.com/linuxwacom/wacom-hid-descriptors). This will help other users with the same device as you. 