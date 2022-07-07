FROM python:3.10-buster

# add app
RUN mkdir /root/frontend/
WORKDIR /root/frontend/
COPY . .
# install app dependencies
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update && apt-get install -y nodejs
RUN npm install --silent

# Expose ports
EXPOSE 3000

# Start app
CMD ["npm", "start"]
