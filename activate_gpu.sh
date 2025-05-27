#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install prerequisites
echo "Installing prerequisites..."
sudo apt-get install -y curl gnupg lsb-release

# Add NVIDIA GPG key
echo "Adding NVIDIA GPG key..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# Add NVIDIA container toolkit repository
echo "Adding NVIDIA container toolkit repository..."
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Update package list again
echo "Updating package list with NVIDIA repository..."
sudo apt-get update

# Install NVIDIA container toolkit
echo "Installing NVIDIA container toolkit..."
sudo apt-get install -y nvidia-container-toolkit

# Install NVIDIA drivers
echo "Installing NVIDIA drivers..."
sudo apt-get install -y nvidia-driver-470  # Change version as needed

# Configure NVIDIA runtime for Docker
echo "Configuring NVIDIA runtime for Docker..."
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker service
echo "Restarting Docker service..."
sudo systemctl restart docker

# Print success message
echo "GPU activated successfully with Docker!"