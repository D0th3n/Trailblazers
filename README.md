# Trailblazers Website Starter

This is a GitHub Pages-ready starter site for your game's lore hub and development blog.

## What it includes

- a landing page
- a lore page
- a devlog page powered by Markdown posts in `_posts/`
- a gallery page for art and screenshots
- a custom visual style without needing a JavaScript framework

## Best GitHub setup

1. Create a GitHub repo named `trailblazers`.
2. Upload everything in this folder to that repo.
3. In GitHub, open `Settings` -> `Pages`.
4. Under `Build and deployment`, choose `Deploy from a branch`.
5. Select the `main` branch and the `/ (root)` folder.
6. Save, then wait for GitHub Pages to publish the site.

Your public site URL will usually be:

- `https://YOUR-USERNAME.github.io/trailblazers/`

If you want that exact repo-path URL, set this in `_config.yml`:

```yml
baseurl: "/trailblazers"
```

If you use a custom domain later, set:

```yml
baseurl: ""
url: "https://yourdomain.com"
```

## How to add a new devlog post

Create a new file in `_posts/` using this format:

```md
---
title: "Your post title"
---

Write your update here.
```

Name the file like this:

```text
YYYY-MM-DD-your-post-title.md
```

Example:

```text
2026-04-20-first-playable-prototype.md
```

## How to add images

1. Put image files in `assets/images/`
2. Reference them in pages or posts like this:

```md
![Concept art]({{ '/assets/images/concept-art.jpg' | relative_url }})
```

## Suggested next steps

- replace the placeholder lore text with your actual setting
- add a logo or title image
- write your first real devlog post
- add concept art or a moodboard to the gallery
