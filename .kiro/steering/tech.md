# Technology Stack

## Core Technologies

- **Static Site Generator**: Hugo (Go-based)
- **Theme**: Paper theme (Git submodule)
- **Content Generation**: Python 3.x with OpenAI API
- **Data Source**: TwitterAPI.io (Third-party Twitter API)
- **Automation**: GitHub Actions
- **Deployment**: GitHub Pages / Netlify / Vercel

## Dependencies

### Python Dependencies (requirements.txt)
- `requests>=2.31.0` - HTTP requests for API calls
- `openai>=1.12.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `tweepy>=4.14.0` - Twitter API client

### Hugo Configuration
- Multilingual setup (English/Chinese)
- Markdown with unsafe HTML rendering enabled
- Custom parameters for Monetag integration

## Common Commands

### Development
```bash
# Install Hugo (macOS)
brew install hugo

# Install Python dependencies
pip install -r requirements.txt

# Generate content locally
export TWITTER_API_KEY="your_api_key"
export OPENAI_API_KEY="your_key"
python scripts/generate_content.py

# Start Hugo development server
hugo server -D
```

### Build & Deploy
```bash
# Build static site
hugo

# Build with specific environment
hugo --environment production
```

### Testing
```bash
# Test content generation script
python scripts/test_generate.py

# Validate Hugo configuration
hugo config
```

## API Requirements

- **TwitterAPI.io**: API key required for tweet search and trend analysis
- **OpenAI API**: API key required for content generation
- **Monetag**: Publisher ID for ad integration

## Environment Variables

- `TWITTER_API_KEY`: TwitterAPI.io API authentication
- `OPENAI_API_KEY`: OpenAI API authentication