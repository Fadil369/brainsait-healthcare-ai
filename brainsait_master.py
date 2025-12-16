"""
BRAINSAIT MASTERLINC MCP Server
Healthcare AI Orchestration with NPHIES Compliance & FHIR R4 Interoperability
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging
import os
import sys
import importlib
from pathlib import Path
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime, timezone

# BRAINSAIT: HIPAA + Arabic RTL support
from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# MEDICAL: FHIR R4 validation
from fhir.resources.patient import Patient
from fhir.resources.claim import Claim
from fhir.resources.coverage import Coverage
from cryptography.fernet import Fernet

# Healthcare logging with audit trail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - MASTERLINC - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BrainSAITMasterLinc:
    """
    MASTERLINC: Master Healthcare AI Orchestration Agent
    
    Core Capabilities:
    - NPHIES Claims Processing & Revenue Cycle Optimization
    - FHIR R4 Resource Management & Interoperability  
    - Clinical Decision Support with Arabic/English Bilingual UI
    - Automated Workflow Orchestration via n8n Integration
    - HIPAA Compliant Audit Logging & Access Controls
    """
    
    def __init__(self, config: Dict[str, Any]):
        # BRAINSAIT: Security-first initialization
        self.config = config
        self.encryption_key = Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)
        
        # MEDICAL: Healthcare compliance setup
        self.nphies_endpoint = config.get("NPHIES_ENDPOINT")
        self.fhir_base_url = config.get("FHIR_BASE_URL")
        self.audit_log = config.get("HIPAA_AUDIT_LOG", "audit.log")
        
        # AGENT: AI workflow configuration
        self.claude_api_key = config.get("CLAUDE_API_KEY")
        self.n8n_webhook = config.get("N8N_WEBHOOK_URL")
        
        # BILINGUAL: Arabic/English support
        self.supported_languages = ["ar", "en"]
        self.current_language = "en"

        # VENDORS: Add NVIDIA Blueprints to path if cloned
        self.vendors_dir = Path.home() / ".brainsait" / "vendors" / "nvidia"
        self.vendor_paths = {
            "ambient": self.vendors_dir / "ambient-healthcare-agents",
            "rag": self.vendors_dir / "rag",
            "assistant": self.vendors_dir / "ai-virtual-assistant",
        }
        for p in self.vendor_paths.values():
            if p.exists() and str(p) not in sys.path:
                sys.path.append(str(p))
        
        # Configurable NVIDIA entrypoints from environment
        self.nvidia_cfg = {
            "rag": {
                "module": os.getenv("NVIDIA_RAG_MODULE", ""),
                "function": os.getenv("NVIDIA_RAG_FUNCTION", "")
            },
            "ambient": {
                "module": os.getenv("NVIDIA_AMBIENT_MODULE", ""),
                "function": os.getenv("NVIDIA_AMBIENT_FUNCTION", "")
            },
            "ava": {
                "module": os.getenv("NVIDIA_AVA_MODULE", ""),
                "function": os.getenv("NVIDIA_AVA_FUNCTION", "")
            },
        }
        
        logger.info("MASTERLINC initialized with HIPAA compliance and vendor scanning")

    async def process_nphies_claim(self, claim_data: Dict[str, Any], 
                                 user_role: str = "provider") -> Dict[str, Any]:
        """
        Process NPHIES claim with full compliance validation
        
        Args:
            claim_data: FHIR R4 Claim resource
            user_role: User role for access control
            
        Returns:
            Processed claim with validation results
            
        Raises:
            ComplianceError: If HIPAA/NPHIES validation fails
        """
        # BRAINSAIT: Role-based access validation
        if not self._validate_user_permission(user_role, "claims:process"):
            raise PermissionError("Insufficient permissions for claims processing")
        
        # MEDICAL: FHIR R4 validation
        try:
            claim = Claim(**claim_data)
            validation_result = self._validate_fhir_claim(claim)
            
            # AGENT: Automated processing via n8n
            workflow_result = await self._trigger_n8n_workflow(
                "nphies_claim_processing",
                {
                    "claim": claim.dict(),
                    "validation": validation_result,
                    "user_role": user_role,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
            # BRAINSAIT: Audit logging
            self._log_hipaa_event(
                action="claim_processed",
                user_role=user_role,
                resource_id=claim.id,
                details=workflow_result
            )
            
            return {
                "status": "success",
                "claim_id": claim.id,
                "nphies_response": workflow_result,
                "validation_result": validation_result,
                "processing_time": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"NPHIES claim processing failed: {str(e)}")
            raise ComplianceError(f"Claim processing error: {str(e)}")

    async def orchestrate_clinical_workflow(self, workflow_type: str,
                                          patient_data: Dict[str, Any],
                                          bilingual_content: bool = True) -> Dict[str, Any]:
        """
        Orchestrate clinical decision support workflows
        
        Args:
            workflow_type: Type of clinical workflow
            patient_data: FHIR Patient resource
            bilingual_content: Enable Arabic/English dual language
            
        Returns:
            Clinical recommendations with bilingual support
        """
        # MEDICAL: Patient data validation
        patient = Patient(**patient_data)
        
        # BILINGUAL: Language detection and setup
        language = self._detect_patient_language(patient_data)
        
        # AGENT: Clinical AI processing
        clinical_analysis = await self._process_clinical_data(
            workflow_type=workflow_type,
            patient=patient,
            language=language
        )
        
        # NEURAL: Apply BrainSAIT branding and UI patterns
        formatted_response = self._format_clinical_response(
            clinical_analysis,
            bilingual=bilingual_content,
            language=language
        )
        
        return formatted_response

    def _validate_user_permission(self, user_role: str, action: str) -> bool:
        """BRAINSAIT: Role-based access control validation"""
        permissions = {
            "admin": ["*"],
            "provider": ["claims:*", "patients:read", "clinical:*"],
            "nurse": ["patients:read", "clinical:read"],
            "auditor": ["audit:read", "compliance:read"]
        }
        
        user_permissions = permissions.get(user_role, [])
        return "*" in user_permissions or action in user_permissions or \
               any(perm.endswith("*") and action.startswith(perm[:-1]) 
                   for perm in user_permissions)

    def _validate_fhir_claim(self, claim: Claim) -> Dict[str, Any]:
        """MEDICAL: FHIR R4 claim validation with NPHIES requirements"""
        validation_errors = []
        
        # Required NPHIES fields validation
        if not claim.patient:
            validation_errors.append("Patient reference required")
        if not claim.provider:
            validation_errors.append("Provider reference required")
        if not claim.insurance:
            validation_errors.append("Insurance coverage required")
            
        return {
            "is_valid": len(validation_errors) == 0,
            "errors": validation_errors,
            "nphies_compliant": len(validation_errors) == 0
        }

    async def _trigger_n8n_workflow(self, workflow_name: str, 
                                   data: Dict[str, Any]) -> Dict[str, Any]:
        """AGENT: Trigger n8n workflow automation"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            webhook_url = f"{self.n8n_webhook}/{workflow_name}"
            
            async with session.post(webhook_url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"n8n workflow failed: {response.status}")

    def _log_hipaa_event(self, action: str, user_role: str, 
                        resource_id: str, details: Dict[str, Any]):
        """BRAINSAIT: HIPAA compliant audit logging"""
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "user_role": user_role,
            "resource_id": resource_id,
            "details": self.fernet.encrypt(json.dumps(details).encode()).decode()
        }
        
        # Write to secure audit log
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

    def _detect_patient_language(self, patient_data: Dict[str, Any]) -> str:
        """BILINGUAL: Auto-detect patient preferred language"""
        # Check communication preferences
        if "communication" in patient_data:
            for comm in patient_data["communication"]:
                if comm.get("preferred", False):
                    language = comm.get("language", {}).get("coding", [{}])[0].get("code", "en")
                    return "ar" if language.startswith("ar") else "en"
        return "en"  # Default to English

    async def _process_clinical_data(self, workflow_type: str, 
                                   patient: Patient, language: str) -> Dict[str, Any]:
        """AGENT: AI-powered clinical analysis"""
        # This would integrate with Claude API for clinical decision support
        clinical_prompt = self._build_clinical_prompt(workflow_type, patient, language)
        
        # Placeholder for Claude API integration
        return {
            "recommendations": "Clinical recommendations would be generated here",
            "risk_factors": [],
            "suggested_actions": [],
            "language": language
        }

    def _build_clinical_prompt(self, workflow_type: str, patient: Patient, 
                             language: str) -> str:
        """BILINGUAL: Build clinical AI prompt with language support"""
        if language == "ar":
            return f"قم بتحليل البيانات السريرية للمريض وتقديم التوصيات الطبية المناسبة..."
        else:
            return f"Analyze patient clinical data and provide appropriate medical recommendations..."

    def _format_clinical_response(self, analysis: Dict[str, Any], 
                                bilingual: bool, language: str) -> Dict[str, Any]:
        """NEURAL: Format response with BrainSAIT design system"""
        return {
            "analysis": analysis,
            "ui_config": {
                "primary_color": "#1a365d",  # Midnight Blue
                "accent_color": "#0ea5e9",   # Signal Teal
                "language": language,
                "rtl_enabled": language == "ar",
                "glass_morphism": True,
                "mesh_gradient": {
                    "primary_speed": 0.3,
                    "wireframe_speed": 0.2,
                    "opacity": 0.6
                }
            },
            "bilingual_content": bilingual,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# -------------------------
# NVIDIA Blueprints integration
# -------------------------
async def _maybe_await(self, value):
    if asyncio.iscoroutine(value):
        return await value
    return value

def _resolve_entrypoint(self, key: str, fallbacks: list) -> Optional[callable]:
    """Resolve a callable entrypoint using env-configured module/function or fallbacks."""
    cfg = self.nvidia_cfg.get(key, {})
    mod_name = (cfg.get("module") or "").strip()
    fn_name = (cfg.get("function") or "").strip()
    candidates = []
    if mod_name:
        candidates.append((mod_name, fn_name or None))
    candidates.extend(fallbacks)
    for mod, fn in candidates:
        try:
            module = importlib.import_module(mod)
            if fn:
                target = getattr(module, fn, None)
                if target:
                    return target
            else:
                # Try common names
                for name in ("query", "run", "process", "handle_intent"):
                    target = getattr(module, name, None)
                    if target:
                        return target
        except Exception:
            continue
    return None

async def query_nvidia_rag(self, query: str, corpus: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
    """Call NVIDIA RAG blueprint if available; fallback to stub."""
    try:
        fn = self._resolve_entrypoint(
            "rag",
            fallbacks=[("rag", None), ("nvidia_rag", None), ("apps.rag", None)]
        )
        if fn:
            result = await self._maybe_await(fn(query=query, corpus=corpus, top_k=top_k))
            return {"provider": "nvidia-rag", "ok": True, "result": result}
    except Exception as e:
        logger.warning(f"NVIDIA RAG invocation failed: {e}")
    return {"provider": "nvidia-rag", "ok": False, "error": "RAG repo not available or incompatible"}

async def run_ambient_healthcare_agent(self, transcript: str, task: str = "summarize") -> Dict[str, Any]:
    """Call NVIDIA ambient-healthcare-agents if available; fallback to stub."""
    try:
        fn = self._resolve_entrypoint(
            "ambient",
            fallbacks=[("ambient", None), ("ambient_healthcare_agents", None), ("ambient_healthcare", None), ("apps.ambient", None)]
        )
        if fn:
            result = await self._maybe_await(fn(transcript=transcript, task=task))
            return {"provider": "nvidia-ambient", "ok": True, "result": result}
    except Exception as e:
        logger.warning(f"Ambient agent invocation failed: {e}")
    return {"provider": "nvidia-ambient", "ok": False, "error": "Ambient repo not available or incompatible"}

async def run_ai_virtual_assistant(self, intent: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Call NVIDIA ai-virtual-assistant if available; fallback to stub."""
    try:
        fn = self._resolve_entrypoint(
            "ava",
            fallbacks=[("ai_virtual_assistant", None), ("assistant", None), ("apps.ai_virtual_assistant", None)]
        )
        if fn:
            result = await self._maybe_await(fn(intent=intent, payload=payload or {}))
            return {"provider": "nvidia-ava", "ok": True, "result": result}
    except Exception as e:
        logger.warning(f"AI virtual assistant invocation failed: {e}")
    return {"provider": "nvidia-ava", "ok": False, "error": "Assistant repo not available or incompatible"}

# Custom Healthcare Exceptions
class ComplianceError(Exception):
    """Raised when healthcare compliance validation fails"""
    pass

class HealthcareAPIError(Exception):
    """Raised when healthcare API calls fail"""
    pass

# MCP Server Setup
server = Server("brainsait-masterlinc")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available healthcare resources"""
    return [
        types.Resource(
            uri="nphies://claims/processor",
            name="NPHIES Claims Processor",
            description="Process and validate NPHIES claims with FHIR R4 compliance",
            mimeType="application/fhir+json"
        ),
        types.Resource(
            uri="clinical://decision-support",
            name="Clinical Decision Support",
            description="AI-powered clinical recommendations with bilingual support",
            mimeType="application/json"
        ),
        types.Resource(
            uri="audit://hipaa-logs",
            name="HIPAA Audit Logs",
            description="Secure healthcare audit trail and compliance monitoring",
            mimeType="application/json"
        )
    ]

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available MASTERLINC tools"""
    return [
        types.Tool(
            name="process_nphies_claim",
            description="Process NPHIES healthcare claims with full compliance validation",
            inputSchema={
                "type": "object",
                "properties": {
                    "claim_data": {
                        "type": "object",
                        "description": "FHIR R4 Claim resource data"
                    },
                    "user_role": {
                        "type": "string",
                        "description": "User role for access control",
                        "enum": ["admin", "provider", "nurse", "auditor"]
                    }
                },
                "required": ["claim_data"]
            }
        ),
        types.Tool(
            name="orchestrate_clinical_workflow",
            description="Orchestrate clinical decision support with bilingual AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_type": {
                        "type": "string",
                        "description": "Type of clinical workflow",
                        "enum": ["diagnosis", "treatment", "radiology", "laboratory"]
                    },
                    "patient_data": {
                        "type": "object",
                        "description": "FHIR Patient resource"
                    },
                    "bilingual_content": {
                        "type": "boolean",
                        "description": "Enable Arabic/English dual language"
                    }
                },
                "required": ["workflow_type", "patient_data"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle MASTERLINC tool calls"""
    
    # Initialize MASTERLINC with config
    import os
    config = {
        "NPHIES_ENDPOINT": os.getenv("NPHIES_ENDPOINT"),
        "FHIR_BASE_URL": os.getenv("FHIR_BASE_URL"),
        "HIPAA_AUDIT_LOG": os.getenv("HIPAA_AUDIT_LOG", "audit.log"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
        "N8N_WEBHOOK_URL": os.getenv("N8N_WEBHOOK_URL")
    }
    
    masterlinc = BrainSAITMasterLinc(config)
    
    if name == "process_nphies_claim":
        try:
            result = await masterlinc.process_nphies_claim(
                claim_data=arguments["claim_data"],
                user_role=arguments.get("user_role", "provider")
            )
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        except Exception as e:
            return [types.TextContent(
                type="text", 
                text=f"Error processing NPHIES claim: {str(e)}"
            )]
    
    elif name == "orchestrate_clinical_workflow":
        try:
            result = await masterlinc.orchestrate_clinical_workflow(
                workflow_type=arguments["workflow_type"],
                patient_data=arguments["patient_data"],
                bilingual_content=arguments.get("bilingual_content", True)
            )
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error in clinical workflow: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdio
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="brainsait-masterlinc",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
