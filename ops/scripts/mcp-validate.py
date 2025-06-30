#!/usr/bin/env python3
"""
MCP Validator Script
Validates MCP compliance for units
"""

import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class MCPValidationError(Exception):
    """MCP validation error"""
    pass


class MCPValidator:
    """Validates MCP compliance for units"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.units_dir = project_root / "units"
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_unit(self, unit_path: Path) -> bool:
        """Validate a single unit for MCP compliance
        
        Args:
            unit_path: Path to unit directory
            
        Returns:
            True if valid, False otherwise
        """
        unit_name = unit_path.name
        print(f"Validating unit: {unit_name}")
        
        # Check unit.yml exists and is valid
        if not self._validate_unit_manifest(unit_path):
            return False
        
        # Check mcp-validation.yml exists and is valid
        if not self._validate_mcp_config(unit_path):
            return False
        
        return True
    
    def _validate_unit_manifest(self, unit_path: Path) -> bool:
        """Validate unit.yml manifest"""
        manifest_path = unit_path / "unit.yml"
        
        if not manifest_path.exists():
            self.errors.append(f"Missing unit.yml in {unit_path.name}")
            return False
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in {manifest_path}: {e}")
            return False
        
        # Check required fields
        required_fields = ["id", "version", "type", "contracts", "entrypoint"]
        for field in required_fields:
            if field not in manifest:
                self.errors.append(f"Missing required field '{field}' in {manifest_path}")
                return False
        
        # Validate MCP-specific fields
        if manifest.get("type") != "mcp-service":
            self.errors.append(f"Unit type must be 'mcp-service', got '{manifest.get('type')}'")
            return False
        
        # Check MCP configuration
        mcp_config = manifest.get("mcp", {})
        if not isinstance(mcp_config, dict):
            self.errors.append(f"MCP configuration must be an object in {manifest_path}")
            return False
        
        if not mcp_config.get("enabled", False):
            self.warnings.append(f"MCP not enabled in {manifest_path}")
        
        return True
    
    def _validate_mcp_config(self, unit_path: Path) -> bool:
        """Validate mcp-validation.yml configuration"""
        config_path = unit_path / "mcp-validation.yml"
        
        if not config_path.exists():
            self.errors.append(f"Missing mcp-validation.yml in {unit_path.name}")
            return False
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in {config_path}: {e}")
            return False
        
        # Check required fields
        required_fields = ["sdk", "spec_version"]
        for field in required_fields:
            if field not in config:
                self.errors.append(f"Missing required field '{field}' in {config_path}")
                return False
        
        # Validate SDK
        if config.get("sdk") != "python":
            self.warnings.append(f"Non-Python SDK in {config_path}: {config.get('sdk')}")
        
        # Validate spec version
        spec_version = config.get("spec_version")
        if spec_version != "2025-06-18":
            self.warnings.append(f"Unexpected spec version in {config_path}: {spec_version}")
        
        # Check for required checks
        checks = config.get("checks", {})
        required_checks = ["sdk-version", "exposes-api", "lifecycle-support", "contract-alignment"]
        for check in required_checks:
            if check not in checks:
                self.warnings.append(f"Missing recommended check '{check}' in {config_path}")
        
        return True
    
    def validate_all_units(self) -> bool:
        """Validate all units in the project
        
        Returns:
            True if all units are valid, False otherwise
        """
        if not self.units_dir.exists():
            self.errors.append("Units directory does not exist")
            return False
        
        units = [d for d in self.units_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not units:
            self.warnings.append("No units found to validate")
            return True
        
        all_valid = True
        for unit_path in units:
            if not self.validate_unit(unit_path):
                all_valid = False
        
        return all_valid
    
    def print_results(self) -> None:
        """Print validation results"""
        print("\n" + "=" * 50)
        print("MCP Validation Results")
        print("=" * 50)
        
        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✓ All MCP validations passed")
        elif not self.errors:
            print(f"\n✓ MCP validation passed with {len(self.warnings)} warnings")
        else:
            print(f"\n✗ MCP validation failed with {len(self.errors)} errors")


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    validator = MCPValidator(project_root)
    
    if validator.validate_all_units():
        validator.print_results()
        sys.exit(0 if not validator.errors else 1)
    else:
        validator.print_results()
        sys.exit(1)


if __name__ == "__main__":
    main()
