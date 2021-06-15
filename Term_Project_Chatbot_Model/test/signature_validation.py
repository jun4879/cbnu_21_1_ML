import base64
import hashlib
import hmac

channel_secret = '4a1a6848b135f44df56004d8ef63c81f' # Channel secret string
body = '' # Request body string
hash = hmac.new(channel_secret.encode('utf-8'),
    body.encode('utf-8'), hashlib.sha256).digest()
signature = base64.b64encode(hash)
# Compare x-line-signature request header and the signature
