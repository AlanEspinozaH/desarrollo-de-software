import os
import sys
import logging
from flask import Flask, jsonify, request

# 12-Factor: config por entorno
PORT = int(os.getenv("PORT", "8080"))
MESSAGE = os.getenv("MESSAGE", "Hola CC3S2")
RELEASE = os.getenv("RELEASE", "dev")

# 12-Factor: logs a stdout
logger = logging.getLogger("miapp")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s'
))
logger.addHandler(handler)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    # Log en stdout (flujo, no archivo)
    logger.info("request %s %s from %s",
                request.method, request.path, request.remote_addr)
    return jsonify({
        "message": MESSAGE,
        "release": RELEASE,
        "method": request.method,
        "path": request.path
    })

if __name__ == "__main__":
    # Bind explícito al puerto de entorno
    logger.info("Starting app on 127.0.0.1:%d message=%s release=%s",
                PORT, MESSAGE, RELEASE)
    # host 127.0.0.1 para que Nginx proxyee desde la misma máquina
    app.run(host="127.0.0.1", port=PORT)

