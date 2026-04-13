# Use an official Nginx image as a parent image
FROM nginx:alpine

# Copy the static frontend files into the Nginx public directory
COPY . /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# The default command for the Nginx image is already to start the server
