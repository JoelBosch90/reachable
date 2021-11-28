# Use the latest version of Node.
FROM node:16-alpine3.14

# Create the working directory and give ownership to the node user.
RUN mkdir -p /client && chown -R node:node /client

# Use the new working directory.
WORKDIR /client

# Copy over all package manager files. Make sure the node user has access.
COPY --chown=node:node package*.json ./

# Tell node that we're in development mode.
ENV NODE_ENV development

# Use the node user to run the install commands.
USER node

# Install all node dependencies.
RUN npm install

# Copy the application files to the directory.
COPY --chown=node:node . .

# Let Nuxt know where we're hosting.
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=8000

# We want to host the client at port 8000.
EXPOSE 8000

# Start the client server in development mode.
CMD ["npm", "run", "dev"]
