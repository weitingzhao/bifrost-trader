#!/usr/bin/env python3
"""
Knowledge Base Synchronization Script
Keeps knowledge base files in sync and validates consistency
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set


class KnowledgeSync:
    def __init__(self):
        self.knowledge_base_path = Path("docs/knowledge-base")
        self.source_path = Path(
            "/Users/vision-mac-trader/Desktop/workspace/projects/documents"
        )
        self.issues: List[str] = []

    def sync_knowledge_base(self):
        """Sync knowledge base files"""
        print("🔄 Syncing knowledge base...")

        # Check if source directory exists
        if not self.source_path.exists():
            print(f"⚠️  Source directory {self.source_path} does not exist")
            return

        # List files in source directory
        source_files = list(self.source_path.glob("*.md"))
        knowledge_files = list(self.knowledge_base_path.glob("*.md"))

        print(f"📁 Found {len(source_files)} files in source directory")
        print(f"📁 Found {len(knowledge_files)} files in knowledge base")

        # Check for missing files
        self._check_missing_files(source_files, knowledge_files)

        # Check for consistency
        self._check_consistency()

        # Generate report
        self._generate_report()

    def _check_missing_files(
        self, source_files: List[Path], knowledge_files: List[Path]
    ):
        """Check for missing files"""
        source_names = {f.name for f in source_files}
        knowledge_names = {f.name for f in knowledge_files}

        missing_in_kb = source_names - knowledge_names
        if missing_in_kb:
            self.issues.append(f"Missing files in knowledge base: {missing_in_kb}")

        extra_in_kb = knowledge_names - source_names
        if extra_in_kb:
            self.issues.append(f"Extra files in knowledge base: {extra_in_kb}")

    def _check_consistency(self):
        """Check consistency of knowledge base files"""
        readme_path = self.knowledge_base_path / "README.md"
        if not readme_path.exists():
            self.issues.append("README.md missing in knowledge base")
            return

        # Read README content
        with open(readme_path, "r") as f:
            readme_content = f.read()

        # Check for references to all knowledge files
        knowledge_files = list(self.knowledge_base_path.glob("*.md"))
        for file_path in knowledge_files:
            if file_path.name == "README.md":
                continue

            file_name = file_path.name
            if file_name not in readme_content:
                self.issues.append(f"README.md missing reference to {file_name}")

    def _generate_report(self):
        """Generate sync report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n📊 Knowledge Base Sync Report - {timestamp}")
        print("=" * 50)

        if self.issues:
            print("❌ Issues found:")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("✅ Knowledge base is in sync")

        print("=" * 50)


def main():
    """Main function"""
    sync = KnowledgeSync()
    sync.sync_knowledge_base()


if __name__ == "__main__":
    main()
