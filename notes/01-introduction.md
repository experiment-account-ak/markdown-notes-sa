# Welcome to My Notes

This project turns ordinary **Markdown files** into a slide-style notes website.

- Use the sidebar to choose a slide
- Use the left and right arrow keys to navigate
- Press `/` to focus search
- Press `F` to enter fullscreen mode

> Replace these examples with your own study notes, documentation, or presentation content.

---

# How Slides Are Created

Each Markdown file can contain one or more slides.

A line containing exactly three dashes separates slides:

```md
# First Slide

Some content.

---

# Second Slide

More content.
```

The first heading in each slide becomes its sidebar title.

---

# Project Structure

```text
markdown-notes-slides/
├── index.html
├── styles.css
├── markdown.js
├── app.js
├── README.md
└── notes/
    ├── index.json
    ├── 01-introduction.md
    ├── 02-css.md
    └── 03-javascript.md
```

Add new Markdown files inside `notes/`, then register them in `notes/index.json`.
