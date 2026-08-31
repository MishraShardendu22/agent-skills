# Contributing to `agent-skills`

Thank you for your interest in expanding and improving the **Autonomous AI Agent Skills Catalog**! We welcome contributions of new agent skills, workflow improvements, optimizations, and bug fixes.

---

## 🛠 Adding a New Skill

1. **Scaffold the Skill**:
   Run the CLI scaffold command:
   ```bash
   ./scripts/skills-sync.sh new your-skill-name
   ```
   This creates `.agents/skills/your-skill-name/SKILL.md`.

2. **Follow the Standard Structure**:
   Every skill must have valid YAML frontmatter:
   ```markdown
   ---
   name: your-skill-name
   description: >-
     A concise 1-2 sentence description explaining when and why the AI agent should activate this skill.
   ---

   # Your Skill Title Skill

   ## 1. Overview
   ...

   ## 2. Core Directives & Rules
   ...

   ## 3. Step-by-Step Procedure
   ...
   ```

3. **Validate Your Changes**:
   Ensure all skills pass validation before submitting:
   ```bash
   python3 scripts/validate-skills.py
   ```

---

## 🚀 Proposing Changes

1. Fork the repository on GitHub.
2. Create your feature branch (`git checkout -b username/feature-name`).
3. Commit your changes with conventional commit syntax (`feat(skill): add your-skill-name`).
4. Push to your branch and open a Pull Request.

---

## 📜 Code of Conduct

Please maintain a collaborative, respectful, and productive environment for all open-source contributors.
