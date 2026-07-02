# Markdown Notes — Complete Updated Project

A small dependency-free localhost notes app that loads Markdown files and displays them as slides or continuous scrollable topics.

## Start the app and terminal manager

Open a terminal inside this folder and run:

```bash
python manage_notes.py
```

On Windows, this may be:

```powershell
py manage_notes.py
```

This is now the recommended way to run the project. It automatically:

1. Starts the local web server.
2. Opens the app in your default browser.
3. Keeps an interactive management menu in the terminal.

The server remains active while the menu is open. Choose **Exit and stop
server** when you are finished. If port `8000` is already occupied, the script
tries the next available port automatically.

Convenience launchers are also included:

- Windows: double-click `START-NOTES.bat`.
- macOS/Linux: run `./start-notes.sh`.

## Terminal menu

The menu includes:

- Add a Markdown note.
- Rename its sidebar name.
- Optionally rename the stored `.md` filename.
- Move a note to a different or new section.
- Reorder notes inside a section.
- Delete a note and optionally its Markdown file.
- Rename, reorder, or delete sections.
- List the complete structure.
- Check for missing, duplicate, or unregistered Markdown files.
- Reopen the browser.

After changing the structure, refresh the browser to see the update.

## Add a note

Choose **Add note** in the menu. The program asks you to drag a Markdown file
into the terminal or paste its path. It then asks for:

1. The name displayed in the sidebar.
2. An existing section or a new section.
3. The note's position inside that section.

The source file is copied into `notes/`, its filename is normalized for the
web, and `notes/index.json` is updated safely. A backup is kept at
`notes/index.json.bak`.

The display name is independent from the stored filename. For example:

```json
{
  "file": "e04-graphql-introduction.md",
  "title": "GraphQL for Beginners"
}
```

Old filename-only entries continue to work:

```json
"e04-graphql-introduction.md"
```

## Individual commands

The same features can be launched directly:

```bash
python manage_notes.py serve
python manage_notes.py add ~/Downloads/my-note.md
python manage_notes.py list
python manage_notes.py rename
python manage_notes.py move
python manage_notes.py reorder
python manage_notes.py delete
python manage_notes.py rename-section
python manage_notes.py reorder-sections
python manage_notes.py delete-section
python manage_notes.py check
```

Useful server options:

```bash
python manage_notes.py --port 9000
python manage_notes.py --no-browser
```

`serve` starts only the web server. Press `Ctrl+C` to stop it. Running the
script without a command starts both the server and interactive menu.

## Project files

```text
markdown-notes/
├── manage_notes.py
├── START-NOTES.bat
├── start-notes.sh
├── index.html
├── styles.css
├── markdown.js
├── app.js
├── README.md
└── notes/
    ├── index.json
    └── *.md
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
