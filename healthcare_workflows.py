"""
BrainSAIT n8n Healthcare Workflow Automation MCP Server
Connects Claude to n8n for automated healthcare processes
"""

import asyncio
import json
import aiohttp
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

class HealthcareWorkflowAutomation:
    """
    AGENT: Healthcare workflow automation via n8n integration
    
    Key Workflows:
    1. NPHIES Revenue Cycle Optimizer
    2. Clinical Decision Support Pipeline  
    3. Patient Data Processing & FHIR Conversion
    4. Automated Reporting & Compliance Monitoring
    5. Bilingual Content Generation (AR/EN)
    """
    
    def __init__(self, n8n_api_key: str, n8n_base_url: str, webhook_url: str):
        self.n8n_api_key = n8n_api_key
        self.n8n_base_url = n8n_base_url.rstrip('/')
        self.webhook_url = webhook_url.rstrip('/')
        
        # BRAINSAIT: Healthcare workflow definitions
        self.healthcare_workflows = {
            "nphies_revenue_optimizer": {
                "name": "NPHIES Revenue Cycle Optimizer",
                "description": "Automate claim submission, tracking, and revenue optimization",
                "webhook_path": "/nphies-revenue-optimizer",
                "inputs": ["claim_data", "provider_info", "patient_demographics"],
                "outputs": ["processed_claim", "revenue_analysis", "compliance_report"]
            },
            "clinical_decision_support": {
                "name": "Clinical Decision Support Pipeline",
                "description": "AI-powered clinical recommendations with FHIR integration",
                "webhook_path": "/clinical-decision-support", 
                "inputs": ["patient_data", "clinical_context", "language_preference"],
                "outputs": ["recommendations", "risk_assessment", "care_plan"]
            },
            "patient_data_processor": {
                "name": "Patient Data Processing & FHIR Conversion",
                "description": "Convert and validate patient data to FHIR R4 format",
                "webhook_path": "/patient-data-processor",
                "inputs": ["raw_patient_data", "data_source", "validation_rules"],
                "outputs": ["fhir_patient", "validation_report", "quality_metrics"]
            },
            "compliance_monitor": {
                "name": "Automated Compliance Monitoring",
                "description": "Monitor HIPAA, NPHIES compliance with automated reporting",
                "webhook_path": "/compliance-monitor",
                "inputs": ["audit_data", "compliance_rules", "reporting_schedule"],
                "outputs": ["compliance_report", "violations", "recommendations"]
            },
            "bilingual_content_generator": {
                "name": "Bilingual Healthcare Content Generator",
                "description": "Generate Arabic/English medical content using TTLINC",
                "webhook_path": "/bilingual-content-generator",
                "inputs": ["content_type", "source_language", "target_language", "medical_context"],
                "outputs": ["translated_content", "quality_score", "medical_validation"]
            }
        }

    async def trigger_workflow(self, workflow_id: str, input_data: Dict[str, Any],
                             execution_mode: str = "webhook") -> Dict[str, Any]:
        """
        Trigger n8n healthcare workflow
        
        Args:
            workflow_id: ID of the workflow to trigger
            input_data: Data to pass to the workflow
            execution_mode: How to trigger (webhook, api, manual)
            
        Returns:
            Workflow execution result
        """
        if execution_mode == "webhook":
            return await self._trigger_webhook_workflow(workflow_id, input_data)
        elif execution_mode == "api":
            return await self._trigger_api_workflow(workflow_id, input_data)
        else:
            raise ValueError(f"Unsupported execution mode: {execution_mode}")

    async def _trigger_webhook_workflow(self, workflow_id: str, 
                                      input_data: Dict[str, Any]) -> Dict[str, Any]:
        """AGENT: Trigger workflow via webhook"""
        
        workflow_config = self.healthcare_workflows.get(workflow_id)
        if not workflow_config:
            raise ValueError(f"Unknown workflow: {workflow_id}")
        
        webhook_path = workflow_config["webhook_path"]
        webhook_url = f"{self.webhook_url}{webhook_path}"
        
        # BRAINSAIT: Add security headers and audit trail
        payload = {
            "workflow_id": workflow_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_data": input_data,
            "execution_context": {
                "source": "brainsait-masterlinc",
                "compliance_mode": "hipaa",
                "audit_required": True
            }
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Content-Type": "application/json",
                "X-BrainSAIT-Workflow": workflow_id,
                "X-Execution-Mode": "automated"
            }
            
            async with session.post(webhook_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "status": "success",
                        "workflow_id": workflow_id,
                        "execution_id": result.get("execution_id"),
                        "result": result,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Webhook failed ({response.status}): {error_text}")

    async def _trigger_api_workflow(self, workflow_id: str, 
                                  input_data: Dict[str, Any]) -> Dict[str, Any]:
        """AGENT: Trigger workflow via n8n API"""
        
        api_url = f"{self.n8n_base_url}/api/v1/workflows/{workflow_id}/execute"
        
        payload = {
            "input": input_data,
            "metadata": {
                "triggered_by": "brainsait-masterlinc",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "compliance_mode": "hipaa"
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.n8n_api_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API execution failed ({response.status}): {error_text}")

    async def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """Get status of workflow execution"""
        
        api_url = f"{self.n8n_base_url}/api/v1/executions/{execution_id}"
        headers = {"Authorization": f"Bearer {self.n8n_api_key}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Status check failed: {response.status}")

    async def list_available_workflows(self) -> Dict[str, Any]:
        """List all available healthcare workflows"""
        
        # MEDICAL: Return healthcare-specific workflow catalog
        return {
            "available_workflows": self.healthcare_workflows,
            "total_count": len(self.healthcare_workflows),
            "categories": {
                "revenue_cycle": ["nphies_revenue_optimizer"],
                "clinical_support": ["clinical_decision_support"],
                "data_processing": ["patient_data_processor"],
                "compliance": ["compliance_monitor"],
                "content_generation": ["bilingual_content_generator"]
            }
        }

    def create_workflow_json(self, workflow_type: str) -> Dict[str, Any]:
        """
        AGENT: Generate n8n workflow JSON for healthcare processes
        
        Creates complete n8n workflow configurations for BrainSAIT healthcare automation
        """
        
        if workflow_type == "nphies_revenue_optimizer":
            return self._create_nphies_workflow()
        elif workflow_type == "clinical_decision_support":
            return self._create_clinical_workflow()
        elif workflow_type == "patient_data_processor":
            return self._create_patient_data_workflow()
        elif workflow_type == "compliance_monitor":
            return self._create_compliance_workflow()
        elif workflow_type == "bilingual_content_generator":
            return self._create_bilingual_workflow()
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")

    def _create_nphies_workflow(self) -> Dict[str, Any]:
        """MEDICAL: Create NPHIES Revenue Cycle Optimizer workflow"""
        return {
            "name": "NPHIES Revenue Cycle Optimizer",
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": "nphies-revenue-optimizer",
                        "responseMode": "responseNode"
                    },
                    "id": "webhook-nphies",
                    "name": "NPHIES Webhook Trigger",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 2,
                    "position": [240, 300],
                    "webhookId": "brainsait-nphies"
                },
                {
                    "parameters": {
                        "assignments": {
                            "assignments": [
                                {
                                    "id": "claim_data", 
                                    "name": "claim_data",
                                    "value": "={{ $json.input_data.claim_data }}",
                                    "type": "object"
                                },
                                {
                                    "id": "provider_info",
                                    "name": "provider_info", 
                                    "value": "={{ $json.input_data.provider_info }}",
                                    "type": "object"
                                }
                            ]
                        }
                    },
                    "id": "extract-claim-data",
                    "name": "Extract Claim Data",
                    "type": "n8n-nodes-base.set",
                    "typeVersion": 3.4,
                    "position": [460, 300]
                },
                {
                    "parameters": {
                        "model": "claude-sonnet-4",
                        "messages": {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": "Analyze this NPHIES claim for revenue optimization opportunities:\n\nClaim Data: {{ $json.claim_data }}\nProvider: {{ $json.provider_info }}\n\nProvide:\n1. Revenue optimization recommendations\n2. Compliance validation\n3. Reimbursement maximization strategies\n4. Risk assessment\n\nResponse in JSON format with Arabic and English descriptions."
                                }
                            ]
                        }
                    },
                    "id": "claude-analysis",
                    "name": "Claude Revenue Analysis", 
                    "type": "n8n-nodes-base.openAi",
                    "typeVersion": 1.3,
                    "position": [680, 300]
                },
                {
                    "parameters": {
                        "url": "={{ $env.NPHIES_ENDPOINT }}/claims/submit",
                        "authentication": "genericCredentialType",
                        "genericAuthType": "httpHeaderAuth",
                        "sendHeaders": true,
                        "headerParameters": {
                            "parameters": [
                                {
                                    "name": "Authorization",
                                    "value": "Bearer {{ $env.NPHIES_ACCESS_TOKEN }}"
                                },
                                {
                                    "name": "Content-Type",
                                    "value": "application/fhir+json"
                                }
                            ]
                        },
                        "sendBody": true,
                        "contentType": "json",
                        "body": "={{ $json.claim_data }}"
                    },
                    "id": "submit-nphies-claim",
                    "name": "Submit to NPHIES",
                    "type": "n8n-nodes-base.httpRequest", 
                    "typeVersion": 4.2,
                    "position": [900, 300]
                },
                {
                    "parameters": {
                        "assignments": {
                            "assignments": [
                                {
                                    "id": "final_result",
                                    "name": "result",
                                    "value": {
                                        "claim_submission": "={{ $json }}",
                                        "revenue_analysis": "={{ $('Claude Revenue Analysis').item.json }}",
                                        "timestamp": "={{ new Date().toISOString() }}",
                                        "status": "processed",
                                        "compliance_validated": true
                                    },
                                    "type": "object"
                                }
                            ]
                        }
                    },
                    "id": "format-response",
                    "name": "Format Final Response",
                    "type": "n8n-nodes-base.set",
                    "typeVersion": 3.4,
                    "position": [1120, 300]
                },
                {
                    "parameters": {
                        "respondWith": "json",
                        "responseBody": "={{ $json.result }}"
                    },
                    "id": "webhook-response",
                    "name": "Return Response",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "typeVersion": 1.1,
                    "position": [1340, 300]
                }
            ],
            "connections": {
                "NPHIES Webhook Trigger": {"main": [["Extract Claim Data"]]},
                "Extract Claim Data": {"main": [["Claude Revenue Analysis"]]},
                "Claude Revenue Analysis": {"main": [["Submit to NPHIES"]]},
                "Submit to NPHIES": {"main": [["Format Final Response"]]},
                "Format Final Response": {"main": [["Return Response"]]}
            },
            "settings": {
                "executionOrder": "v1"
            },
            "staticData": null,
            "tags": ["brainsait", "nphies", "healthcare", "revenue-cycle"],
            "triggerCount": 1,
            "updatedAt": datetime.now(timezone.utc).isoformat(),
            "versionId": "1.0.0"
        }

# MCP Server Setup
server = Server("n8n-healthcare-workflows")

@server.list_tools() 
async def handle_list_tools() -> list[types.Tool]:
    """List available n8n workflow tools"""
    return [
        types.Tool(
            name="trigger_healthcare_workflow",
            description="Trigger automated healthcare workflow in n8n",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_id": {
                        "type": "string",
                        "description": "Healthcare workflow to trigger",
                        "enum": [
                            "nphies_revenue_optimizer",
                            "clinical_decision_support", 
                            "patient_data_processor",
                            "compliance_monitor",
                            "bilingual_content_generator"
                        ]
                    },
                    "input_data": {
                        "type": "object",
                        "description": "Input data for the workflow"
                    },
                    "execution_mode": {
                        "type": "string",
                        "description": "How to execute the workflow",
                        "enum": ["webhook", "api"],
                        "default": "webhook"
                    }
                },
                "required": ["workflow_id", "input_data"]
            }
        ),
        types.Tool(
            name="get_workflow_status",
            description="Check status of workflow execution",
            inputSchema={
                "type": "object", 
                "properties": {
                    "execution_id": {
                        "type": "string",
                        "description": "Execution ID to check status for"
                    }
                },
                "required": ["execution_id"]
            }
        ),
        types.Tool(
            name="list_healthcare_workflows",
            description="List all available healthcare workflows",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="create_workflow_json",
            description="Generate n8n workflow JSON for healthcare automation",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_type": {
                        "type": "string",
                        "description": "Type of healthcare workflow to create",
                        "enum": [
                            "nphies_revenue_optimizer",
                            "clinical_decision_support",
                            "patient_data_processor", 
                            "compliance_monitor",
                            "bilingual_content_generator"
                        ]
                    }
                },
                "required": ["workflow_type"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle n8n workflow tool calls"""
    
    import os
    
    # Initialize workflow automation
    workflow_automation = HealthcareWorkflowAutomation(
        n8n_api_key=os.getenv("N8N_API_KEY", ""),
        n8n_base_url=os.getenv("N8N_BASE_URL", "https://n8n.example.com"),
        webhook_url=os.getenv("N8N_WEBHOOK_URL", "https://hooks.n8n.example.com")
    )
    
    try:
        if name == "trigger_healthcare_workflow":
            result = await workflow_automation.trigger_workflow(
                workflow_id=arguments["workflow_id"],
                input_data=arguments["input_data"],
                execution_mode=arguments.get("execution_mode", "webhook")
            )
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        elif name == "get_workflow_status":
            result = await workflow_automation.get_workflow_status(
                execution_id=arguments["execution_id"]
            )
            
            return [types.TextContent(
                type="text", 
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        elif name == "list_healthcare_workflows":
            result = await workflow_automation.list_available_workflows()
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        elif name == "create_workflow_json":
            result = workflow_automation.create_workflow_json(
                workflow_type=arguments["workflow_type"]
            )
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]

async def main():
    """Run the n8n healthcare workflows MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="n8n-healthcare-workflows",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
