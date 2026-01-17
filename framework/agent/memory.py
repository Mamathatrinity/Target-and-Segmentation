"""
Agent Memory System
Tracks bugs, patterns, test results to prevent loops and enable learning.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class AgentMemory:
    """Persistent memory for agent - prevents repeating same fixes."""
    
    def __init__(self, memory_path: str = ".agent/memory.json"):
        self.memory_path = Path(memory_path)
        self.memory = self._load_memory()
        
    def _load_memory(self) -> Dict:
        """Load memory from JSON file."""
        if self.memory_path.exists():
            with open(self.memory_path, 'r') as f:
                return json.load(f)
        return {
            "fixed_bugs": [],
            "known_patterns": [],
            "test_results": {},
            "last_updated": None,
            "metadata": {
                "version": "1.0.0",
                "created": str(datetime.now()),
                "description": "Agent memory - tracks bugs, patterns, and results"
            }
        }
    
    def save(self):
        """Persist memory to disk."""
        self.memory["last_updated"] = str(datetime.now())
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def record_bug_fix(self, bug: Dict[str, Any]):
        """Record a fixed bug to prevent re-fixing."""
        bug_entry = {
            "bug_id": bug.get("id", f"bug_{len(self.memory['fixed_bugs']) + 1}"),
            "description": bug.get("description"),
            "file": bug.get("file"),
            "line": bug.get("line"),
            "pattern": bug.get("pattern"),
            "fix_action": bug.get("fix_action"),
            "fixed_at": str(datetime.now()),
            "tests_affected": bug.get("tests_affected", [])
        }
        
        # Check if already fixed
        if not self.is_bug_fixed(bug_entry["bug_id"]):
            self.memory["fixed_bugs"].append(bug_entry)
            self.save()
            return True
        return False
    
    def is_bug_fixed(self, bug_id: str) -> bool:
        """Check if bug was already fixed."""
        return any(bug["bug_id"] == bug_id for bug in self.memory["fixed_bugs"])
    
    def get_fixed_bugs(self, file_path: Optional[str] = None) -> List[Dict]:
        """Get all fixed bugs, optionally filtered by file."""
        if file_path:
            return [bug for bug in self.memory["fixed_bugs"] 
                   if bug.get("file") == file_path]
        return self.memory["fixed_bugs"]
    
    def record_pattern(self, pattern: Dict[str, Any]):
        """Record a discovered pattern for future reference."""
        pattern_entry = {
            "pattern_id": pattern.get("id", f"pattern_{len(self.memory['known_patterns']) + 1}"),
            "name": pattern.get("name"),
            "description": pattern.get("description"),
            "detection_regex": pattern.get("detection"),
            "fix_action": pattern.get("fix_action"),
            "occurrences": 1,
            "first_seen": str(datetime.now()),
            "last_seen": str(datetime.now()),
            "auto_fix": pattern.get("auto_fix", False)
        }
        
        # Check if pattern exists
        existing = next((p for p in self.memory["known_patterns"] 
                        if p["pattern_id"] == pattern_entry["pattern_id"]), None)
        
        if existing:
            existing["occurrences"] += 1
            existing["last_seen"] = str(datetime.now())
        else:
            self.memory["known_patterns"].append(pattern_entry)
        
        self.save()
    
    def get_pattern_by_error(self, error_message: str) -> Optional[Dict]:
        """Find matching pattern for an error message."""
        import re
        for pattern in self.memory["known_patterns"]:
            if re.search(pattern["detection_regex"], error_message):
                return pattern
        return None
    
    def record_test_result(self, test_name: str, result: Dict[str, Any]):
        """Record test execution result."""
        if test_name not in self.memory["test_results"]:
            self.memory["test_results"][test_name] = {
                "executions": [],
                "total_runs": 0,
                "total_passes": 0,
                "total_failures": 0
            }
        
        execution = {
            "timestamp": str(datetime.now()),
            "status": result.get("status"),  # passed, failed, skipped
            "duration": result.get("duration"),
            "error": result.get("error"),
            "validations": result.get("validations", {})
        }
        
        self.memory["test_results"][test_name]["executions"].append(execution)
        self.memory["test_results"][test_name]["total_runs"] += 1
        
        if result.get("status") == "passed":
            self.memory["test_results"][test_name]["total_passes"] += 1
        elif result.get("status") == "failed":
            self.memory["test_results"][test_name]["total_failures"] += 1
        
        self.save()
    
    def get_test_history(self, test_name: str) -> Optional[Dict]:
        """Get execution history for a specific test."""
        return self.memory["test_results"].get(test_name)
    
    def get_flaky_tests(self, min_runs: int = 3) -> List[str]:
        """Identify tests that have inconsistent results."""
        flaky = []
        for test_name, data in self.memory["test_results"].items():
            if data["total_runs"] >= min_runs:
                if data["total_passes"] > 0 and data["total_failures"] > 0:
                    flaky.append(test_name)
        return flaky
    
    def get_stats(self) -> Dict:
        """Get memory statistics."""
        return {
            "total_bugs_fixed": len(self.memory["fixed_bugs"]),
            "total_patterns": len(self.memory["known_patterns"]),
            "total_tests_tracked": len(self.memory["test_results"]),
            "flaky_tests": len(self.get_flaky_tests()),
            "last_updated": self.memory.get("last_updated")
        }
    
    def clear(self, keep_patterns: bool = True):
        """Clear memory, optionally keeping learned patterns."""
        if keep_patterns:
            patterns = self.memory["known_patterns"]
            self.memory = self._load_memory()
            self.memory["known_patterns"] = patterns
        else:
            self.memory = self._load_memory()
        self.save()


# Global memory instance
_memory_instance = None

def get_memory() -> AgentMemory:
    """Get global memory instance (singleton)."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = AgentMemory()
    return _memory_instance
