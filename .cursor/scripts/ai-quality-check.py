#!/usr/bin/env python3
"""
AI Code Quality Check Script
Validates AI-generated code against project standards
"""

import sys
import ast
import re
from pathlib import Path
from typing import List, Dict, Any

class AICodeQualityChecker:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def check_file(self, file_path: str) -> bool:
        """Check a single Python file for quality issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Run checks
            self._check_imports(tree)
            self._check_functions(tree)
            self._check_classes(tree)
            self._check_docstrings(tree)
            self._check_type_hints(tree)
            
            return len(self.errors) == 0
            
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error checking {file_path}: {e}")
            return False
    
    def _check_imports(self, tree: ast.AST):
        """Check import statements"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith('shared.'):
                        continue  # Allow shared imports
                    if not self._is_standard_import(alias.name):
                        self.warnings.append(f"Non-standard import: {alias.name}")
    
    def _check_functions(self, tree: ast.AST):
        """Check function definitions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for type hints
                if not node.returns and node.name != '__init__':
                    self.warnings.append(f"Function {node.name} missing return type hint")
                
                # Check for docstrings
                if not ast.get_docstring(node):
                    self.warnings.append(f"Function {node.name} missing docstring")
    
    def _check_classes(self, tree: ast.AST):
        """Check class definitions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check for docstrings
                if not ast.get_docstring(node):
                    self.warnings.append(f"Class {node.name} missing docstring")
    
    def _check_docstrings(self, tree: ast.AST):
        """Check docstring quality"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if docstring and len(docstring) < 10:
                    self.warnings.append(f"{type(node).__name__} {node.name} has short docstring")
    
    def _check_type_hints(self, tree: ast.AST):
        """Check type hint usage"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.annotation is None and arg.arg != 'self':
                        self.warnings.append(f"Function {node.name} argument {arg.arg} missing type hint")
    
    def _is_standard_import(self, module_name: str) -> bool:
        """Check if import is from standard library or common packages"""
        standard_modules = {
            'typing', 'collections', 'datetime', 'json', 'os', 'sys',
            'pathlib', 'logging', 'asyncio', 'contextlib', 'functools',
            'fastapi', 'pydantic', 'sqlalchemy', 'pytest'
        }
        return module_name.split('.')[0] in standard_modules
    
    def print_results(self):
        """Print check results"""
        if self.errors:
            print("❌ Errors found:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("⚠️  Warnings found:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ No quality issues found")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python ai-quality-check.py <file1> [file2] ...")
        sys.exit(1)
    
    checker = AICodeQualityChecker()
    all_passed = True
    
    for file_path in sys.argv[1:]:
        print(f"Checking {file_path}...")
        if not checker.check_file(file_path):
            all_passed = False
    
    checker.print_results()
    
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
