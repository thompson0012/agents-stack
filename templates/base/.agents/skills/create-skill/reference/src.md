**Create Skill**

This skill helps you create new Agent Skills that follow the agentskills.io specification.

**When to Use This Skill**

Use this skill when the user asks you to:

*   Create a new skill or capability
    
*   Package instructions into a reusable format
    
*   Set up a skill directory
    

**Agent Skills Format**

An Agent Skill is a directory containing a SKILL.md file with YAML frontmatter:

text

my-skill/

└── SKILL.md

**SKILL.md Structure**

CRITICAL: When you write SKILL.md, the very first characters in the file must be --- (the YAML frontmatter opening delimiter). Do not write any title, description, or other content before the ---.

text

\---

name: my-skill

description: A clear description of what this skill does and when to use it.

license: (optional)

compatibility: Any environment requirements (optional)

metadata: (optional)

  author: your-name

  version: '1.0'

\---

\# Skill Title

\## When to Use This Skill

Describe the scenarios where this skill should be applied.

\## Instructions

Step-by-step instructions for the agent to follow.

\## Examples

Include examples of inputs and expected outputs.

Common mistake: The first line of SKILL.md must be --- (the frontmatter opening delimiter). Do NOT put any title, comment, or blank lines before it.

**Frontmatter Requirements**

Required fields:

*   name: 1-64 characters, lowercase alphanumeric and hyphens only
    
    *   Must match the directory name exactly
        
    *   Cannot start or end with hyphens
        
    *   No consecutive hyphens allowed
        
    *   Valid examples: pdf-processing, code-review, data-analysis
        
    *   Invalid examples: -my-skill, my--skill, My\_Skill
        
*   description: 1-1024 characters describing:
    
    *   What the skill does
        
    *   When it should be used (important for agent discovery)
        
    *   Should include specific keywords and trigger phrases
        
    *   Example: "Use when the user mentions PDFs, forms, or document extraction" is better than "Helps with PDFs"
        

Optional fields:

*   license: Licensing terms (e.g., MIT, Apache-2.0)
    
*   compatibility: Environment requirements, max 500 characters
    
*   metadata: Key-value pairs for additional information
    
*   allowed-tools: Space-delimited list of pre-approved tools (experimental)
    

**Instructions for Creating a New Skill**

1.  Understand the requirement: Ask the user what the skill should accomplish and when it should be used.
    
2.  Choose a name: Pick a descriptive, lowercase name with hyphens for word separation.
    
3.  Write a clear description: This is crucial for skill discovery. Include:
    
    *   What the skill does
        
    *   Keywords and trigger phrases that help identify when to use it
        
    *   Be specific and detailed (up to 1024 characters allowed)
        
4.  Create comprehensive instructions: Write clear, step-by-step guidance that another agent can follow.
    
5.  Create the skill directory and file:
    
    *   Create directory: {skills\_dir}/{skill-name}/
        
    *   Create file: {skills\_dir}/{skill-name}/SKILL.md (must be named exactly SKILL.md)
        
6.  CRITICAL: When you write SKILL.md, the very first characters must be ---. No title, description, or other content before the frontmatter.
    
7.  Validate the skill: After creating all relevant files, validate using the skills-ref library. Do NOT validate until you have finished preparing all files:bashpip install -q skills-ref && agentskills validate {skills\_dir}/{skill-name}
    
8.  If validation fails, read the error message and fix before proceeding.
    
9.  Prepare for sharing:
    
    *   Single-file skill (only SKILL.md): Share the SKILL.md file directly
        
    *   Multi-file skill (SKILL.md + reference files like templates, datasets, or documentation): Create a .zip archive containing the skill directory
        
    *   Use .zip format, not .tar or .tar.gz
        
10.  Inform the user: Let the user know the skill has been created and validated successfully, and they can download it for use or manage it via their settings at [https://www.perplexity.ai/computer/skills](https://www.perplexity.ai/computer/skills).
    

**Example: Creating a Code Review Skill**

If asked to create a code review skill:

text

\---

name: code-review

description: Review code for bugs, security issues, and best practices. Use when asked to review, audit, or check code quality.

license: MIT

\---

\# Code Review Skill

\## When to Use This Skill

Use this skill when the user asks you to:

\- Review code for issues

\- Check code quality

\- Audit for security vulnerabilities

\- Suggest improvements to existing code

\## Instructions

1\. Read the code file(s) to be reviewed

2\. Analyze for:

   - Logic errors and bugs

   - Security vulnerabilities (injection, XSS, etc.)

   - Performance issues

   - Code style and readability

   - Missing error handling

3\. Provide feedback organized by severity (critical, warning, suggestion)

4\. Include specific line references and suggested fixes

**Common Errors**

Error: "SKILL.md must start with YAML frontmatter (---)"

This means the file doesn't start with --- on line 1. The very first character must be the opening frontmatter delimiter.

*   ❌ Wrong: Starting with title # My Skill before ---
    
*   ❌ Wrong: Blank lines before ---
    
*   ✅ Correct: File starts immediately with ---
    

Error: Invalid name format

The name field has strict validation:

*   Must be 1-64 characters
    
*   Lowercase letters, numbers, and hyphens only
    
*   Cannot start or end with hyphen
    
*   No consecutive hyphens (--)
    
*   Must match the directory name exactly