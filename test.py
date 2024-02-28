import websockets
import asyncio
import http.server
import socketserver
import threading
import logging
from running_bot import running_bot  
import uuid
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server data
PORT = 7890
HTTP_PORT = 8001  # Port for serving HTML file
logger.info("Server listening on Port %d", PORT)

# Dictionary to store session IDs for each WebSocket connection
sessions = {}

# Flag to indicate whether the HTTP server should keep serving
http_server_running = True

# The main behavior function for this server
async def echo(websocket, path):
    # Generate a unique session ID for the current WebSocket connection
    session_id = str(uuid.uuid4())
    sessions[session_id] = websocket

    logger.info("A client connected with session ID: %s", session_id)

    # Handle incoming messages
    try:
        async for message in websocket:
            logger.info("Received message from client with session ID %s: %s", session_id, message)
            # Process the message using running_bot function
            response = running_bot(message, session_id)
            await websocket.send(response)
    # Handle disconnecting clients 
    except websockets.exceptions.ConnectionClosed as e:
        logger.info("A client with session ID %s disconnected", session_id)
    finally:
        del sessions[session_id]

# Function to serve HTML file
def serve_html():
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", HTTP_PORT), Handler)
    logger.info("Serving HTML file at http://localhost:%d/client.html", HTTP_PORT)
    global http_server_running
    while http_server_running:
        httpd.handle_request()

# Start the WebSocket server
start_server = websockets.serve(echo, "localhost", PORT)

# Start the HTTP server in a separate thread
html_thread = threading.Thread(target=serve_html)
html_thread.start()

try:
    # Start the event loop for WebSocket server
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    logger.info("KeyboardInterrupt: Stopping servers...")
    # Set the flag to stop the HTTP server
    http_server_running = False
    # Wait for the HTTP server thread to finish
    html_thread.join()
    logger.info("Servers stopped.")
    sys.exit(0)
