# ── Stage 1: Builder ──────────────────────────────────────────
FROM node:18-slim AS builder

WORKDIR /app

# Copy package files first (layer caching — only reinstalls if deps change)
COPY package*.json ./

RUN npm ci --omit=dev


# ── Stage 2: Final image ──────────────────────────────────────
FROM node:18-slim

WORKDIR /app

# Copy only installed modules from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy app source
COPY . .

RUN useradd -m appuser && chown -R appuser /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

CMD ["node", "app.js"]