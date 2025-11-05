import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.core.logger import setup_logger
from src.core.platform import PlatformDetector
from src.checker.environment_checker import EnvironmentChecker
from src.setup.setup_manager import SetupManager
from src.update.update_manager import UpdateManager
from src.troubleshooting.problem_solver import ProblemSolver
from src.api.mcp_server import register_mcp_routes
from src.api.dev_info import DevelopmentInfoProvider

# Initialize FastAPI app
app = FastAPI(
    title="Local Computer Assistant API",
    description="Agent-to-Agent API for Local Computer Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register MCP routes
register_mcp_routes(app)

# Security
security = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Global state
logger = setup_logger()
platform_detector = PlatformDetector()
platform_info = platform_detector.detect()

# Request/Response Models
class CheckRequest(BaseModel):
    verbose: bool = False
    include_software: bool = True
    include_network: bool = True
    include_security: bool = True

class SetupRequest(BaseModel):
    config_path: str = "config/default.yaml"
    packages: Optional[List[str]] = None

class UpdateRequest(BaseModel):
    auto_apply: bool = False

class DiagnoseRequest(BaseModel):
    categories: Optional[List[str]] = None

class FixRequest(BaseModel):
    auto_fix: bool = True
    issue_ids: Optional[List[str]] = None

class APIResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class Capability(BaseModel):
    name: str
    description: str
    parameters: Optional[Dict[str, Any]] = None

class AgentInfo(BaseModel):
    agent_id: str = "local-computer-assistant"
    name: str = "Local Computer Assistant"
    version: str = "1.0.0"
    capabilities: List[Capability]
    endpoints: Dict[str, str]
    status: str = "active"

# Authentication (simplified - implement proper OAuth2 for production)
async def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
    # TODO: Implement proper API key validation
    # For now, allow if API key is provided or use default key
    # Get API key from environment variable
    expected_key = os.getenv("API_KEY", None)
    if api_key and expected_key and api_key == expected_key:
        return api_key
    return None

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Local Computer Assistant API", "version": "1.0.0"}

@app.get("/api/v1/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint"""
    return APIResponse(
        status="success",
        data={"status": "healthy", "platform": platform_info['os']},
        message="Service is operational"
    )

@app.get("/api/v1/capabilities", response_model=APIResponse)
async def get_capabilities():
    """Get list of assistant capabilities"""
    capabilities = [
        Capability(
            name="check_environment",
            description="Check and analyze computer environment",
            parameters={"verbose": "bool", "include_software": "bool"}
        ),
        Capability(
            name="setup_system",
            description="Setup and configure system",
            parameters={"config_path": "string", "packages": "list"}
        ),
        Capability(
            name="check_updates",
            description="Check for system and software updates",
            parameters={"auto_apply": "bool"}
        ),
        Capability(
            name="diagnose_issues",
            description="Detect system issues",
            parameters={"categories": "list"}
        ),
        Capability(
            name="fix_issues",
            description="Fix detected issues",
            parameters={"auto_fix": "bool", "issue_ids": "list"}
        ),
    ]
    
    return APIResponse(
        status="success",
        data={"capabilities": [c.dict() for c in capabilities]},
        message="Capabilities retrieved successfully"
    )

@app.get("/api/v1/agent-info", response_model=AgentInfo)
async def get_agent_info():
    """Get agent information for discovery"""
    capabilities = [
        Capability(name="check_environment", description="Check environment"),
        Capability(name="setup_system", description="Setup system"),
        Capability(name="check_updates", description="Check updates"),
        Capability(name="diagnose_issues", description="Diagnose issues"),
        Capability(name="fix_issues", description="Fix issues"),
    ]
    
    return AgentInfo(
        capabilities=capabilities,
        endpoints={
            "rest": "http://localhost:8000/api/v1",
            "mcp": "http://localhost:8000/mcp"
        }
    )

@app.post("/api/v1/check", response_model=APIResponse)
async def check_environment(request: CheckRequest = CheckRequest()):
    """Check computer environment"""
    try:
        checker = EnvironmentChecker(platform_info, logger)
        results = checker.check_all()
        
        # Filter results based on request
        filtered_results = {}
        if request.include_software:
            filtered_results['software'] = results.get('software', {})
        if request.include_network:
            filtered_results['network'] = results.get('network', {})
        if request.include_security:
            filtered_results['security'] = results.get('security', {})
        
        filtered_results['system'] = results.get('system', {})
        filtered_results['resources'] = results.get('resources', {})
        filtered_results['development'] = results.get('development', {})
        
        return APIResponse(
            status="success",
            data=filtered_results,
            message="Environment check completed"
        )
    except Exception as e:
        logger.error(f"Error in check: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/setup", response_model=APIResponse)
async def setup_system(request: SetupRequest):
    """Setup system from configuration"""
    try:
        manager = SetupManager(platform_info, logger)
        manager.setup_from_config(request.config_path)
        
        return APIResponse(
            status="success",
            message="System setup initiated"
        )
    except Exception as e:
        logger.error(f"Error in setup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/update", response_model=APIResponse)
async def check_updates(request: UpdateRequest = UpdateRequest()):
    """Check for updates"""
    try:
        update_manager = UpdateManager(platform_info, logger)
        update_manager.check_and_update()
        
        return APIResponse(
            status="success",
            message="Update check completed"
        )
    except Exception as e:
        logger.error(f"Error in update: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/diagnose", response_model=APIResponse)
async def diagnose_issues(request: DiagnoseRequest = DiagnoseRequest()):
    """Diagnose system issues"""
    try:
        solver = ProblemSolver(platform_info, logger)
        issues = solver.detect_issues()
        
        # Filter by categories if specified
        if request.categories:
            issues = [i for i in issues if i.get('category') in request.categories]
        
        return APIResponse(
            status="success",
            data={"issues": issues, "count": len(issues)},
            message=f"Found {len(issues)} issues"
        )
    except Exception as e:
        logger.error(f"Error in diagnose: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/fix", response_model=APIResponse)
async def fix_issues(request: FixRequest = FixRequest()):
    """Fix detected issues"""
    try:
        solver = ProblemSolver(platform_info, logger)
        issues = solver.detect_issues()
        
        # Filter by issue_ids if specified
        if request.issue_ids:
            issues = [i for i in issues if i.get('id') in request.issue_ids]
        
        if request.auto_fix:
            solver.fix_issues(issues)
        
        return APIResponse(
            status="success",
            data={"issues_fixed": len(issues)},
            message=f"Fixed {len(issues)} issues"
        )
    except Exception as e:
        logger.error(f"Error in fix: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/status", response_model=APIResponse)
async def get_status():
    """Get assistant status"""
    return APIResponse(
        status="success",
        data={
            "platform": platform_info['os'],
            "version": platform_info.get('version', 'unknown'),
            "status": "active"
        },
        message="Assistant is active"
    )

@app.get("/api/v1/dev-info", response_model=APIResponse)
async def get_development_info():
    """Get development information: system specs and development tools"""
    try:
        provider = DevelopmentInfoProvider(platform_info, logger)
        dev_info = provider.get_development_info()
        
        return APIResponse(
            status="success",
            data=dev_info,
            message="Development information retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error getting dev info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Run the API server"""
    import uvicorn
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()

