# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Public API URL is baked into the client bundle at build time (import.meta.env.VITE_*)
# Override from docker-compose build.args for the droplet's public IP/domain.
ARG VITE_API_BASE_URL=http://localhost:5000
ARG VITE_API_TIMEOUT=30000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_API_TIMEOUT=$VITE_API_TIMEOUT

# Build the application
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Copy built application
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0

# Start the application
CMD ["node", "build"]

# Development stage
FROM node:20-alpine AS development

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies)
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]
