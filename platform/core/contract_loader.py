"""
Minimal Contract Loader for Platform Core
Loads and validates YAML contracts from platform/contracts/
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List


class ContractLoadError(Exception):
    """Raised when contract loading fails"""
    pass


class ContractLoader:
    """Minimal contract loader with basic YAML validation"""
    
    def __init__(self, contracts_dir: Optional[Path] = None):
        """Initialize contract loader
        
        Args:
            contracts_dir: Path to contracts directory, defaults to platform/contracts/
        """
        if contracts_dir is None:
            # Default to platform/contracts/ relative to this file
            self.contracts_dir = Path(__file__).parent.parent / "contracts"
        else:
            self.contracts_dir = Path(contracts_dir)
    
    def load_contract(self, contract_name: str) -> Dict[str, Any]:
        """Load a single contract by name
        
        Args:
            contract_name: Name of contract file (without .yml extension)
            
        Returns:
            Parsed contract data
            
        Raises:
            ContractLoadError: If contract cannot be loaded or parsed
        """
        contract_path = self.contracts_dir / f"{contract_name}.yml"
        
        if not contract_path.exists():
            raise ContractLoadError(f"Contract file not found: {contract_path}")
        
        try:
            with open(contract_path, 'r', encoding='utf-8') as f:
                contract_data = yaml.safe_load(f)
            
            if contract_data is None:
                raise ContractLoadError(f"Contract file is empty: {contract_path}")
            
            # Basic validation - must be a dictionary
            if not isinstance(contract_data, dict):
                raise ContractLoadError(f"Contract must be a YAML object: {contract_path}")
            
            return contract_data
            
        except yaml.YAMLError as e:
            raise ContractLoadError(f"Invalid YAML in contract {contract_path}: {e}")
        except IOError as e:
            raise ContractLoadError(f"Cannot read contract file {contract_path}: {e}")
    
    def list_contracts(self) -> List[str]:
        """List all available contract names
        
        Returns:
            List of contract names (without .yml extension)
        """
        if not self.contracts_dir.exists():
            return []
        
        contracts = []
        for contract_file in self.contracts_dir.glob("*.yml"):
            contracts.append(contract_file.stem)
        
        return sorted(contracts)
    
    def validate_contract_syntax(self, contract_path: Path) -> bool:
        """Validate YAML syntax of a contract file
        
        Args:
            contract_path: Path to contract file
            
        Returns:
            True if syntax is valid, False otherwise
        """
        try:
            with open(contract_path, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            return True
        except (yaml.YAMLError, IOError):
            return False
