# ---------- Stage 1: Build the frontend ----------
    FROM node:18 AS builder

    # 1) Set working directory
    WORKDIR /app
    
    # 2) Copy package files and install dependencies
    COPY package*.json ./
    RUN npm install
    
    # 3) Copy the rest of the frontend code
    COPY . .
    
    # 4) Build the production version
    RUN npm run build
    
    # ---------- Stage 2: Serve the built files ----------
    FROM node:18-alpine
    
    # 5) Create a directory for the app
    WORKDIR /app
    
    # 6) Copy build artifacts from builder
    COPY --from=builder /app/dist ./dist
    
    # 7) Install a simple static server
    RUN npm install -g serve
    
    # 8) Expose port 3000
    EXPOSE 3000
    
    # 9) Command to serve the build on port 3000
    CMD ["serve", "-s", "dist", "-l", "3000"]
        