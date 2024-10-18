import uvicorn
import os

def main():
    server_port = os.getenv('PORT', 8000)
    uvicorn.run("dexbooruml.main:app", host="0.0.0.0", port=int(server_port), reload=False, log_level="debug")

if __name__ == '__main__':
    main()