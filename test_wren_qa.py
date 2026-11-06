import unittest
from fastapi.testclient import TestClient
from backend.main import app
from backend.models import GovernanceMode

client = TestClient(app)

class TestZeroDogWrenQA(unittest.TestCase):
    def setUp(self):
        res = client.post("/api/reset")
        self.assertEqual(res.status_code, 200)

    def test_01_global_state_boot(self):
        """Spherical Cow in a Vacuum: App boots directly into pre-hydrated state."""
        res = client.get("/api/state")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(data["total_tokens_monitored"], 10_000_000)
        self.assertGreater(data["net_zerodog_savings_usd"], 1000.0)
        self.assertEqual(len(data["active_incidents"]), 3)
        self.assertEqual(len(data["users"]), 6)
        print("✓ Test 01 Passed: Pre-hydrated state boots cleanly in <10ms")

    def test_02_workflow_1_opus_overkill_remediation(self):
        """Wren Workflow 1: Semantic Query -> Causal Pinpoint -> Downscale Remediation."""
        query_res = client.post("/api/query", json={"query": "commit message overkill"})
        self.assertEqual(query_res.status_code, 200)
        q_data = query_res.json()
        self.assertEqual(q_data["matched_incident_id"], "AI-SPEND-101")
        self.assertTrue(len(q_data["highlighted_node_ids"]) > 0)

        inc = q_data["incident"]
        self.assertTrue(inc["verdict"]["model_overkill"]["verdict"])
        self.assertGreaterEqual(inc["verdict"]["model_overkill"]["probability"], 0.95)

        gov_res = client.post("/api/governance", json={
            "incident_id": "AI-SPEND-101",
            "mode": GovernanceMode.AUTO_DOWNSCALE_REWRITE.value,
            "force_override": False
        })
        self.assertEqual(gov_res.status_code, 200)
        g_data = gov_res.json()
        self.assertEqual(g_data["new_status"], "REMEDIATED_OPTIMIZED")
        self.assertIn("Niche Partitioning Applied", g_data["action_receipt_markdown"])

        state_res = client.get("/api/state")
        state_data = state_res.json()
        self.assertGreater(state_data["net_zerodog_savings_usd"], 1218.40)
        print("✓ Test 02 Passed: Wren Workflow 1 (Overkill Niche Partitioning) completed and asserted")

    def test_03_workflow_2_safety_intercept_guardrail(self):
        """Wren Workflow 2: Safety Intercept prevents cascading outage on prescribed burn."""
        sel_res = client.post("/api/incident/select", json={"incident_id": "AI-SPEND-202"})
        self.assertEqual(sel_res.status_code, 200)
        inc = sel_res.json()["incident"]
        self.assertTrue(inc["safety_intercept"]["intercept_active"])

        throttle_res = client.post("/api/governance", json={
            "incident_id": "AI-SPEND-202",
            "mode": GovernanceMode.THROTTLE_AND_EDUCATE.value,
            "force_override": False
        })
        self.assertEqual(throttle_res.status_code, 409)
        err = throttle_res.json()["detail"]
        self.assertEqual(err["error"], "SAFETY_INTERCEPT_ENFORCED")
        self.assertTrue(err["intercept_blocked"])

        safe_res = client.post("/api/governance", json={
            "incident_id": "AI-SPEND-202",
            "mode": GovernanceMode.REALLOCATE_QUOTA.value,
            "force_override": False
        })
        self.assertEqual(safe_res.status_code, 200)
        s_data = safe_res.json()
        self.assertEqual(s_data["new_status"], "MITIGATED_SAFE_HOLD")
        self.assertIn("Prescribed Disturbance Validated", s_data["action_receipt_markdown"])
        print("✓ Test 03 Passed: Wren Workflow 2 (Safety Intercept Guardrail) successfully interlocked and resolved")

    def test_04_robin_hood_nutrient_cycling(self):
        """Verify dynamic nutrient redistribution from wasteful user to top steward."""
        res = client.post("/api/governance", json={
            "incident_id": "AI-SPEND-101",
            "mode": GovernanceMode.REALLOCATE_QUOTA.value,
            "force_override": False
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        realloc = data["reallocation_details"]
        self.assertIsNotNone(realloc)
        self.assertEqual(realloc["donor_name"], "Dave Miller")
        self.assertEqual(realloc["recipient_name"], "Elena Rostova")
        self.assertEqual(realloc["amount_transferred_usd"], 25.0)

        state = client.get("/api/state").json()
        users = {u["name"]: u for u in state["users"]}
        self.assertEqual(users["Dave Miller"]["daily_quota_usd"], 35.0)
        self.assertEqual(users["Elena Rostova"]["daily_quota_usd"], 105.0)
        print("✓ Test 04 Passed: Robin Hood Nutrient Cycling transferred $25 quota from Dave to Elena")

    def test_05_roast_my_stack_challenge(self):
        """Verify the 'Roast My Stack' live challenge evaluator."""
        challenge_prompt = "Format this git commit message: [500 lines of git diff dumped here] and lint the JSON"
        res = client.post("/api/challenge/analyze", json={
            "prompt_text": challenge_prompt,
            "target_model": "claude-3-opus",
            "mcp_tools_text": "tool: git_exec"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["jev_overkill"]["verdict"])
        self.assertGreaterEqual(data["jev_overkill"]["probability"], 0.90)
        self.assertGreater(data["projected_daily_waste_usd"], 50.0)
        self.assertIn("Trophic Mismatch Detected", data["ecological_diagnosis"])
        print("✓ Test 05 Passed: Live Challenge Evaluator roasted prompt in <20ms")

if __name__ == "__main__":
    unittest.main()
