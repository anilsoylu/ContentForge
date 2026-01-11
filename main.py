#!/usr/bin/env python3
"""
Interactive Content Generation Script v4
- Modular architecture
- Parallel API calls (asyncio)
- YAML template support
- Preview mode
- Retry mechanism
- Progress bar
"""

import argparse
import asyncio
import os
from datetime import datetime
from pathlib import Path

from tqdm import tqdm

from api.client import OpenRouterClient
from core import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_OUTPUT_DIR,
    ConfigNotFoundError,
    ContentConfig,
    GeneratedContent,
    load_api_key,
    load_config,
    save_default_config,
)
from generators.html import build_full_html, build_table_html
from generators.markdown import build_full_md, build_table_md
from generators.prompts import (
    build_conclusion_prompt,
    build_intro_prompt,
    build_section_prompt,
    build_table_prompt,
)
from utils.text import clean_markdown_fences, parse_table_data


# ============================================================
# PREVIEW MODE
# ============================================================

def show_preview(config: ContentConfig) -> None:
    """Show structure without making API calls."""
    print()
    print("=" * 50)
    print("   PREVIEW MODE (no API calls will be made)")
    print("=" * 50)
    print()

    print(f"📄 STRUCTURE:")
    print(f"   <h1>{config.title}</h1>")
    print()
    print(f"   <div class=\"intro\">")
    print(f"      ~{config.intro_words} words intro paragraph")
    print(f"   </div>")
    print()

    if config.table.enabled and config.table.rows > 0:
        col_headers = [col.header for col in config.table.columns]
        print(f"   <div class=\"comparison-table\">")
        print(f"      <h2>Comparison</h2>")
        print(f"      <table> {config.table.rows} rows, {len(col_headers)} columns: {', '.join(col_headers)} </table>")
        print(f"   </div>")
        print()

    for section in config.sections:
        print(f"   <section>")
        print(f"      <h2>{section.heading}</h2>")
        print(f"      ~{section.words} words content")
        print(f"   </section>")
        print()

    print(f"   <div class=\"conclusion\">")
    print(f"      <h2>Conclusion</h2>")
    print(f"      ~{config.conclusion_words} words summary")
    print(f"   </div>")
    print()

    print(f"📊 ESTIMATES:")
    print(f"   Total words: ~{config.total_words}")
    print(f"   API calls: {config.api_call_count}")
    print(f"   Model: {config.model}")
    print(f"   Output format: {config.output}")
    print(f"   Language: {config.language}")
    print(f"   Estimated cost: ~${config.api_call_count * 0.0002:.4f}")
    print()


# ============================================================
# PARALLEL GENERATION
# ============================================================

async def generate_all_content(
    api_key: str,
    config: ContentConfig
) -> GeneratedContent:
    """Generate all content in parallel."""
    headings = config.headings
    table_rows = config.table.rows if config.table.enabled else 0

    print(f"\n   🚀 Starting {config.api_call_count} API calls in parallel...\n")

    async with OpenRouterClient(api_key, config.model, config.site.url) as client:
        with tqdm(total=config.api_call_count, desc="   Content generation", unit="section") as pbar:
            tasks: list[tuple[str, str]] = []

            # 1. Introduction paragraph
            intro_prompt = build_intro_prompt(
                config.title, headings, config.intro_words, config.seo, config.language
            )
            tasks.append(("intro", intro_prompt))

            # 2. Comparison table (optional)
            if table_rows > 0:
                table_prompt = build_table_prompt(
                    config.title, config.table, config.placeholders, config.language
                )
                tasks.append(("table", table_prompt))

            # 3. Sections
            for i, section in enumerate(config.sections):
                section_prompt = build_section_prompt(
                    config.title,
                    section.heading,
                    section.words,
                    i,
                    len(config.sections),
                    headings[:i],
                    config.seo,
                    config.placeholders,
                    config.language
                )
                tasks.append((f"section_{i}", section_prompt))

            # 4. Conclusion paragraph
            conclusion_prompt = build_conclusion_prompt(
                config.title, headings, config.conclusion_words, config.seo, config.language
            )
            tasks.append(("conclusion", conclusion_prompt))

            # Run all tasks in parallel
            results = await client.generate_batch(tasks, pbar=pbar)

    # Organize results
    content = GeneratedContent()
    content.intro = results.get("intro", "")
    content.conclusion = results.get("conclusion", "")

    # Table (build both formats)
    if "table" in results:
        raw_data = clean_markdown_fences(results["table"])
        table_rows_data = parse_table_data(raw_data, config.table.columns)
        content.table_html = build_table_html(table_rows_data, config.table.columns)
        content.table_md = build_table_md(table_rows_data, config.table.columns)

    # Sections (ordered)
    content.sections = [
        results.get(f"section_{i}", "")
        for i in range(len(config.sections))
    ]

    return content


# ============================================================
# FILE SAVING
# ============================================================

def save_output(content: str, output_dir: str, output_format: str = "html") -> str:
    """Save content to file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    extension = "md" if output_format == "md" else "html"
    filename = f"{timestamp}.{extension}"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


# ============================================================
# MAIN FUNCTION
# ============================================================

async def run_async(args: argparse.Namespace) -> None:
    """Main async function."""
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Init mode
    if args.init:
        save_default_config(args.config or DEFAULT_CONFIG_PATH)
        return

    # Determine config path
    config_path = args.config or DEFAULT_CONFIG_PATH

    # Load config
    try:
        config = load_config(config_path)
    except ConfigNotFoundError as e:
        print(f"❌ {e}")
        print(f"   To create example config: python {Path(__file__).name} --init")
        return

    # Preview mode
    if args.preview:
        show_preview(config)
        return

    # Load API key
    api_key = load_api_key()

    print("-" * 50)
    print("🚀 Generating content (parallel mode)...")
    print("-" * 50)

    # Parallel generation
    content = await generate_all_content(api_key, config)

    # Build output based on format
    if config.output == "md":
        full_content = build_full_md(
            config.title, content, config.headings, config.seo.all_keywords
        )
    else:
        full_content = build_full_html(
            config.title, content, config.headings, config.seo.all_keywords
        )

    # Save
    output_dir = os.path.join(script_dir, DEFAULT_OUTPUT_DIR)
    filepath = save_output(full_content, output_dir, config.output)

    # Calculate word count
    word_count = len(full_content.split())

    print()
    print("=" * 50)
    print("✅ COMPLETED!")
    print(f"   File: {filepath}")
    print(f"   Target: ~{config.total_words} words")
    print(f"   Generated: {word_count} words ({len(full_content)} characters)")
    print("=" * 50)


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(description="SEO Content Generator v4")
    parser.add_argument("-c", "--config", help="YAML config file path")
    parser.add_argument("-p", "--preview", action="store_true", help="Preview mode")
    parser.add_argument("--init", action="store_true", help="Create example config")
    return parser.parse_args()


def main():
    """Entry point."""
    args = parse_args()

    try:
        asyncio.run(run_async(args))
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
