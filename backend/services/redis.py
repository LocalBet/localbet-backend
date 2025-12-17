# backend/services/redis.py
import redis.asyncio as redis

# Conexión al servidor Redis (localhost:6379 por defecto)
redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)