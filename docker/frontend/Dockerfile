# Build Stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy project files
COPY frontend/ .

# ENV variable needs to be set at build time
ENV NEXT_PUBLIC_API_URL=http://localhost:8000

# Build the Next.js app
RUN npm run build

# Runtime Stage
FROM node:20-alpine

WORKDIR /app

# Node ENV variable
ENV NODE_ENV=production

# Create a non-root user for better security
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

# Copy necessary files from builder stage
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000 \
    NEXT_TELEMETRY_DISABLED=1

CMD ["node", "server.js"]

