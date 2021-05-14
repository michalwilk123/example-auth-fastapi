import uvicorn
# from app.main import app

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app", 
        host="localhost", 
        port=5000, 
        reload=True, 
        access_log=True, 
        log_level="trace"
    )
