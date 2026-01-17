"""
App Configuration Loader
Dynamically loads app configs for multi-application testing.
"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
import importlib


class AppConfig:
    """Configuration for a single application (segments, target_list, etc.)."""
    
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.module = config.get("module")
        self.page_object = config.get("page_object")
        self.db_helpers = config.get("db_helpers")
        self.test_prefix = config.get("test_prefix")
        self.features = config.get("features", [])
        
    def get_module(self):
        """Import and return the test module."""
        if self.module:
            return importlib.import_module(self.module)
        return None
    
    def get_page_object_class(self):
        """Import and return the page object class."""
        if self.page_object:
            module_path, class_name = self.page_object.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        return None
    
    def get_db_helpers(self):
        """Import and return the DB helpers module."""
        if self.db_helpers:
            return importlib.import_module(self.db_helpers)
        return None
    
    def has_feature(self, feature: str) -> bool:
        """Check if app supports a feature."""
        return feature in self.features


class ValidationConfig:
    """Configuration for validation layers."""
    
    def __init__(self, config: Dict):
        self.ui_enabled = config.get("ui", {}).get("enabled", True)
        self.api_enabled = config.get("api", {}).get("enabled", True)
        self.db_enabled = config.get("database", {}).get("enabled", True)
        self.cross_layer_enabled = config.get("cross_layer", {}).get("enabled", True)
        
        self.api_required_params = config.get("api", {}).get("required_params", {})
        self.cross_layer_fields = config.get("cross_layer", {}).get("compare_fields", [])


class AgentConfig:
    """Configuration for agent behavior."""
    
    def __init__(self, config: Dict):
        self.name = config.get("name", "Test Agent")
        self.version = config.get("version", "1.0.0")
        self.mode = config.get("mode", "autonomous")
        
        memory_cfg = config.get("memory", {})
        self.memory_enabled = memory_cfg.get("enabled", True)
        self.memory_path = memory_cfg.get("persist_path", ".agent/memory.json")
        self.memory_max_history = memory_cfg.get("max_history", 100)
        
        healing_cfg = config.get("self_healing", {})
        self.healing_enabled = healing_cfg.get("enabled", True)
        self.healing_patterns_path = healing_cfg.get("patterns_path", ".agent/patterns.json")
        self.healing_auto_fix = healing_cfg.get("auto_fix", True)
        self.healing_confidence_threshold = healing_cfg.get("confidence_threshold", 0.8)
        
        reflection_cfg = config.get("reflection", {})
        self.reflection_enabled = reflection_cfg.get("enabled", True)
        self.reflection_learn_from_failures = reflection_cfg.get("learn_from_failures", True)
        self.reflection_suggest_improvements = reflection_cfg.get("suggest_improvements", True)


class AppLoader:
    """Loads and manages application configurations."""
    
    def __init__(self, config_path: str = ".agent/config.yaml"):
        self.config_path = Path(config_path)
        self.config_data = self._load_config()
        
        # Parse configurations
        self.agent_config = AgentConfig(self.config_data.get("agent", {}))
        self.validation_config = ValidationConfig(self.config_data.get("validations", {}))
        
        # Load app configurations
        self.apps: Dict[str, AppConfig] = {}
        for app_name, app_cfg in self.config_data.get("apps", {}).items():
            self.apps[app_name] = AppConfig(app_name, app_cfg)
        
        self.current_app: Optional[AppConfig] = None
        
    def _load_config(self) -> Dict:
        """Load YAML configuration file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def get_app(self, app_name: str) -> Optional[AppConfig]:
        """Get configuration for specific app."""
        return self.apps.get(app_name)
    
    def set_current_app(self, app_name: str) -> bool:
        """Set the currently active app context."""
        app = self.get_app(app_name)
        if app:
            self.current_app = app
            return True
        return False
    
    def list_apps(self) -> List[str]:
        """Get list of all configured apps."""
        return list(self.apps.keys())
    
    def get_app_features(self, app_name: str) -> List[str]:
        """Get features supported by an app."""
        app = self.get_app(app_name)
        return app.features if app else []
    
    def reload_config(self):
        """Reload configuration from file."""
        self.__init__(str(self.config_path))


# Global loader instance
_loader_instance = None

def get_app_loader() -> AppLoader:
    """Get global app loader instance (singleton)."""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = AppLoader()
    return _loader_instance
