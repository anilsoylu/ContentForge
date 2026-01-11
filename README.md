# ContentForge

AI-powered SEO content generator with parallel processing. Generate blog articles, comparison tables, and optimized content at scale.

## Features

- **Parallel Generation** - All content sections generated simultaneously using asyncio
- **SEO Optimization** - Keyword targeting, density control, E-E-A-T compliance
- **Comparison Tables** - Dynamic tables with customizable columns and star ratings
- **Dual Output** - Generate both HTML and Markdown formats
- **YAML Configuration** - Simple template-based setup, no coding required
- **Preview Mode** - See structure and cost estimates before generation
- **Multi-language** - Generate content in any language
- **Retry Mechanism** - Automatic retry with exponential backoff

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/contentforge.git
cd contentforge

# Install dependencies
pip install -r requirements.txt

# Copy environment template and add your API key
cp .env.example .env
```

## Configuration

Edit `config.yaml` to customize your content:

```yaml
# Page title
title: "Best Web Hosting Providers 2025"

# SEO settings
seo:
  primary_keyword: "web hosting"
  secondary_keywords:
    - "VPS hosting"
    - "shared hosting"
  keyword_density: 2.0
  tone: "informative"

# Content sections
sections:
  - heading: "What is Shared Hosting?"
    words: 120
  - heading: "VPS vs Dedicated Server"
    words: 120

# Comparison table
table:
  enabled: true
  rows: 5
  columns:
    - name: "item"
      header: "Provider"
    - name: "rating"
      header: "Rating"
      type: "stars"

# AI model
model: "openai/gpt-4o-mini"

# Output format: html or md
output: "md"
```

## Usage

```bash
# Generate content
python main.py

# Preview mode (no API calls)
python main.py -p

# Use custom config file
python main.py -c custom_config.yaml

# Create example config
python main.py --init
```

## Environment Variables

Create a `.env` file with your OpenRouter API key:

```
OPENROUTER_API_KEY=your_api_key_here
```

Get your API key from [OpenRouter](https://openrouter.ai/).

## Project Structure

```
contentforge/
├── main.py              # Entry point
├── config.yaml          # Configuration template
├── requirements.txt     # Dependencies
├── api/
│   └── client.py        # OpenRouter API client
├── core/
│   ├── config.py        # Config loader
│   ├── constants.py     # Defaults and prompts
│   ├── exceptions.py    # Custom exceptions
│   └── models.py        # Data models
├── generators/
│   ├── html.py          # HTML output builder
│   ├── markdown.py      # Markdown output builder
│   └── prompts.py       # AI prompt templates
├── utils/
│   └── text.py          # Text utilities
└── content/             # Generated output
```

## Supported Models

| Model | Speed | Cost/Section | Best For |
|-------|-------|--------------|----------|
| `openai/gpt-4o-mini` | ~45 tps | ~$0.00012 | Bulk content, drafts |
| `openai/gpt-4o` | ~30 tps | ~$0.003 | High-quality articles |

## Cost Estimation

Based on real usage data with GPT-4o-mini:

| Metric | Value |
|--------|-------|
| Avg input tokens | ~340 |
| Avg output tokens | ~120 |
| Cost per API call | ~$0.00012 |

### Calculate Your Cost

A typical article has:
- 1 introduction
- 1 comparison table (optional)
- 3-5 content sections
- 1 conclusion

**Total: 5-8 API calls per article**

| Articles | API Calls | Estimated Cost |
|----------|-----------|----------------|
| 1 | 6 | $0.0007 |
| 10 | 60 | $0.007 |
| 100 | 600 | $0.07 |
| 1,000 | 6,000 | $0.72 |
| 10,000 | 60,000 | $7.20 |

> Use `python main.py -p` (preview mode) to see exact API call count and cost estimate before generation.

## License

MIT License - see [LICENSE](LICENSE) for details.
