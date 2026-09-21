# Preflight Roadmap

## Vision

Preflight is a Python CLI for checking code quality and maintainability.

The goal is to go beyond running existing tools and start analyzing the codebase itself, showing where the biggest problems are and what should be fixed first.

## Near-term goals

### Codebase analysis

Add checks for:

- Large files and functions
- High complexity
- Dead code
- Duplicate code
- Weak typing
- Test and coverage signals

### Reporting

Make the output easier to act on:

- Group findings by category
- Highlight the worst files and functions
- Rank issues by severity
- Show the most important problems first

### Health scoring

Explore a simple maintainability score based on measurable signals.

The score should be transparent and easy to understand.

### Change-aware analysis

Show whether a branch improves or worsens the codebase:

- Compare against another branch
- Show newly introduced issues
- Track changes in maintainability metrics

## Out of scope for now

- Web dashboard
- AI-dependent analysis
- IDE integration
- Multi-language support
