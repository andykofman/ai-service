from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time

app = FastAPI()

class MockResponse(BaseModel):
    status: str
    data: dict

@app.get("/mock/external/status")
async def get_status():
    # Simulate some processing time
    time.sleep(random.uniform(0.1, 0.5))
    return MockResponse(
        status="success",
        data={"service": "mock-external", "status": "operational"}
    )

@app.get("/mock/external/data")
async def get_data():
    # Simulate some processing time
    time.sleep(random.uniform(0.2, 1.0))
    return MockResponse(
        status="success",
        data={
            "items": [
                {"id": 1, "name": "Mock Item 1", "value": random.randint(1, 100)},
                {"id": 2, "name": "Mock Item 2", "value": random.randint(1, 100)},
                {"id": 3, "name": "Mock Item 3", "value": random.randint(1, 100)}
            ]
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 