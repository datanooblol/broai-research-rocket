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

# # Install uv (fast Python package manager)
# echo "Installing uv..."
# curl -LsSf https://astral.sh/uv/install.sh | sh

#!/bin/bash

# Exit immediately on error
set -e

echo "Installing uv (fast Python package manager)..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure ~/.cargo/bin is in PATH
if ! grep -q 'export PATH="$HOME/.cargo/bin:$PATH"' ~/.bashrc; then
  echo 'Adding uv to PATH via ~/.bashrc'
  echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
else
  echo 'uv PATH already present in ~/.bashrc'
fi

# Apply changes to current session
export PATH="$HOME/.cargo/bin:$PATH"
echo "uv version: $(uv --version)"

echo "Done. You may need to restart your terminal for changes to fully apply."


# Clean up unnecessary files
echo "Cleaning up..."
sudo apt-get autoremove -y
sudo apt-get clean

echo "System update, upgrade, and tool installation completed!"
