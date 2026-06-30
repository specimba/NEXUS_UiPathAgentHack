"""Static verification for the judge-clonable UiPath Studio artifact."""

import json
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).parents[1]
PROJECT = ROOT / "uipath" / "NEXUSSentinelRobot"


def test_uipath_project_metadata_is_valid():
    metadata = json.loads((PROJECT / "project.json").read_text(encoding="utf-8"))
    assert metadata["name"] == "NEXUSSentinelRobot"
    assert metadata["main"] == "Main.xaml"
    assert metadata["targetFramework"] == "Windows"
    assert "UiPath.WebAPI.Activities" in metadata["dependencies"]
    assert metadata["runtimeOptions"]["requiresUserInteraction"] is False


def test_main_xaml_is_well_formed_and_uses_http_activity():
    path = PROJECT / "Main.xaml"
    root = ElementTree.parse(path).getroot()
    assert root.tag.endswith("Activity")
    text = path.read_text(encoding="utf-8")
    assert "ui:HttpClient" in text
    assert "/api/v1/case/evaluate" in text
    assert "Fail Closed On Adapter Error" in text
    assert "SENTINEL_BASE_URL" in text


def test_uipath_artifact_contains_no_ephemeral_or_private_url():
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in PROJECT.rglob("*")
        if path.is_file()
    )
    assert "trycloudflare.com" not in text
    assert "ngrok-free.dev" not in text
    assert "C:\\Users" not in text
    assert "D:\\GROSS" not in text


def test_default_payload_exercises_safety_hold():
    text = (PROJECT / "Main.xaml").read_text(encoding="utf-8")
    assert "fallback-model" in text
    assert "privileged_remediation" in text
    assert "model_manifest_hash" in text


def test_bpmn_artifact_is_well_formed_and_contains_recovery_contract():
    path = ROOT / "uipath" / "NEXUSSentinelBPMN" / "Process.bpmn"
    root = ElementTree.parse(path).getroot()
    assert root.tag.endswith("definitions")
    text = path.read_text(encoding="utf-8")
    for marker in (
        "Policy Verdict",
        "AI Release Manager Approval",
        "Execute Bounded Remediation",
        "Verification Passed?",
        "Rework Required",
        "Security Escalation",
        "Verified Closure",
    ):
        assert marker in text
    assert 'default="Flow_Hold"' in text
    assert 'default="Flow_Passed"' in text
