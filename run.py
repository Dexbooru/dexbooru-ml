import uvicorn
import os
from dotenv import load_dotenv


def main():
    load_dotenv()

    server_port = os.getenv('PORT', 8000)
    uvicorn.run("dexbooruml.server:app", host="0.0.0.0", port=int(
        server_port), reload=False, log_level="debug")

if __name__ == '__main__':
    main()
