# Use the latest version of Node.
FROM node:16-alpine3.14 as build

# Create the working directory and give ownership to the node user.
RUN mkdir -p /client && chown -R node:node /client

# Use the new working directory.
WORKDIR /client

# Copy over all package manager files.
COPY --chown=node:node package*.json ./

# We need to build in development mode.
ENV NODE_ENV development

# Use the node user to run the install commands.
USER node

# Install all development dependencies.
RUN npm install

# Copy the application files to the directory.
COPY --chown=node:node . .

# Make sure we optimize for production.
RUN npm run build

# Use our build phase to host the live environment.
FROM build as release

# After building, we can switch to production mode.
ENV NODE_ENV=production

# Use the node user to run the install commands.
USER node

# Install only the libraries that we need for production.
RUN npm ci --only=production

# Let Nuxt know where we're hosting.
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=8000

# We want to host the client at port 8000.
EXPOSE 8000

# Start the client server in production mode.
CMD ["npm", "run", "start"]
