# Stage 1: Build React app
FROM node:24-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json first (for Docker cache optimization)
COPY package.json .

# Install dependencies
RUN npm install

# Copy rest of frontend code
COPY . .

# Build the React app for production
RUN npm run build

# Stage 2: Serve built React app using nginx
FROM nginx:alpine

# Copy built files from Stage 1 into nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Nginx runs automatically
CMD ["nginx", "-g", "daemon off;"]