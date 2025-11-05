"""
MCP (Model Context Protocol) Server Implementation
JSON-RPC 2.0 server for agent-to-agent communication
"""
import json
from typing import Any, Dict, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.core.logger import setup_logger
from src.core.platform import PlatformDetector
from src.checker.environment_checker import EnvironmentChecker
from src.setup.setup_manager import SetupManager
from src.update.update_manager import UpdateManager
from src.troubleshooting.problem_solver import ProblemSolver
from src.api.dev_info import DevelopmentInfoProvider

logger = setup_logger()
platform_detector = PlatformDetector()
platform_info = platform_detector.detect()

class MCPServer:
    """MCP Server implementing JSON-RPC 2.0"""
    
    def __init__(self):
        self.methods = {
            "mcp.get_dev_info": self.get_dev_info,
            "mcp.check_environment": self.check_environment,
            "mcp.setup_system": self.setup_system,
            "mcp.check_updates": self.check_updates,
            "mcp.diagnose_issues": self.diagnose_issues,
            "mcp.fix_issues": self.fix_issues,
            "mcp.list_capabilities": self.list_capabilities,
            "mcp.get_status": self.get_status,
        }
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC 2.0 request"""
        try:
            # Validate JSON-RPC 2.0 format
            if request.get("jsonrpc") != "2.0":
                return self._error_response(
                    request.get("id"),
                    -32600,
                    "Invalid Request",
                    "jsonrpc must be '2.0'"
                )
            
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if not method:
                return self._error_response(request_id, -32600, "Invalid Request", "method is required")
            
            if method not in self.methods:
                return self._error_response(request_id, -32601, "Method not found", f"Method '{method}' not found")
            
            # Call the method
            result = self.methods[method](params)
            
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
            
        except Exception as e:
            logger.error(f"Error handling MCP request: {e}", exc_info=True)
            return self._error_response(
                request.get("id"),
                -32603,
                "Internal error",
                str(e)
            )
    
    def _error_response(self, request_id: Optional[Any], code: int, message: str, data: Any = None) -> Dict[str, Any]:
        """Create error response"""
        error = {
            "code": code,
            "message": message
        }
        if data:
            error["data"] = data
        
        response = {
            "jsonrpc": "2.0",
            "error": error,
            "id": request_id
        }
        return response
    
    def get_dev_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get development information: system specs and development tools"""
        provider = DevelopmentInfoProvider(platform_info, logger)
        return provider.get_development_info()
    
    def check_environment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check environment"""
        checker = EnvironmentChecker(platform_info, logger)
        results = checker.check_all()
        return results
    
    def setup_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Setup system"""
        config_path = params.get("config_path", "config/default.yaml")
        manager = SetupManager(platform_info, logger)
        manager.setup_from_config(config_path)
        return {"status": "success", "message": "Setup initiated"}
    
    def check_updates(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check updates"""
        update_manager = UpdateManager(platform_info, logger)
        update_manager.check_and_update()
        return {"status": "success", "message": "Update check completed"}
    
    def diagnose_issues(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Diagnose issues"""
        solver = ProblemSolver(platform_info, logger)
        issues = solver.detect_issues()
        
        categories = params.get("categories")
        if categories:
            issues = [i for i in issues if i.get('category') in categories]
        
        return {
            "issues": issues,
            "count": len(issues)
        }
    
    def fix_issues(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fix issues"""
        solver = ProblemSolver(platform_info, logger)
        issues = solver.detect_issues()
        
        issue_ids = params.get("issue_ids")
        if issue_ids:
            issues = [i for i in issues if i.get('id') in issue_ids]
        
        auto_fix = params.get("auto_fix", True)
        if auto_fix:
            solver.fix_issues(issues)
        
        return {
            "status": "success",
            "issues_fixed": len(issues)
        }
    
    def list_capabilities(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List capabilities"""
        return {
            "capabilities": [
                {
                    "name": "get_dev_info",
                    "description": "Get development information: system specs and development tools",
                    "parameters": {}
                },
                {
                    "name": "check_environment",
                    "description": "Check and analyze computer environment",
                    "parameters": {
                        "verbose": "bool",
                        "include_software": "bool",
                        "include_network": "bool",
                        "include_security": "bool"
                    }
                },
                {
                    "name": "setup_system",
                    "description": "Setup and configure system",
                    "parameters": {
                        "config_path": "string",
                        "packages": "list"
                    }
                },
                {
                    "name": "check_updates",
                    "description": "Check for system and software updates",
                    "parameters": {
                        "auto_apply": "bool"
                    }
                },
                {
                    "name": "diagnose_issues",
                    "description": "Detect system issues",
                    "parameters": {
                        "categories": "list"
                    }
                },
                {
                    "name": "fix_issues",
                    "description": "Fix detected issues",
                    "parameters": {
                        "auto_fix": "bool",
                        "issue_ids": "list"
                    }
                }
            ]
        }
    
    def get_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get status"""
        return {
            "status": "active",
            "platform": platform_info['os'],
            "version": platform_info.get('version', 'unknown')
        }

# Create MCP server instance
mcp_server = MCPServer()

# Add MCP endpoint to FastAPI app
def register_mcp_routes(app: FastAPI):
    """Register MCP routes with FastAPI app"""
    
    @app.post("/mcp")
    async def mcp_endpoint(request: Dict[str, Any]):
        """MCP JSON-RPC 2.0 endpoint"""
        try:
            # Handle batch requests
            if isinstance(request, list):
                responses = [mcp_server.handle_request(req) for req in request]
                return JSONResponse(content=responses)
            else:
                response = mcp_server.handle_request(request)
                return JSONResponse(content=response)
        except Exception as e:
            logger.error(f"Error in MCP endpoint: {e}", exc_info=True)
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": "Internal error",
                        "data": str(e)
                    },
                    "id": request.get("id") if isinstance(request, dict) else None
                },
                status_code=500
            )
    
    @app.get("/mcp/info")
    async def mcp_info():
        """MCP server information"""
        return {
            "name": "Local Computer Assistant MCP Server",
            "version": "1.0.0",
            "protocol": "json-rpc-2.0",
            "methods": list(mcp_server.methods.keys())
        }

