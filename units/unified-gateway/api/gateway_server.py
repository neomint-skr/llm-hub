"""
Unified Gateway Server
FastAPI Gateway that connects to MCP servers as a client
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from .health import create_health_router

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Unified Gateway", version="1.0.0")

# Security scheme
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify bearer token"""
    if not os.getenv("AUTH_ENABLED", "true").lower() == "true":
        return True

    expected_token = os.getenv("API_KEY", "changeme")
    if credentials.credentials != expected_token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return True

# Add CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include health router
health_router = create_health_router()
app.include_router(health_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Unified Gateway", "version": "1.0.0"}

# Public routes defined - auth middleware applied via dependencies
@app.post("/tools/{tool_name}")
async def execute_tool(tool_name: str, _: bool = Depends(verify_token)):
    """Execute tool via gateway"""
    return {"message": f"Tool {tool_name} execution placeholder", "status": "not_implemented"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("GATEWAY_PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
