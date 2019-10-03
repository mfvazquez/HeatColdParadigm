#!/bin/sh
install_dir=$(dirname $0)
pip install -r $install_dir/requirements
whl_file=wxPython-4.0.6-cp36-cp36m-linux_x86_64.whl
wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/$whl_file -O $install_dir/$whl_file 
sudo apt-get install libusb-1.0-0-dev portaudio19-dev libasound2-dev
pip install $install_dir/$whl_file
