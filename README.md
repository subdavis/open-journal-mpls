# Open City MPLS Blog

This repository contains both the source code for article generation and the blog itself.

## About this project

[Read the about page](/blog/content/about.md)

## Contributions

This project is an ongoing exploration of how LLMs can be used to extract meaningful insights out of complicated bureaucratic processes to serve the public interest. It is open-ended, with lots of room for ideas and experiments.

Contributions or comments of any sort are welcome.

## Development Setup

### Blog

The blog is a [Hugo](https://gohugo.io/) static site.

```bash
git submodule update --recursive # Install hugo themes
cd blog/
hugo server -D
```

Content in `blog/content/posts` is auto-generated. To add any corrections to a summary, edit the file in `archive/summary` and re-run generation.

### Article generation

Article generation is scripted in Python and uses Anthropic's Claude AI.

* You'll need to install Python and [Poetry](https://python-poetry.org/). 
* You'll also need access to the [Anthropic API](https://www.anthropic.com/api)
* LIMS scraping and Transcript scraping do not require authentication.

```bash
cp .env.example .env 
# Add your Anthropic API key
poetry install
poetry run generate
```