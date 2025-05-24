# Use Node.js version 23 based on the lightweight Alpine Linux image
FROM node:23-alpine  

# Set the working directory inside the container to /app
WORKDIR /app  

# Enable polling for file watching (required for hot-reloading in Docker)
ENV CHOKIDAR_USEPOLLING=true  

# Enable Watchpack polling for Webpack (another method for file change detection in Docker)
ENV WATCHPACK_POLLING=true