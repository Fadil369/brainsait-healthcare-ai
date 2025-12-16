#!/usr/bin/env python3
"""
BrainSAIT NPHIES Compliance MCP Server
Handles Saudi NPHIES (National Platform for Health Information Exchange and Services) compliance
Part of BrainSAIT healthcare AI platform

BRAINSAIT: NPHIES compliance with Arabic/English bilingual support
MEDICAL: FHIR R4 validation and NPHIES-specific requirements
NEURAL: BrainSAIT branded responses with professional styling
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import aiohttp
from cryptography.fernet import Fernet
import hashlib

# MCP imports
from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    Prompt,
    PromptMessage,
)

# FHIR validation
from fhir.resources import Bundle, Claim, Patient, Organization, Practitioner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPHIESComplianceError(Exception):
    """Custom exception for NPHIES compliance violations"""
    pass

class BrainSAITNPHIESCompliance:
    """
    NPHIES Compliance Handler for Saudi Healthcare
    
    Handles:
    - NPHIES claim validation and submission
    - Saudi MOH compliance requirements
    - Arabic/English bilingual documentation
    - FHIR R4 resource validation for NPHIES
    - Revenue cycle optimization
    """
    
    def __init__(self):
        # BRAINSAIT: Load environment variables with security
        self.nphies_endpoint = os.getenv("NPHIES_ENDPOINT", "https://nphies.sa.gov.sa/api/v1")
        self.client_id = os.getenv("NPHIES_CLIENT_ID")
        self.client_secret = os.getenv("NPHIES_CLIENT_SECRET")
        self.access_token = os.getenv("NPHIES_ACCESS_TOKEN")
        self.moh_endpoint = os.getenv("SAUDI_MOH_ENDPOINT", "https://moh.gov.sa/api")
        
        # MEDICAL: FHIR and encryption setup
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        if self.encryption_key:
            self.cipher = Fernet(self.encryption_key.encode())
        
        # NEURAL: Audit logging for HIPAA compliance
        self.audit_log_path = os.getenv("HIPAA_AUDIT_LOG", "/var/log/brainsait/nphies_audit.log")
        
        # BILINGUAL: Support for Arabic content
        self.arabic_locale = "ar-SA"
        self.default_locale = "en-US"
        
    async def validate_nphies_claim(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate FHIR claim against NPHIES requirements
        
        Args:
            claim_data: FHIR R4 Claim resource as dictionary
            
        Returns:
            Dict with validation results and compliance status
            
        Raises:
            NPHIESComplianceError: If critical compliance issues found
        """
        try:
            # MEDICAL: Validate FHIR R4 structure
            claim = Claim(**claim_data)
            
            # BRAINSAIT: NPHIES-specific validation rules
            validation_results = {
                "is_compliant": True,
                "validation_errors": [],
                "warnings": [],
                "nphies_requirements_met": [],
                "arabic_content_valid": True,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Required NPHIES fields validation
            required_fields = [
                "identifier", "status", "type", "patient", "provider",
                "priority", "procedure", "insurance", "total"
            ]
            
            for field in required_fields:
                if not hasattr(claim, field) or getattr(claim, field) is None:
                    validation_results["validation_errors"].append({
                        "field": field,
                        "error": f"Required NPHIES field '{field}' is missing",
                        "severity": "error",
                        "arabic_message": f"الحقل المطلوب '{field}' مفقود في نظام نفيس"
                    })
                    validation_results["is_compliant"] = False
            
            # NPHIES identifier format validation
            if hasattr(claim, 'identifier') and claim.identifier:
                for identifier in claim.identifier:
                    if identifier.system == "https://nphies.sa":
                        validation_results["nphies_requirements_met"].append("NPHIES identifier present")
                    else:
                        validation_results["warnings"].append({
                            "field": "identifier.system",
                            "warning": "NPHIES identifier system should be 'https://nphies.sa'",
                            "arabic_message": "نظام التعريف يجب أن يكون 'https://nphies.sa'"
                        })
            
            # Saudi-specific validation
            if hasattr(claim, 'patient') and claim.patient:
                # Validate Saudi ID format (10 digits starting with 1 or 2)
                patient_id = str(claim.patient.reference) if claim.patient.reference else ""
                if not self._validate_saudi_id(patient_id):
                    validation_results["validation_errors"].append({
                        "field": "patient.identifier",
                        "error": "Invalid Saudi national ID format",
                        "severity": "error",
                        "arabic_message": "تنسيق رقم الهوية الوطنية السعودية غير صالح"
                    })
                    validation_results["is_compliant"] = False
            
            # NEURAL: Log validation attempt with audit trail
            await self._audit_log("nphies_validation", {
                "claim_id": getattr(claim, 'id', 'unknown'),
                "validation_result": validation_results["is_compliant"],
                "timestamp": validation_results["timestamp"]
            })
            
            return validation_results
            
        except Exception as e:
            logger.error(f"NPHIES validation error: {str(e)}")
            raise NPHIESComplianceError(f"Failed to validate NPHIES claim: {str(e)}")
    
    async def submit_nphies_claim(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit validated claim to NPHIES platform
        
        Args:
            claim_data: Validated FHIR R4 Claim resource
            
        Returns:
            Dict with submission results and NPHIES response
        """
        try:
            # BRAINSAIT: Pre-submission validation
            validation_result = await self.validate_nphies_claim(claim_data)
            if not validation_result["is_compliant"]:
                return {
                    "success": False,
                    "error": "Claim failed NPHIES validation",
                    "validation_errors": validation_result["validation_errors"],
                    "arabic_message": "فشل في التحقق من صحة المطالبة في نظام نفيس"
                }
            
            # MEDICAL: Prepare NPHIES submission payload
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/fhir+json",
                "Accept": "application/fhir+json",
                "Accept-Language": "ar-SA,en-US"
            }
            
            # NEURAL: Submit to NPHIES endpoint
            async with aiohttp.ClientSession() as session:
                submission_url = f"{self.nphies_endpoint}/Claim"
                
                async with session.post(
                    submission_url,
                    headers=headers,
                    json=claim_data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    response_data = await response.json()
                    
                    result = {
                        "success": response.status == 201,
                        "status_code": response.status,
                        "nphies_response": response_data,
                        "submission_id": response_data.get("id"),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    
                    if response.status == 201:
                        result["message"] = "Claim successfully submitted to NPHIES"
                        result["arabic_message"] = "تم تقديم المطالبة بنجاح إلى نظام نفيس"
                        
                        # BRAINSAIT: Log successful submission
                        await self._audit_log("nphies_submission_success", {
                            "claim_id": claim_data.get("id"),
                            "submission_id": result["submission_id"],
                            "timestamp": result["timestamp"]
                        })
                    else:
                        result["error"] = f"NPHIES submission failed: {response_data.get('error', 'Unknown error')}"
                        result["arabic_message"] = f"فشل في تقديم المطالبة: {response_data.get('error', 'خطأ غير معروف')}"
                        
                        # NEURAL: Log submission failure
                        await self._audit_log("nphies_submission_failure", {
                            "claim_id": claim_data.get("id"),
                            "error": result["error"],
                            "status_code": response.status,
                            "timestamp": result["timestamp"]
                        })
                    
                    return result
                    
        except aiohttp.ClientError as e:
            error_msg = f"Network error submitting to NPHIES: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "arabic_message": f"خطأ في الشبكة عند التقديم لنظام نفيس: {str(e)}"
            }
        except Exception as e:
            error_msg = f"Unexpected error in NPHIES submission: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "arabic_message": f"خطأ غير متوقع في تقديم نظام نفيس: {str(e)}"
            }
    
    async def get_nphies_status(self, submission_id: str) -> Dict[str, Any]:
        """
        Check status of submitted NPHIES claim
        
        Args:
            submission_id: NPHIES submission identifier
            
        Returns:
            Dict with current claim status and processing details
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/fhir+json",
                "Accept-Language": "ar-SA,en-US"
            }
            
            async with aiohttp.ClientSession() as session:
                status_url = f"{self.nphies_endpoint}/Claim/{submission_id}"
                
                async with session.get(status_url, headers=headers) as response:
                    response_data = await response.json()
                    
                    if response.status == 200:
                        claim_status = response_data.get("status", "unknown")
                        
                        # BILINGUAL: Status mapping
                        status_mapping = {
                            "active": {"en": "Active", "ar": "نشط"},
                            "cancelled": {"en": "Cancelled", "ar": "ملغي"},
                            "draft": {"en": "Draft", "ar": "مسودة"},
                            "entered-in-error": {"en": "Entered in Error", "ar": "خطأ في الإدخال"}
                        }
                        
                        return {
                            "success": True,
                            "submission_id": submission_id,
                            "status": claim_status,
                            "status_display": status_mapping.get(claim_status, {"en": claim_status, "ar": claim_status}),
                            "last_updated": response_data.get("meta", {}).get("lastUpdated"),
                            "nphies_response": response_data,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to retrieve NPHIES status: {response.status}",
                            "arabic_message": f"فشل في استرداد حالة نظام نفيس: {response.status}"
                        }
                        
        except Exception as e:
            error_msg = f"Error checking NPHIES status: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "arabic_message": f"خطأ في فحص حالة نظام نفيس: {str(e)}"
            }
    
    def _validate_saudi_id(self, id_string: str) -> bool:
        """Validate Saudi national ID format (10 digits, starts with 1 or 2)"""
        if not id_string or len(id_string) != 10:
            return False
        
        if not id_string.isdigit():
            return False
            
        if not id_string.startswith(('1', '2')):
            return False
            
        # Luhn algorithm validation for Saudi ID
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        
        return luhn_checksum(id_string) == 0
    
    async def _audit_log(self, action: str, details: Dict[str, Any]):
        """HIPAA compliant audit logging"""
        try:
            audit_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": action,
                "details": details,
                "service": "brainsait-nphies-compliance",
                "user_agent": "BrainSAIT-MCP-Server/1.0"
            }
            
            # NEURAL: Encrypt sensitive audit data
            if self.cipher:
                encrypted_details = self.cipher.encrypt(json.dumps(details).encode())
                audit_entry["details_encrypted"] = encrypted_details.decode()
                del audit_entry["details"]
            
            # Write to audit log
            audit_line = json.dumps(audit_entry) + "\n"
            
            # Ensure audit log directory exists
            os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)
            
            with open(self.audit_log_path, "a") as audit_file:
                audit_file.write(audit_line)
                
        except Exception as e:
            logger.error(f"Failed to write audit log: {str(e)}")

# Initialize the MCP server
server = Server("brainsait-nphies-compliance")
nphies_handler = BrainSAITNPHIESCompliance()

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available NPHIES compliance tools"""
    return ListToolsResult(
        tools=[
            Tool(
                name="validate_nphies_claim",
                description="Validate FHIR R4 claim against NPHIES requirements with Arabic/English support",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "claim_data": {
                            "type": "object",
                            "description": "FHIR R4 Claim resource as JSON object"
                        }
                    },
                    "required": ["claim_data"]
                }
            ),
            Tool(
                name="submit_nphies_claim", 
                description="Submit validated claim to NPHIES platform in Saudi Arabia",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "claim_data": {
                            "type": "object",
                            "description": "Validated FHIR R4 Claim resource"
                        }
                    },
                    "required": ["claim_data"]
                }
            ),
            Tool(
                name="get_nphies_status",
                description="Check processing status of submitted NPHIES claim",
                inputSchema={
                    "type": "object", 
                    "properties": {
                        "submission_id": {
                            "type": "string",
                            "description": "NPHIES submission identifier"
                        }
                    },
                    "required": ["submission_id"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """Handle tool execution requests"""
    try:
        if request.name == "validate_nphies_claim":
            claim_data = request.arguments.get("claim_data")
            if not claim_data:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="Error: claim_data is required for NPHIES validation"
                    )]
                )
            
            result = await nphies_handler.validate_nphies_claim(claim_data)
            return CallToolResult(
                content=[TextContent(
                    type="text", 
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
            )
        
        elif request.name == "submit_nphies_claim":
            claim_data = request.arguments.get("claim_data")
            if not claim_data:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="Error: claim_data is required for NPHIES submission"
                    )]
                )
            
            result = await nphies_handler.submit_nphies_claim(claim_data)
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
            )
        
        elif request.name == "get_nphies_status":
            submission_id = request.arguments.get("submission_id")
            if not submission_id:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="Error: submission_id is required for NPHIES status check"
                    )]
                )
            
            result = await nphies_handler.get_nphies_status(submission_id)
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
            )
        
        else:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error: Unknown tool '{request.name}'"
                )]
            )
            
    except Exception as e:
        logger.error(f"Tool execution error: {str(e)}")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Error executing tool: {str(e)}"
            )]
        )

async def main():
    """Run the NPHIES compliance MCP server"""
    async with stdio_server(server, StdioServerParameters()) as (read, write):
        await server.run(read, write, InitializationOptions(
            server_name="brainsait-nphies-compliance",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=None,
                experimental_capabilities={}
            )
        ))

if __name__ == "__main__":
    asyncio.run(main())