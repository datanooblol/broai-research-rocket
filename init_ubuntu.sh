#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt-get update

# Upgrade installed packages
echo "Upgrading installed packages..."
sudo apt-get upgrade -y

# Optionally, perform a full upgrade
echo "Performing full upgrade..."
sudo apt-get dist-upgrade -y

# Install Git if not already installed
echo "Installing Git..."
sudo apt-get install -y git

# Install uv (fast Python package manager)
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clean up unnecessary files
echo "Cleaning up..."
sudo apt-get autoremove -y
sudo apt-get clean

echo "System update, upgrade, and tool installation completed!"
