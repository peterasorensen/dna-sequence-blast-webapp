FROM python:3.10-buster
WORKDIR /root

# add app
RUN mkdir frontend/
COPY . ./frontend/
# install app dependencies
RUN apt-get update && apt-get install -y npm
RUN npm install npm@latest -g
RUN npm install --silent

# Expose ports
EXPOSE 3000

# Start app
CMD ["npm", "start"]
