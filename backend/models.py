from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class GovernanceMode(str, Enum):
    AUTO_DOWNSCALE_REWRITE = "AUTO_DOWNSCALE_REWRITE"
    THROTTLE_AND_EDUCATE = "THROTTLE_AND_EDUCATE"
    REALLOCATE_QUOTA = "REALLOCATE_QUOTA"

class MCPLoopRiskChoice(str, Enum):
    CLEAN_EXECUTION = "CLEAN_EXECUTION"
    TOOL_RETRY_STORM = "TOOL_RETRY_STORM"
    UNBOUNDED_GREP = "UNBOUNDED_GREP"
    SCHEMA_POLLUTION = "SCHEMA_POLLUTION"

class TrophicTier(str, Enum):
    MEGAHERBIVORE = "MEGAHERBIVORE"
    MESOHERBIVORE = "MESOHERBIVORE"
    MICROFORAGER = "MICROFORAGER"

class JevNoul(BaseModel):
    verdict: bool = Field(..., description="Discrete boolean decision")
    probability: float = Field(..., ge=0.0, le=1.0, description="Posterior probability p")
    confidence_interval: float = Field(..., ge=0.0, le=1.0, description="Epistemic confidence interval")
    rubric_id: str = Field(..., description="Edge rubric identifier")

class CausalNode(BaseModel):
    id: str
    label: str
    node_type: str
    status: str
    metadata: Dict[str, Any] = {}

class CausalEdge(BaseModel):
    source: str
    target: str
    relation: str

class JevBehavioralVerdict(BaseModel):
    session_id: str
    user_id: str
    user_name: str
    department: str
    current_model: str
    recommended_model: str
    trophic_tier_current: TrophicTier
    trophic_tier_recommended: TrophicTier
    tokens_burned: int
    cost_incurred_usd: float
    cost_with_zero_dog_usd: float
    datadog_span_fee_saved_usd: float
    model_overkill: JevNoul
    mcp_loop_risk: MCPLoopRiskChoice
    prompt_craft_score: float = Field(..., ge=0.0, le=100.0)
    detected_antipattern: str
    ecological_diagnosis: str
    prompt_preview: str
    mcp_tool_chain: List[str]

class UserQuotaProfile(BaseModel):
    user_id: str
    name: str
    department: str
    avatar_emoji: str
    daily_quota_usd: float
    current_spend_usd: float
    efficiency_rank: str
    prompt_craft_index: float
    reputation_score: int
    bonus_tokens_awarded_usd: float = 0.0
    penalties_incurred_usd: float = 0.0

class SafetyInterceptStatus(BaseModel):
    intercept_active: bool
    authorized_job_id: Optional[str] = None
    authorized_job_name: Optional[str] = None
    ecological_analogy: Optional[str] = None
    reason_description: Optional[str] = None
    risk_if_throttled: Optional[str] = None
    override_allowed: bool = True

class IncidentBundle(BaseModel):
    incident_id: str
    title: str
    subtitle: str
    status: str
    verdict: JevBehavioralVerdict
    safety_intercept: SafetyInterceptStatus
    nodes: List[CausalNode]
    edges: List[CausalEdge]
    claude_optimized_prompt: str
    claude_coaching_notes: str
    active_governance_mode: GovernanceMode = GovernanceMode.AUTO_DOWNSCALE_REWRITE
    remediated: bool = False

class GlobalStateResponse(BaseModel):
    total_tokens_monitored: int
    total_spend_incurred_usd: float
    net_zerodog_savings_usd: float
    datadog_fees_eliminated_usd: float
    trophic_efficiency_ratio: float
    active_incidents: List[IncidentBundle]
    users: List[UserQuotaProfile]
    current_incident_id: str

class GovernanceExecutionRequest(BaseModel):
    incident_id: str
    mode: GovernanceMode
    force_override: bool = False

class GovernanceExecutionResponse(BaseModel):
    success: bool
    incident_id: str
    mode: GovernanceMode
    new_status: str
    action_receipt_markdown: str
    dollars_saved_immediate: float
    reallocation_details: Optional[Dict[str, Any]] = None

class ChallengeAnalyzeRequest(BaseModel):
    prompt_text: str
    target_model: Optional[str] = "claude-3-opus"
    mcp_tools_text: Optional[str] = ""

class ChallengeAnalyzeResponse(BaseModel):
    jev_overkill: JevNoul
    mcp_loop_risk: MCPLoopRiskChoice
    prompt_craft_score: float
    trophic_verdict: str
    projected_daily_waste_usd: float
    optimized_cost_usd: float
    savings_percentage: float
    claude_optimized_rewrite: str
    ecological_diagnosis: str
