#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt-get update

# Install necessary packages
echo "Installing prerequisites..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Remove existing Docker GPG key if it exists
if [ -f /usr/share/keyrings/docker-archive-keyring.gpg ]; then
    echo "Removing existing Docker GPG key..."
    sudo rm /usr/share/keyrings/docker-archive-keyring.gpg
fi

# Add Docker's official GPG key
echo "Adding Docker GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
UBUNTU_VERSION=$(lsb_release -cs) # Automatically fetch your Ubuntu version codename
echo "Adding Docker repository..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $UBUNTU_VERSION stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again to include Docker repository
echo "Updating package list with Docker repository..."
sudo apt-get update

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version


# Optional: Add the current user to the Docker group to run without sudo
echo "Adding current user to Docker group..."
sudo usermod -aG docker $USER

echo "Docker installation completed! Please log out and log back in to apply the Docker group changes."

# ---------------------------------
# Install Docker Compose
# ---------------------------------

echo "Installing Docker Compose..."

# Download the latest version of Docker Compose
# sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '\"' -f 4)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to the Docker Compose binary
sudo chmod +x /usr/local/bin/docker-compose

# Verify Docker Compose installation
docker-compose --version

echo "Docker Compose installation completed!"