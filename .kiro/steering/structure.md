# Project Structure

## Directory Organization

```
├── .github/workflows/     # GitHub Actions automation
├── content/              # Hugo content directory
│   ├── en/posts/        # English articles
│   ├── zh/posts/        # Chinese articles
│   ├── _index.md        # Main page content
│   └── _index.zh.md     # Chinese main page
├── scripts/             # Python automation scripts
├── themes/paper/        # Hugo theme (Git submodule)
├── layouts/             # Custom Hugo layouts
├── static/              # Static assets
├── public/              # Generated site output
└── data/                # Hugo data files
```

## Content Conventions

### Article Structure
- **Filename Format**: `YYYY-MM-DD-{slug}.md`
- **Front Matter**: YAML with title, date, draft status, tags, categories
- **Content**: Markdown with embedded Monetag ad placeholders
- **Languages**: Separate directories for `en/` and `zh/` content

### Front Matter Template
```yaml
---
title: "Article Title"
date: 2025-08-13T17:50:45.584481
draft: false
tags: ["topic", "trending", "twitter"]
categories: ["Social Media Trends"]
---
```

## File Naming Conventions

- **Content Files**: Date-prefixed with URL-friendly slugs
- **Scripts**: Descriptive names with underscores (`generate_content.py`)
- **Configuration**: Standard Hugo naming (`hugo.toml`)

## Automation Structure

### Content Generation Flow
1. `scripts/generate_content.py` - Main content generation script
2. Twitter API → Trend fetching
3. OpenAI API → Article generation
4. Hugo content creation → Bilingual output
5. GitHub Actions → Automated publishing

### Key Components
- **TwitterTrendFetcher**: Handles Twitter API integration
- **ContentGenerator**: Manages OpenAI content creation
- **HugoPublisher**: Creates Hugo-compatible markdown files

## Theme Integration

- Uses Paper theme as Git submodule
- Custom layouts in `/layouts/` override theme defaults
- Monetag integration through custom partials
- Bilingual support configured in `hugo.toml`