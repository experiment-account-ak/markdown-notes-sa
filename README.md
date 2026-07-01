# Markdown Notes — Complete Updated Project

A small dependency-free localhost notes app that loads Markdown files and displays them as slides or continuous scrollable topics.

## Run locally

Open a terminal inside this folder:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

Do not open `index.html` directly with `file://`, because the browser will block loading the Markdown files.

## Files

```text
markdown-notes-complete-updated/
├── index.html
├── styles.css
├── markdown.js
├── app.js
├── README.md
└── notes/
    ├── index.json
    ├── 01-introduction.md
    ├── 02-css.md
    ├── 03-javascript.md
    └── graphql-mutation-explanation.md
```

## Add a Markdown file

Create the file inside `notes/`, then add it to `notes/index.json`.

```json
{
  "title": "GraphQL Notes",
  "files": [
    "graphql-mutation-explanation.md"
  ]
}
```

## One scrollable topic

Do not place `---` between sections:

```md
# Main title

## First section

Content

## Second section

More content
```

A line containing only `---` creates another slide/navigation entry.

## Headings

```md
# H1
## H2
### H3
```

The current sizes are configured in `styles.css`:

- H1: 22px
- H2: 15px
- H3: 10px
- Regular text and bullets: 13px

## Code blocks

Use a language after the opening backticks:

````md
```js
const app = express();
```

```graphql
mutation {
  setMessage(message: "Hello GraphQL")
}
```

```json
{
  "data": {
    "setMessage": "Hello GraphQL"
  }
}
```

```bash
npm start
```

```scss
$baseColor: #2471a3;

@mixin title($side) {
  width: $side;
  height: $side;
}
```
````

Programming blocks are dark and syntax-colored.

Use `text` for light rounded example boxes:

````md
```text
Give me the current message.
```
````

## Color one specific phrase

Write:

```md
==★ Schema describes the mutation.==
```

The color is controlled in `styles.css`:

```css
.slide .key-point {
  color: var(--key-point);
  font-weight: 700;
}
```

The default key-point color is `#F2B800`.

## Semantic bullets

```md
- [+] Positive point
- [!] Warning point
- [>] Follow-up point
```

## Keyboard controls

- Left arrow / Page Up: previous note
- Right arrow / Page Down: next note
- Home: first note
- End: final note
- `/`: focus search
- `F`: fullscreen

## Inline backticks inside text boxes

Single backticks inside a `text` block are preserved literally:

````md
```text
You may call `setMessage` and send a `String`.
```
````

Outside a fenced block, single backticks create inline code styling:

```md
`schema.js` contains the schema.
```
