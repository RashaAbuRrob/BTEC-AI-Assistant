from app import create_app
from config.settings import Config
import os

if __name__ == '__main__':
    app = create_app()
    
    # Run the Flask application
    port = Config.FLASK_PORT
    debug = Config.FLASK_ENV == 'development'
    
    print(f"Starting BTEC Smart Assistant on port {port}...")
    print(f"Environment: {Config.FLASK_ENV}")
    
    app.run(
        host='127.0.0.1',
        port=port,
        debug=debug
    )
