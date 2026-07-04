/*
  Small dependency-free Markdown renderer.

  Supported:
  - #, ##, ### headings
  - heading IDs for internal links
  - paragraphs
  - unordered and ordered lists
  - fenced code blocks
  - lightweight syntax highlighting
  - blockquotes
  - horizontal rules
  - simple tables
  - **bold**, *italic*, `inline code`
  - [links](https://example.com)
  - [internal links](#section-name)
  - ![images](images/example.png)
  - ==specifically highlighted text==
  - semantic bullets: [+], [!], [>]
*/

(function attachMarkdownRenderer(globalObject) {
  "use strict";

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function createHeadingId(text) {
    return String(text)
      .replace(/[*_`~]/g, "")
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-");
  }

  function renderInline(source) {
    let text = escapeHtml(source);

    const codeTokens = [];

    text = text.replace(/`([^`\n]+)`/g, (_, code) => {
      const token = `@@INLINE_CODE_${codeTokens.length}@@`;
      codeTokens.push(`<code>${code}</code>`);
      return token;
    });

    text = text
      // Images: ![alt text](relative-or-absolute-path)
      .replace(
        /!\[([^\]]*)\]\(([^)\s]+)\)/g,
        '<img src="$2" alt="$1" class="md-image">'
      )

      // Links: [label](relative-or-absolute-path)
      .replace(
        /\[([^\]]+)\]\(([^)\s]+)\)/g,
        (match, label, href) => {
          const isExternal = /^https?:\/\//i.test(href);

          if (isExternal) {
            return `<a href="${href}" target="_blank" rel="noreferrer">${label}</a>`;
          }

          return `<a href="${href}">${label}</a>`;
        }
      )

      .replace(/==(.+?)==/g, '<span class="key-point">$1</span>')
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/__([^_]+)__/g, "<strong>$1</strong>")
      .replace(/(^|[^\w])\*([^*\n]+)\*/g, "$1<em>$2</em>")
      .replace(/(^|[^\w])_([^_\n]+)_/g, "$1<em>$2</em>");

    codeTokens.forEach((html, index) => {
      text = text.replace(`@@INLINE_CODE_${index}@@`, html);
    });

    return text;
  }

  const LANGUAGE_ALIASES = {
    js: "javascript",
    javascript: "javascript",
    jsx: "javascript",
    gql: "graphql",
    graphql: "graphql",
    json: "json",
    bash: "bash",
    shell: "bash",
    sh: "bash",
    css: "css",
    scss: "scss",
    html: "html",
    xml: "xml",
    text: "text",
    txt: "text",
    plain: "text",
    plaintext: "text"
  };

  const KEYWORDS = {
    javascript: new Set([
      "as", "async", "await", "break", "case", "catch", "class", "const",
      "continue", "default", "delete", "do", "else", "export", "extends",
      "finally", "for", "from", "function", "get", "if", "import", "in",
      "instanceof", "let", "new", "of", "return", "set", "static", "switch",
      "throw", "try", "typeof", "var", "void", "while", "with", "yield"
    ]),
    graphql: new Set([
      "directive", "enum", "extend", "fragment", "implements", "input",
      "interface", "mutation", "on", "query", "repeatable", "scalar",
      "schema", "subscription", "type", "union"
    ]),
    scss: new Set([
      "and", "as", "at-root", "content", "debug", "each", "else", "error",
      "extend", "for", "forward", "from", "function", "if", "import",
      "include", "mixin", "not", "or", "return", "through", "to", "use",
      "warn", "while", "with"
    ]),
    css: new Set([
      "important", "inherit", "initial", "revert", "unset"
    ]),
    bash: new Set([
      "case", "do", "done", "elif", "else", "esac", "export", "fi", "for",
      "function", "if", "in", "local", "readonly", "select", "then", "until",
      "while"
    ]),
    html: new Set([]),
    xml: new Set([]),
    json: new Set([])
  };

  function token(className, value) {
    return `<span class="token ${className}">${escapeHtml(value)}</span>`;
  }

  function normalizeLanguage(language) {
    const value = String(language || "")
      .trim()
      .toLowerCase()
      .replace(/[^\w-]/g, "");

    return LANGUAGE_ALIASES[value] || value || "text";
  }

  function isIdentifierStart(character) {
    return /[A-Za-z_]/.test(character);
  }

  function isIdentifierPart(character) {
    return /[A-Za-z0-9_-]/.test(character);
  }

  function highlightHtmlLike(source) {
    return escapeHtml(source)
      .replace(
        /(&lt;\/?)([A-Za-z][\w:-]*)([^&]*?)(\/?&gt;)/g,
        (_, open, tagName, attributes, close) => {
          const highlightedAttributes = attributes.replace(
            /([A-Za-z_:][\w:.-]*)(=)(&quot;.*?&quot;|&#039;.*?&#039;)/g,
            '<span class="token property">$1</span><span class="token operator">$2</span><span class="token string">$3</span>'
          );

          return (
            `<span class="token punctuation">${open}</span>` +
            `<span class="token keyword">${tagName}</span>` +
            highlightedAttributes +
            `<span class="token punctuation">${close}</span>`
          );
        }
      );
  }

  function highlightCode(source, language) {
    const lang = normalizeLanguage(language);

    if (lang === "text") {
      return escapeHtml(source);
    }

    if (lang === "html" || lang === "xml") {
      return highlightHtmlLike(source);
    }

    const keywords = KEYWORDS[lang] || new Set();
    let output = "";
    let index = 0;

    while (index < source.length) {
      const character = source[index];
      const next = source[index + 1];

      if (/\s/.test(character)) {
        output += character;
        index += 1;
        continue;
      }

      if (character === "/" && next === "*") {
        let end = source.indexOf("*/", index + 2);
        end = end === -1 ? source.length : end + 2;
        output += token("comment", source.slice(index, end));
        index = end;
        continue;
      }

      if (
        (character === "/" && next === "/") ||
        (character === "#" && ["bash", "graphql"].includes(lang))
      ) {
        const end = source.indexOf("\n", index);
        const stop = end === -1 ? source.length : end;
        output += token("comment", source.slice(index, stop));
        index = stop;
        continue;
      }

      if (character === '"' || character === "'" || character === "`") {
        const quote = character;
        let end = index + 1;
        let escaped = false;

        while (end < source.length) {
          const current = source[end];

          if (!escaped && current === quote) {
            end += 1;
            break;
          }

          escaped = !escaped && current === "\\";
          if (current !== "\\") {
            escaped = false;
          }

          end += 1;
        }

        output += token("string", source.slice(index, end));
        index = end;
        continue;
      }

      if (lang === "scss" && character === "$" && isIdentifierStart(next || "")) {
        let end = index + 2;

        while (end < source.length && isIdentifierPart(source[end])) {
          end += 1;
        }

        output += token("variable", source.slice(index, end));
        index = end;
        continue;
      }

      if (
        (lang === "scss" || lang === "css") &&
        character === "@" &&
        isIdentifierStart(next || "")
      ) {
        let end = index + 2;

        while (end < source.length && isIdentifierPart(source[end])) {
          end += 1;
        }

        output += token("atrule", source.slice(index, end));
        index = end;
        continue;
      }

      const numberMatch = source
        .slice(index)
        .match(/^-?(?:0x[\da-f]+|\d*\.?\d+)(?:e[+-]?\d+)?(?:px|rem|em|vh|vw|%|s|ms)?/i);

      if (numberMatch) {
        output += token("number", numberMatch[0]);
        index += numberMatch[0].length;
        continue;
      }

      if (isIdentifierStart(character)) {
        let end = index + 1;

        while (end < source.length && isIdentifierPart(source[end])) {
          end += 1;
        }

        const word = source.slice(index, end);
        const lower = word.toLowerCase();
        const rest = source.slice(end);
        const nextNonSpace = rest.match(/^\s*(.)/)?.[1] || "";

        let className = "";

        if (lower === "true" || lower === "false") {
          className = "boolean";
        } else if (lower === "null" || lower === "undefined") {
          className = "null";
        } else if (keywords.has(lower)) {
          className = "keyword";
        } else if (
          lang === "graphql" &&
          ["String", "Int", "Float", "Boolean", "ID"].includes(word)
        ) {
          className = "builtin";
        } else if (
          (lang === "css" || lang === "scss") &&
          nextNonSpace === ":"
        ) {
          className = "property";
        } else if (nextNonSpace === "(") {
          className = "function";
        }

        output += className ? token(className, word) : escapeHtml(word);
        index = end;
        continue;
      }

      if (/[=+\-*/!<>?:&|]/.test(character)) {
        let end = index + 1;

        while (end < source.length && /[=+\-*/!<>?:&|]/.test(source[end])) {
          end += 1;
        }

        output += token("operator", source.slice(index, end));
        index = end;
        continue;
      }

      if (/[{}[\]();,.]/.test(character)) {
        output += token("punctuation", character);
        index += 1;
        continue;
      }

      output += escapeHtml(character);
      index += 1;
    }

    return output;
  }

  function parseTable(lines, startIndex) {
    const header = lines[startIndex];
    const separator = lines[startIndex + 1];

    if (
      !header?.includes("|") ||
      !separator ||
      !/^\s*\|?[\s:|-]+\|[\s:|-]*\|?\s*$/.test(separator)
    ) {
      return null;
    }

    const splitRow = (row) =>
      row
        .trim()
        .replace(/^\|/, "")
        .replace(/\|$/, "")
        .split("|")
        .map((cell) => cell.trim());

    const headers = splitRow(header);
    const rows = [];

    let index = startIndex + 2;

    while (index < lines.length && lines[index].includes("|")) {
      rows.push(splitRow(lines[index]));
      index += 1;
    }

    const headHtml = headers
      .map((cell) => `<th>${renderInline(cell)}</th>`)
      .join("");

    const bodyHtml = rows
      .map((row) => {
        const cells = headers
          .map(
            (_, cellIndex) =>
              `<td>${renderInline(row[cellIndex] ?? "")}</td>`
          )
          .join("");

        return `<tr>${cells}</tr>`;
      })
      .join("");

    return {
      html:
        `<table>` +
        `<thead><tr>${headHtml}</tr></thead>` +
        `<tbody>${bodyHtml}</tbody>` +
        `</table>`,
      nextIndex: index
    };
  }

  function renderMarkdown(markdown) {
    const normalized = String(markdown).replace(/\r\n?/g, "\n");
    const lines = normalized.split("\n");
    const html = [];

    let index = 0;
    let paragraph = [];
    let listType = null;
    let listItems = [];
    let quoteLines = [];

    function flushParagraph() {
      if (!paragraph.length) {
        return;
      }

      html.push(`<p>${renderInline(paragraph.join(" "))}</p>`);
      paragraph = [];
    }

    function flushList() {
      if (!listType || !listItems.length) {
        listType = null;
        listItems = [];
        return;
      }

      function renderListItem(item) {
        const marker = item.match(/^\[([+!>])\]\s*(.*)$/);

        if (!marker) {
          return `<li>${renderInline(item)}</li>`;
        }

        const className = {
          "+": "marker-positive",
          "!": "marker-warning",
          ">": "marker-arrow"
        }[marker[1]];

        return `<li class="${className}">${renderInline(marker[2])}</li>`;
      }

      html.push(
        `<${listType}>${listItems
          .map(renderListItem)
          .join("")}</${listType}>`
      );

      listType = null;
      listItems = [];
    }

    function flushQuote() {
      if (!quoteLines.length) {
        return;
      }

      html.push(
        `<blockquote>${renderInline(quoteLines.join(" "))}</blockquote>`
      );

      quoteLines = [];
    }

    function flushBlocks() {
      flushParagraph();
      flushList();
      flushQuote();
    }

    while (index < lines.length) {
      const line = lines[index];

      if (/^```/.test(line.trim())) {
        flushBlocks();

        const rawLanguage = line.trim().slice(3).trim();
        const language = normalizeLanguage(rawLanguage);
        const codeLines = [];
        index += 1;

        while (
          index < lines.length &&
          !/^```/.test(lines[index].trim())
        ) {
          codeLines.push(lines[index]);
          index += 1;
        }

        const code = codeLines.join("\n");

        html.push(
          `<pre data-language="${escapeHtml(language)}" ` +
          `class="language-${escapeHtml(language)}">` +
          `<code class="language-${escapeHtml(language)}">` +
          `${highlightCode(code, language)}` +
          `</code></pre>`
        );

        index += 1;
        continue;
      }

      const table = parseTable(lines, index);

      if (table) {
        flushBlocks();
        html.push(table.html);
        index = table.nextIndex;
        continue;
      }

      const headingMatch = line.match(/^(#{1,3})\s+(.+)$/);

      if (headingMatch) {
        flushBlocks();

        const level = headingMatch[1].length;
        const headingText = headingMatch[2].trim();
        const headingId = createHeadingId(headingText);

        html.push(
          `<h${level} id="${escapeHtml(headingId)}">${renderInline(headingText)}</h${level}>`
        );

        index += 1;
        continue;
      }

      if (/^\s*(---+|\*\*\*+)\s*$/.test(line)) {
        flushBlocks();
        html.push("<hr>");
        index += 1;
        continue;
      }

      const unorderedMatch = line.match(/^\s*[-+*]\s+(.+)$/);

      if (unorderedMatch) {
        flushParagraph();
        flushQuote();

        if (listType && listType !== "ul") {
          flushList();
        }

        listType = "ul";
        listItems.push(unorderedMatch[1]);
        index += 1;
        continue;
      }

      const orderedMatch = line.match(/^\s*\d+\.\s+(.+)$/);

      if (orderedMatch) {
        flushParagraph();
        flushQuote();

        if (listType && listType !== "ol") {
          flushList();
        }

        listType = "ol";
        listItems.push(orderedMatch[1]);
        index += 1;
        continue;
      }

      const quoteMatch = line.match(/^\s*>\s?(.*)$/);

      if (quoteMatch) {
        flushParagraph();
        flushList();
        quoteLines.push(quoteMatch[1]);
        index += 1;
        continue;
      }

      if (!line.trim()) {
        flushBlocks();
        index += 1;
        continue;
      }

      flushList();
      flushQuote();
      paragraph.push(line.trim());
      index += 1;
    }

    flushBlocks();

    return html.join("\n");
  }

  globalObject.Markdown = {
    escapeHtml,
    render: renderMarkdown
  };
})(window);