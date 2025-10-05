import hashlib
import base64
import asyncio

async def encryptcodeVerifier(p):
    b = bytearray()
    b.extend(map(ord, p))
    ho = hashlib.sha256(b)
    hash_base64 = base64.b64encode(ho.digest()).decode('utf-8')
    return hash_base64.replace('+', '-').replace('/', '_').rstrip('=')






