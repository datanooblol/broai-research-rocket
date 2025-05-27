#!/bin/bash

sudo chmod +x ./init_ubuntu.sh && sudo ./init_ubuntu.sh
sudo chmod +x ./install_docker.sh && sudo ./install_docker.sh
sudo chmod +x ./activate_gpu.sh && sudo ./activate_gpu.sh

echo "All scripts executed successfully. Your environment is now set up."