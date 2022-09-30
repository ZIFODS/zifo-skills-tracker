FROM node:16.10 as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

FROM base AS runtime

# Create working directory
WORKDIR /app

# Install npm packages
COPY ./frontend/package.json /app
COPY ./frontend/package-lock.json /app

RUN npm install

# Copy source code
COPY ./frontend /app

# Run the application with Docker run
CMD ["npm", "start"]