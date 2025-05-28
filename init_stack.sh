#!/bin/bash

sudo chmod +x ./init_ubuntu.sh && sudo ./init_ubuntu.sh
sudo chmod +x ./install_docker.sh && sudo ./install_docker.sh
sudo chmod +x ./install_nvidia.sh && sudo ./install_nvidia.sh
sudo chmod +x ./activate_gpu.sh && sudo ./activate_gpu.sh
sudo chmod +x ./install_aws_cli.sh && sudo ./install_aws_cli.sh

echo "All scripts executed successfully. Your environment is now set up."
sudo reboot