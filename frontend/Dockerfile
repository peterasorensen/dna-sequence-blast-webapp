FROM python:3.10-buster

# add app
RUN mkdir /root/frontend/
WORKDIR /root/frontend/
COPY ./frontend ./
# install app dependencies
RUN apt-get update && apt-get install -y npm nodejs
#RUN npm install npm@latest -g
RUN npm install --silent

# Expose ports
EXPOSE 3000

# Start app
CMD ["npm", "start"]
