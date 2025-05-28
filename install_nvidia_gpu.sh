#!/bin/bash

set -e  # Exit on error

echo "🔧 Updating package list..."
sudo apt update -y

echo "📦 Installing ubuntu-drivers-common..."
sudo apt install -y ubuntu-drivers-common

echo "🔍 Detecting available NVIDIA drivers..."
ubuntu-drivers devices

echo "🚀 Installing recommended NVIDIA driver (nvidia-driver-535)..."
sudo apt install -y nvidia-driver-535

echo "🔁 Rebooting to activate the driver..."
# sudo reboot
