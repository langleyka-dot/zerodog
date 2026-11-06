import json
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
from .models import (
    IncidentBundle,
    UserQuotaProfile,
    GlobalStateResponse,
    GovernanceMode,
    GovernanceExecutionResponse
)
from .cognee_graph import CausalMemoryGraph

class StateManager:
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            data_path = str(Path(__file__).parent.parent / "data" / "prebaked_governance.json")
        self.data_path = data_path
        self.lock = threading.Lock()
        self.metrics: Dict[str, Any] = {}
        self.users: Dict[str, UserQuotaProfile] = {}
        self.incidents: Dict[str, IncidentBundle] = {}
        self.current_incident_id: str = "AI-SPEND-101"
        self.graph = CausalMemoryGraph()
        self.reset()

    def reset(self):
        with self.lock:
            with open(self.data_path, "r") as f:
                raw = json.load(f)
            self.metrics = dict(raw["metrics"])
            self.users = {u["user_id"]: UserQuotaProfile(**u) for u in raw["users"]}
            self.incidents = {inc["incident_id"]: IncidentBundle(**inc) for inc in raw["incidents"]}
            self.current_incident_id = "AI-SPEND-101"
            active = self.incidents[self.current_incident_id]
            self.graph.load_from_incident(
                [n.dict() if hasattr(n, 'dict') else n.model_dump() for n in active.nodes],
                [e.dict() if hasattr(e, 'dict') else e.model_dump() for e in active.edges]
            )

    def get_state(self) -> GlobalStateResponse:
        with self.lock:
            return GlobalStateResponse(
                total_tokens_monitored=self.metrics["total_tokens_monitored"],
                total_spend_incurred_usd=round(self.metrics["total_spend_incurred_usd"], 2),
                net_zerodog_savings_usd=round(self.metrics["net_zerodog_savings_usd"], 2),
                datadog_fees_eliminated_usd=round(self.metrics["datadog_fees_eliminated_usd"], 2),
                trophic_efficiency_ratio=self.metrics["trophic_efficiency_ratio"],
                active_incidents=list(self.incidents.values()),
                users=list(self.users.values()),
                current_incident_id=self.current_incident_id
            )

    def set_current_incident(self, incident_id: str) -> Optional[IncidentBundle]:
        with self.lock:
            if incident_id in self.incidents:
                self.current_incident_id = incident_id
                inc = self.incidents[incident_id]
                self.graph.load_from_incident(
                    [n.dict() if hasattr(n, 'dict') else n.model_dump() for n in inc.nodes],
                    [e.dict() if hasattr(e, 'dict') else e.model_dump() for e in inc.edges]
                )
                return inc
            return None

    def query(self, query_str: str) -> Dict[str, Any]:
        with self.lock:
            q = query_str.lower().strip()
            target_inc_id = self.current_incident_id
            if any(k in q for k in ["opus", "commit", "overkill", "dave", "101", "format"]):
                target_inc_id = "AI-SPEND-101"
            elif any(k in q for k in ["loop", "mcp", "algal", "sarah", "102", "retry", "postgres"]):
                target_inc_id = "AI-SPEND-102"
            elif any(k in q for k in ["sec", "compliance", "prescribed", "alex", "202", "fire", "batch"]):
                target_inc_id = "AI-SPEND-202"

            self.current_incident_id = target_inc_id
            inc = self.incidents[target_inc_id]
            self.graph.load_from_incident(
                [n.dict() if hasattr(n, 'dict') else n.model_dump() for n in inc.nodes],
                [e.dict() if hasattr(e, 'dict') else e.model_dump() for e in inc.edges]
            )

            matched_node_ids = self.graph.find_connected_subgraph(q)
            return {
                "matched_incident_id": target_inc_id,
                "incident": inc.dict() if hasattr(inc, 'dict') else inc.model_dump(),
                "highlighted_node_ids": matched_node_ids,
                "causal_summary": f"Cognee Causal Web navigated to {inc.title}. Pinpointed root foraging pattern and connected nodes."
            }

    def execute_governance(self, incident_id: str, mode: GovernanceMode, force_override: bool = False) -> GovernanceExecutionResponse:
        with self.lock:
            if incident_id not in self.incidents:
                raise ValueError(f"Incident {incident_id} not found")

            inc = self.incidents[incident_id]

            if inc.safety_intercept.intercept_active and mode == GovernanceMode.THROTTLE_AND_EDUCATE and not force_override:
                raise PermissionError(
                    f"SAFETY INTERCEPT ENFORCED: Incident {incident_id} involves an authorized prescribed disturbance ({inc.safety_intercept.authorized_job_name}). Destructive throttling is interlocked to prevent statutory regulatory breach."
                )

            inc.active_governance_mode = mode
            inc.remediated = True

            receipt = ""
            saved_now = 0.0
            realloc = None

            if mode == GovernanceMode.AUTO_DOWNSCALE_REWRITE:
                inc.status = "REMEDIATED_OPTIMIZED"
                saved_now = 1.34
                self.metrics["net_zerodog_savings_usd"] += saved_now
                for node in inc.nodes:
                    if node.status in ["critical", "warning"]:
                        node.status = "remediated"
                receipt = (
                    "**Niche Partitioning Applied (Downscale & Prompt Compression)**:\n"
                    "- Model switched from Claude 3 Opus -> Claude 3.5 Haiku\n"
                    "- 54,200 raw diff tokens pruned at edge to 180 structured tokens\n"
                    "- Injected ephemeral prompt-caching headers\n"
                    "- Instant Savings: $1.34 (99.4% cost reduction)\n"
                    "- Datadog span logging fees avoided: $0.035"
                )

            elif mode == GovernanceMode.THROTTLE_AND_EDUCATE:
                inc.status = "REMEDIATED_OPTIMIZED"
                saved_now = 4.68
                self.metrics["net_zerodog_savings_usd"] += saved_now
                for node in inc.nodes:
                    if node.status in ["critical", "warning"]:
                        node.status = "remediated"
                receipt = (
                    "**Parasitic Algal Loop Severed (Circuit Breaker Intercept)**:\n"
                    "- Agent session throttled after 3 consecutive schema errors\n"
                    "- Corrected database table schema injected into context\n"
                    "- Saved 12 redundant agent roundtrips and 150k tokens\n"
                    "- Instant Savings: $4.68\n"
                    "- Interactive educational diff dispatched to developer"
                )

            elif mode == GovernanceMode.REALLOCATE_QUOTA:
                if inc.safety_intercept.intercept_active:
                    inc.status = "MITIGATED_SAFE_HOLD"
                    receipt = (
                        "**Prescribed Disturbance Validated (Approved Exception)**:\n"
                        f"- Authorized {inc.safety_intercept.authorized_job_name} verified under legal compliance mandate\n"
                        "- Dedicated high-throughput enterprise batch pool allocated\n"
                        "- Destructive rate-limits bypassed while maintaining audit trail"
                    )
                else:
                    inc.status = "REMEDIATED_OPTIMIZED"
                    donor = self.users.get(inc.verdict.user_id, self.users["user_dave"])
                    recipient = self.users["user_elena"]

                    transfer_amount = 25.0
                    donor.daily_quota_usd = max(10.0, donor.daily_quota_usd - transfer_amount)
                    donor.penalties_incurred_usd += transfer_amount
                    donor.reputation_score = max(50, donor.reputation_score - 75)
                    donor.efficiency_rank = "SHAME"

                    recipient.daily_quota_usd += transfer_amount
                    recipient.bonus_tokens_awarded_usd += transfer_amount
                    recipient.reputation_score = min(1000, recipient.reputation_score + 50)
                    recipient.efficiency_rank = "ELITE"

                    saved_now = 25.0
                    realloc = {
                        "donor_name": donor.name,
                        "donor_remaining_quota": donor.daily_quota_usd,
                        "recipient_name": recipient.name,
                        "recipient_new_quota": recipient.daily_quota_usd,
                        "amount_transferred_usd": transfer_amount
                    }
                    receipt = (
                        f"**Robin Hood Nutrient Cycling Executed**:\n"
                        f"- Harvested ${transfer_amount:.2f} token quota from {donor.name} (Efficiency: {donor.efficiency_rank})\n"
                        f"- Transferred ${transfer_amount:.2f} as an 'AI Power User Bonus' to {recipient.name} ({recipient.efficiency_rank})\n"
                        f"- Dynamic carrying capacity restored: {recipient.name}'s daily quota raised to ${recipient.daily_quota_usd:.2f}"
                    )

            return GovernanceExecutionResponse(
                success=True,
                incident_id=incident_id,
                mode=mode,
                new_status=inc.status,
                action_receipt_markdown=receipt,
                dollars_saved_immediate=saved_now,
                reallocation_details=realloc
            )

state_manager = StateManager()
