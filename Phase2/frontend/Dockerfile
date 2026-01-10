# 1. Start with a base system (like buying a laptop with Node installed)
FROM node:24-alpine

# 2. Set the working folder inside the container
WORKDIR /app

# 3. Copy only package files first (better for caching)
COPY package.json ./

# 4. Install dependencies
RUN npm install

# 5. Copy the rest of your code
COPY . .

# 6. Expose the port your app runs on
EXPOSE 3000

# 7. The command to start the app
CMD ["npm", "start"]