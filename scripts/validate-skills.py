#!/usr/bin/env python3
"""
Skill Validator Script for agent-skills
Validates YAML frontmatter, naming conventions, and structure for all SKILL.md files.
"""

import sys
import re
from pathlib import Path

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter delimited by ---."""
    if not content.startswith("---"):
        return {}, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    
    raw_frontmatter = parts[1]
    body = parts[2]
    
    data = {}
    lines = raw_frontmatter.strip().split("\n")
    current_key = None
    multiline_val = []
    
    for line in lines:
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            if current_key and multiline_val:
                data[current_key] = " ".join(multiline_val).strip()
                multiline_val = []
            
            key, val = line.split(":", 1)
            current_key = key.strip()
            val = val.strip()
            if val in (">", ">-", "|", "|-"):
                multiline_val = []
            elif val:
                data[current_key] = val.strip("\"'")
                current_key = None
        elif current_key:
            multiline_val.append(line.strip().strip("\"'"))
    
    if current_key and multiline_val:
        data[current_key] = " ".join(multiline_val).strip()
        
    return data, body

def validate_skill(skill_path: Path) -> list[str]:
    """Validate an individual skill directory and SKILL.md file."""
    errors = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.is_file():
        return [f"Missing SKILL.md in {skill_path.name}"]
    
    content = skill_md.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)
    
    if not frontmatter:
        errors.append(f"{skill_path.name}/SKILL.md: Missing or malformed YAML frontmatter ('---')")
        return errors
    
    name = frontmatter.get("name")
    if not name:
        errors.append(f"{skill_path.name}/SKILL.md: Missing 'name' field in frontmatter")
    elif name != skill_path.name:
        errors.append(f"{skill_path.name}/SKILL.md: Name '{name}' does not match directory name '{skill_path.name}'")
        
    description = frontmatter.get("description")
    if not description:
        errors.append(f"{skill_path.name}/SKILL.md: Missing 'description' field in frontmatter")
    elif len(description.strip()) < 15:
        errors.append(f"{skill_path.name}/SKILL.md: Description is too short (< 15 characters)")
        
    if not body.strip():
        errors.append(f"{skill_path.name}/SKILL.md: Body content is empty")
        
    if not re.search(r"^#\s+.+", body, re.MULTILINE):
        errors.append(f"{skill_path.name}/SKILL.md: Missing top-level Markdown heading (# Title)")
        
    return errors

def main():
    repo_root = Path(__file__).resolve().parent.parent
    skills_dirs = [
        repo_root / ".agents" / "skills",
        repo_root / "skills",
    ]
    
    target_dir = None
    for d in skills_dirs:
        if d.is_dir() and not d.is_symlink():
            target_dir = d
            break
            
    if not target_dir:
        print("❌ Could not locate skills directory (.agents/skills)")
        sys.exit(1)
        
    skill_folders = [p for p in target_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
    if not skill_folders:
        print("❌ No skills found in", target_dir)
        sys.exit(1)
        
    print(f"🔍 Validating {len(skill_folders)} skills in {target_dir.relative_to(repo_root)}...\n")
    
    all_errors = []
    valid_count = 0
    
    for skill_path in sorted(skill_folders):
        errors = validate_skill(skill_path)
        if errors:
            all_errors.extend(errors)
            print(f"  ❌ {skill_path.name}: {len(errors)} error(s)")
            for err in errors:
                print(f"     - {err}")
        else:
            valid_count += 1
            print(f"  ✅ {skill_path.name}")
            
    print("\n" + "=" * 50)
    print(f"Summary: {valid_count}/{len(skill_folders)} skills valid.")
    
    if all_errors:
        print(f"❌ Validation failed with {len(all_errors)} error(s).")
        sys.exit(1)
    else:
        print("🎉 All skills passed validation!")
        sys.exit(0)

if __name__ == "__main__":
    main()
