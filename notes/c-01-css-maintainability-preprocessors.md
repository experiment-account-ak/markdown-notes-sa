## Lecture Summary Request

# C-01 - CSS Scalability and Maintainability: Preprocessors

## The mental model: **Write better-organized source code, then compile it into browser-ready CSS**

Think of Sass like a **translator sitting between the developer and the browser**:

```text
Developer writes SCSS/Sass
        ↓
Sass preprocessor translates it
        ↓
Normal CSS is generated
        ↓
Browser reads the generated CSS
```

The browser does **not** understand Sass directly. It only understands the final CSS produced by the preprocessor. This translation process is the central idea of the lecture. `C-01-css-maintainability-preprocessors.pdf`
## 1. Why does CSS become difficult to maintain?

The lecture begins with a common problem: CSS files can grow very large as an application grows.

This may cause:

- high complexity;
- poor readability;
- poor maintainability;
- longer loading times when external stylesheets are too large;
- uncontrolled “proliferation” of styles;
- increasingly specific or **overspecific selectors**;
- repeated CSS declarations;
- unused or **dead code**.

▣ **Dead code**  
CSS rules that remain in the stylesheet but are no longer used by the application.

▣ **Overspecific selector**  
A selector that includes more IDs, classes or nested elements than necessary.

💡 Example:

```css
html body main div.content section.article p.message {
  color: red;
}
```

This might work, but it is difficult to override and strongly tied to one exact HTML structure.

❗ The lecture identifies the underlying reason as CSS’s limited mechanisms for **modularization and reuse**.

→ Result: As the application grows, developers may copy declarations, create increasingly complex selectors and lose track of which rules are still needed.
## 2. What approaches does the lecture introduce?

The lecture names two possible approaches:

1. **Additional tools**
   - CSS preprocessors
   - Sass is used as the example.

2. **Methodical or structured approaches**
   - naming conventions
   - BEM is mentioned as an example.

❗ This particular lecture focuses on **preprocessors and Sass**. BEM is only introduced as another possible solution and is not explained further here.
## 3. What is a CSS preprocessor?

▣ **CSS preprocessor**  
A tool that extends CSS with additional language constructs and translates the resulting stylesheet into ordinary CSS.

The source language is normally a **superset of CSS** or a CSS-like language with additional features.

However, that source code cannot normally be processed directly by the browser.

```text
Extended stylesheet language
        ↓
     Preprocessor
        ↓
      Pure CSS
        ↓
      Browser
```

The diagram on page 8 presents exactly this pipeline:

- the source stylesheet provides more features than CSS;
- the source stylesheet does not run in the browser;
- the preprocessor generates CSS;
- the generated CSS runs in the browser.

❗ A preprocessor is therefore mainly a **development-time tool**, not something that usually operates inside the browser.
## 4. Examples of CSS preprocessors

The lecture names:

- Sass
- Less
- Stylus

The remaining lecture uses **Sass** as its example.
## 5. What is Sass?

▣ **Sass**  
Sass stands for **Syntactically Awesome Style Sheets**. It is a stylesheet language that is translated into CSS using a Sass preprocessor.

Sass offers two syntax variants.

## 5.1 SCSS

▣ **SCSS - Sassy CSS**

- file extension: `.scss`;
- uses braces and semicolons like normal CSS;
- is a true superset of CSS;
- valid CSS is therefore also valid SCSS;
- easy to introduce into an existing CSS project.

## 5.2 Indented syntax

- file extension: `.sass`;
- uses indentation instead of braces;
- normally omits semicolons;
- is more compact;
- is described in the lecture as being derived from YAML-like indentation.

Sass also provides good IDE support, such as syntax highlighting, and uses a Dart-based preprocessor to translate source files into CSS.
## 6. Which CSS features does Sass add?

The lecture focuses on four Sass features:

1. variables;
2. mixins;
3. imports;
4. nested rules.

It later mentions that Sass supports many more constructs, including inheritance, functions, loops and arithmetic operations, but these are outside the detailed scope of this lecture. `C-01-css-maintainability-preprocessors.pdf`
## 7. Sass variables

## What problem do Sass variables solve?

▣ **Sass variable**  
A named value stored in a Sass stylesheet so that the same value can be reused in multiple places.

The goal is to **centralize frequently used values**.

Variable names begin with `$`.

```scss
$mediumFontSize: 42px;
$primaryColor: #ffe4e1;
```

Instead of repeating `42px` or `#ffe4e1` throughout the file, the stylesheet refers to these variables.
## Complete lecture example

### SCSS source

```scss
$mediumFontSize: 42px;
$primaryColor: #ffe4e1;

#header {
  font-size: $mediumFontSize;
  background-color: $primaryColor;
}

.button {
  background-color: $primaryColor;
}

p {
  font-size: $mediumFontSize;
}
```

### Generated CSS

```css
#header {
  font-size: 42px;
  background-color: #ffe4e1;
}

.button {
  background-color: #ffe4e1;
}

p {
  font-size: 42px;
}
```

## What happens here?

```scss
$mediumFontSize: 42px;
```

This creates a variable named `$mediumFontSize`.

```scss
font-size: $mediumFontSize;
```

The preprocessor substitutes the variable with its stored value.

```css
font-size: 42px;
```

The browser receives only this generated CSS. It does not receive the original Sass variable.

→ Result: The repeated design values are controlled from one central place.

💡 For example, changing:

```scss
$mediumFontSize: 48px;
```

would update both `#header` and `p` when Sass generates the CSS again.
## 8. Sass variables versus CSS custom properties

Modern CSS also supports reusable values through **custom properties**.

▣ **CSS custom property**  
A native CSS property whose name begins with `--` and whose value is accessed using `var(...)`.

## Complete lecture example

```css
/*
The :root pseudo-class selects the root element of the document.
In HTML, the root element is <html>.

Properties declared here are visible to all elements contained
inside <html>, so they are globally available.
*/
:root {
  --mediumFontSize: 42px;
  --primaryColor: #ffe4e1;
}

#header {
  font-size: var(--mediumFontSize);
  background-color: var(--primaryColor);
}

.button {
  background-color: var(--primaryColor);
}
```

## Syntax comparison

### Sass variable

```scss
$primaryColor: #ffe4e1;

.button {
  background-color: $primaryColor;
}
```

### CSS custom property

```css
:root {
  --primaryColor: #ffe4e1;
}

.button {
  background-color: var(--primaryColor);
}
```
## Important difference: compile time versus runtime

### Sass variable

```text
SCSS source
   ↓ Sass compilation
Value is substituted
   ↓
Ordinary CSS
```

The Sass variable disappears during compilation.

### CSS custom property

```text
CSS file containing --primaryColor
   ↓
Browser keeps the property
   ↓
Value is evaluated at runtime
```

❗ CSS custom properties remain available inside the browser at runtime.

Therefore, unlike Sass variables, CSS custom properties:

- participate in the CSS cascade;
- can vary by element or scope;
- can be manipulated using JavaScript.

💡 Simple example:

```css
:root {
  --primaryColor: blue;
}

.warning-area {
  --primaryColor: red;
}

button {
  background-color: var(--primaryColor);
}
```

A normal button uses blue, while a button inside `.warning-area` can use red because custom properties participate in the cascade.

→ Result: Sass variables are replaced during preprocessing, whereas CSS custom properties remain dynamic inside the browser.
## 9. Mixins

## What problem do mixins solve?

Variables reuse **individual values**.

Mixins reuse **entire blocks of declarations**.

▣ **Mixin**  
A reusable collection of CSS declarations that can optionally receive parameters.

### General declaration syntax

```scss
@mixin mixinName([parameter]*) {
  /* CSS declarations */
}
```

### General inclusion syntax

```scss
@include mixinName([argument]*);
```

Parameters begin with `$`, like Sass variables.
## Complete lecture example

### SCSS source

```scss
@mixin box($side) {
  width: $side;
  height: $side;
  border-radius: 5px;
  -webkit-box-reflect: below 5px;
}

.content-box {
  @include box(200px);
  border: 1px solid;
  overflow: scroll;
}

.header-box {
  @include box(150px);
  background-color: gray;
}
```

### Generated CSS

```css
.content-box {
  width: 200px;
  height: 200px;
  border-radius: 5px;
  -webkit-box-reflect: below 5px;
  border: 1px solid;
  overflow: scroll;
}

.header-box {
  width: 150px;
  height: 150px;
  border-radius: 5px;
  -webkit-box-reflect: below 5px;
  background-color: gray;
}
```
## Line-by-line explanation

```scss
@mixin box($side) {
```

Defines a reusable mixin named `box`.

`$side` is a parameter. The caller supplies its value.

```scss
width: $side;
height: $side;
```

The same parameter is used for width and height, creating a square.

```scss
@include box(200px);
```

Inserts the declarations from `box`, replacing `$side` with `200px`.

Therefore:

```scss
@include box(200px);
```

generates:

```css
width: 200px;
height: 200px;
border-radius: 5px;
-webkit-box-reflect: below 5px;
```

The declarations written directly inside `.content-box` are then added after the mixin declarations:

```scss
border: 1px solid;
overflow: scroll;
```

Similarly:

```scss
@include box(150px);
```

generates a box with a width and height of `150px`.

→ Result: Shared box styling is declared once but reused with different sizes.
## 10. Imports

## What problem do Sass imports solve?

A single stylesheet can become too large. Imports allow the stylesheet to be divided into smaller files.

▣ **Sass import**  
A mechanism for bringing content from another Sass stylesheet into the current Sass compilation process.

### Syntax

```scss
@import 'FileNameWithoutFileExtension';
```

The file extension can be omitted.

The Sass preprocessor combines the files and generates one CSS file.

❗ According to the lecture, unused variables, mixins or other Sass elements from an imported file do not create CSS rules merely because they were imported.

For example, a variable definition alone does not produce browser CSS. It only influences generated CSS when used.
## Complete lecture example

### `base.scss`

```scss
$baseColor: #2471a3;
$fontStack: Arial, sans-serif;

@mixin tile($side) {
  width: $side;
  height: $side;
}
```

This file contains:

- a reusable colour;
- a reusable font stack;
- a reusable `tile` mixin.

### `boxes.scss`

```scss
/* import 'base.scss' */
@import 'base';

@mixin box($side) {
  /* use mixin from 'base' */
  @include tile($side);
  border-radius: 5px;
}

.header-box {
  @include box(150px);

  /* use variable from 'base' */
  background-color: $baseColor;
}
```

### Generated CSS

```css
.header-box {
  width: 150px;
  height: 150px;
  border-radius: 5px;
  background-color: #2471a3;
}
```
## How does the flow work?

```text
base.scss
 ├── $baseColor
 ├── $fontStack
 └── tile($side)
          ↓ imported into
boxes.scss
 ├── box($side) uses tile($side)
 └── .header-box uses box() and $baseColor
          ↓ Sass compiler
generated CSS
```

Step by step:

1. `boxes.scss` imports `base.scss`.

```scss
@import 'base';
```

2. The `box` mixin can now use `tile`.

```scss
@include tile($side);
```

3. `.header-box` includes `box(150px)`.

```scss
@include box(150px);
```

4. `box(150px)` internally includes `tile(150px)`.

5. The final CSS therefore receives:

```css
width: 150px;
height: 150px;
border-radius: 5px;
```

6. `$baseColor` becomes:

```css
background-color: #2471a3;
```

❗ `$fontStack` does not appear in the generated CSS because the example never uses it in a CSS declaration.

→ Result: Multiple source files are used during development, but Sass produces one final CSS stylesheet. `C-01-css-maintainability-preprocessors.pdf`
## 11. Sass imports versus native CSS imports

Native CSS also has an `@import` rule.

## Lecture example

```css
/* Imports all rules from 'basis.css' into
   the current CSS file */
@import 'basis.css';
```

However, the lecture identifies disadvantages of native CSS imports:

- the browser performs a separate HTTP request for every imported file;
- the requests are performed sequentially rather than in parallel;
- this can increase loading times and harm performance.

## Mental distinction

### Sass import

```text
Several Sass source files
       ↓ build time
One generated CSS file
       ↓
One CSS resource for the browser
```

### Native CSS import

```text
Browser downloads main CSS
       ↓
Browser discovers @import
       ↓
Browser requests another CSS file
```

❗ Sass imports are resolved before the stylesheet reaches the browser. Native CSS imports are resolved by the browser.
## 12. Nested rules

## What problem does nesting solve?

▣ **Nesting**  
Writing related selectors inside one another so that the stylesheet structure resembles the HTML structure.

The goal is to improve readability.

Instead of writing:

```css
.navbar ul {
  list-style-type: none;
}

.navbar a {
  color: #45b39d;
}

.navbar a:hover {
  font-size: larger;
}
```

Sass lets the developer group these rules under `.navbar`.
## Complete lecture example

### SCSS source

```scss
.navbar {
  ul {
    list-style-type: none;
  }

  a {
    color: #45b39d;

    &:hover {
      font-size: larger;
    }
  }
}
```

### Generated CSS

```css
.navbar ul {
  list-style-type: none;
}

.navbar a {
  color: #45b39d;
}

.navbar a:hover {
  font-size: larger;
}
```
## How is normal nesting translated?

```scss
.navbar {
  ul {
    list-style-type: none;
  }
}
```

The nested `ul` becomes a descendant selector:

```css
.navbar ul {
  list-style-type: none;
}
```

This means:

> Select every `ul` contained somewhere inside an element whose class is `navbar`.
## What does `&` mean?

▣ **The Sass parent selector `&`**  
A symbol that refers to the complete selector of the current parent rule.

Inside:

```scss
a {
  &:hover {
    font-size: larger;
  }
}
```

`&` means the current selector, which after considering the outer nesting is:

```css
.navbar a
```

Therefore:

```scss
&:hover
```

becomes:

```css
.navbar a:hover
```

❗ Without `&`, the meaning would be different because Sass could interpret the nested selector as a descendant rather than joining `:hover` directly to `a`.

→ Result: `&` lets a pseudo-class, modifier or similar selector be attached directly to the parent selector.
## 13. What is the danger of excessive nesting?

Although nesting can improve readability, the lecture warns against nesting too deeply.

Consider:

```scss
.page {
  .content {
    .article {
      .message {
        span {
          color: red;
        }
      }
    }
  }
}
```

This generates:

```css
.page .content .article .message span {
  color: red;
}
```

This selector is:

- highly specific;
- strongly dependent on the HTML structure;
- harder to override;
- harder to reuse if the element moves elsewhere.

❗ Nesting should represent meaningful relationships, not reproduce every level of the HTML document.

→ Result: Nesting can solve a readability problem, but excessive nesting can recreate the original problem of overspecific selectors.
## 14. Sass nesting versus native CSS nesting

The lecture states that native CSS now also provides nesting functionality in relevant browsers.

However, Sass nesting and CSS nesting are **similar but subtly incompatible**.

## Sass nesting from the lecture

```scss
.navbar {
  ul {
    list-style-type: none;
  }

  a {
    color: #45b39d;

    &:hover {
      font-size: larger;
    }
  }
}
```

## Native CSS nesting from the lecture

```css
.navbar {
  & ul {
    list-style-type: none;
  }

  & a {
    color: #45b39d;

    &:hover {
      font-size: larger;
    }
  }
}
```

The lecture explains that `&` is required in this CSS example to create descendant selectors.

Nested CSS selectors must begin with an allowed symbol such as:

```text
&  @  :  .  >  ~  +  #  [  *
```

## Main comparison

```text
Sass:
.navbar {
  a { ... }
}

Native CSS shown in lecture:
.navbar {
  & a { ... }
}
```

❗ Similar syntax does not mean that Sass nesting and native CSS nesting can always be copied between files unchanged.
## 15. SCSS versus indented syntax

The lecture presents the same idea using both Sass syntaxes.

## SCSS

```scss
$color: #45b39d;

.navbar {
  border: 1px solid $color;

  a {
    color: $color;
  }
}
```

Characteristics:

- uses `{ }`;
- uses `;`;
- resembles CSS;
- valid CSS is valid SCSS;
- easy to combine with an existing CSS project.
## Indented syntax

```sass
$color: #45b39d
.navbar
  border: 1px solid $color
  a
    color: $color
```

Characteristics:

- indentation defines hierarchy;
- no curly braces;
- no semicolons;
- slightly more compact.

## Equivalent generated CSS

Both versions represent approximately:

```css
.navbar {
  border: 1px solid #45b39d;
}

.navbar a {
  color: #45b39d;
}
```

❗ The difference is mainly the way the Sass source is written. Both are translated into CSS.
## 16. How do the four Sass features fit together?

Use this map:

```text
Problem: repeated value
        ↓
Variable
Example: one reusable colour

Problem: repeated declaration block
        ↓
Mixin
Example: reusable width + height + border radius

Problem: one stylesheet becomes too large
        ↓
Import
Example: base.scss + boxes.scss

Problem: related selectors are scattered
        ↓
Nesting
Example: navbar rules grouped together
```

A useful hierarchy is:

```text
Variable
    reuses one value

Mixin
    reuses several declarations

Import
    reuses and organizes stylesheet modules

Nesting
    organizes selector relationships
```
## 17. One combined example using the lecture concepts

The following is a small conceptual example combining the ideas already introduced in the lecture.

### `_base.scss`

```scss
$primaryColor: #2471a3;

@mixin tile($side) {
  width: $side;
  height: $side;
}
```

### `navigation.scss`

```scss
@import 'base';

.navbar {
  background-color: $primaryColor;

  ul {
    list-style-type: none;
  }

  a {
    color: white;

    &:hover {
      font-size: larger;
    }
  }
}

.header-box {
  @include tile(150px);
}
```

### Generated CSS

```css
.navbar {
  background-color: #2471a3;
}

.navbar ul {
  list-style-type: none;
}

.navbar a {
  color: white;
}

.navbar a:hover {
  font-size: larger;
}

.header-box {
  width: 150px;
  height: 150px;
}
```

This maps the concepts as follows:

```text
$primaryColor       → variable
tile($side)         → mixin
@import 'base'      → import
.navbar { ul {...}} → nesting
```
## 18. What are the benefits and costs of CSS preprocessors?

## Benefits

### 1. They compensate for weaknesses in CSS

Preprocessors extend CSS with additional options.

### 2. They support modularization

Large stylesheets can be divided into separate source files.

### 3. They support reuse

Variables and mixins reduce duplicated declarations.

### 4. They support DRY

▣ **DRY - Don’t Repeat Yourself**  
A principle that recommends avoiding multiple copies of the same knowledge or implementation.

💡 Instead of writing:

```css
.button {
  background-color: #2471a3;
}

.header {
  background-color: #2471a3;
}

.footer {
  background-color: #2471a3;
}
```

Sass can centralize the value:

```scss
$baseColor: #2471a3;
```
## Costs

### 1. An additional build step is required

```text
SCSS/Sass
   ↓ compilation
CSS
```

The source cannot simply be passed to the browser as ordinary CSS.

### 2. Additional tooling is needed

For example:

- compiler integration;
- syntax highlighting;
- source-level debugging;
- IDE support.

### 3. Native CSS may already provide the feature

The lecture specifically notes:

- CSS custom properties as an alternative to Sass variables;
- native CSS nesting as an alternative to Sass nesting.

❗ Before introducing a preprocessing feature, developers should check whether native CSS already provides an appropriate solution.
## 19. Likely exam questions

## What is a CSS preprocessor?

▣ A CSS preprocessor extends CSS with additional language constructs. Because browsers do not normally process the preprocessor language directly, the source stylesheet is translated into pure CSS before it is delivered to the browser.
## Explain the preprocessing pipeline

```text
Sass or SCSS source
        ↓
Sass preprocessor
        ↓
Generated CSS
        ↓
Browser
```

The developer works with the extended source language, but the browser receives ordinary CSS.
## What is the difference between a Sass variable and a CSS custom property?

A Sass variable begins with `$` and is substituted during the build process. It is no longer present in the generated CSS.

A CSS custom property begins with `--`, is accessed using `var(...)`, remains available at runtime, participates in the cascade and can be manipulated using JavaScript.
## What is the difference between a variable and a mixin?

A variable reuses a single value:

```scss
$color: red;
```

A mixin reuses an entire declaration block and may accept parameters:

```scss
@mixin box($side) {
  width: $side;
  height: $side;
}
```
## What does `@include` do?

`@include` inserts the declarations of a previously defined mixin.

```scss
@include box(200px);
```

This includes the `box` declarations using `200px` as the argument.
## Why are Sass imports useful?

They allow a stylesheet to be split into multiple modules. Sass combines the imported source files during preprocessing and creates a single generated CSS file.
## What is the difference between Sass import and native CSS import?

Sass resolves imports during the build process and can generate one combined CSS file.

A native CSS `@import` is handled by the browser and may cause additional sequential HTTP requests, potentially increasing loading time.
## What does the Sass `&` symbol mean?

`&` represents the current parent selector.

```scss
a {
  &:hover {
    font-size: larger;
  }
}
```

When nested under `.navbar`, it becomes:

```css
.navbar a:hover {
  font-size: larger;
}
```
## Why can excessive nesting be harmful?

It can generate overspecific selectors, increase coupling to the HTML structure and make styles difficult to override or reuse.
## Compare SCSS and the Sass indented syntax

SCSS uses braces and semicolons and is a true superset of CSS. Its files use `.scss`.

The indented syntax uses indentation instead of braces and semicolons. Its files use `.sass`.
## 20. Final lecture map

```text
CSS scalability problem
│
├── Stylesheets grow
├── Repetition increases
├── Selectors become overspecific
├── Readability decreases
└── Dead code appears
        │
        ▼
CSS preprocessor
        │
        └── Sass
             │
             ├── Variables
             │    └── reuse values
             │
             ├── Mixins
             │    └── reuse declaration blocks
             │
             ├── Imports
             │    └── divide source into modules
             │
             └── Nesting
                  └── group related selectors
        │
        ▼
Sass compiler generates ordinary CSS
        │
        ▼
Browser processes the CSS
```

## Core takeaway

❗ Sass does not replace CSS in the browser.

It provides a more expressive and reusable **source language for developers**, which must then be translated into normal CSS.

→ Result: Preprocessors can improve modularity, reuse and maintainability, but they also introduce a compilation step and additional tooling. Developers should also check whether native CSS features, such as custom properties or CSS nesting, already solve the required problem. `C-01-css-maintainability-preprocessors.pdf`

## Which Section Was Marked NP?

You are right: **NP means “not exam relevant.”**

In this lecture, only **slide/page 28: “SCSS vs. Indented Syntax”** is marked **NP**. `C-01-css-maintainability-preprocessors.pdf`

Therefore, this section from my summary is not exam relevant:

## Section 15 - SCSS versus indented syntax

Specifically, you do **not** need to study in detail:

- the syntax comparison between `.scss` and `.sass`;
- braces and semicolons in SCSS;
- indentation-based syntax in Sass;
- the statement that SCSS is a true superset of CSS;
- the statement that the indented syntax is derived from YAML;
- the comparison code:

```scss
$color: #45b39d;

.navbar {
  border: 1px solid $color;

  a {
    color: $color;
  }
}
```

versus:

```sass
$color: #45b39d
.navbar
  border: 1px solid $color
  a
    color: $color
```

I also briefly mentioned the two syntax variants earlier in **Section 5: “What is Sass?”**. That information came from slide 10, which is **not marked NP**, so the basic fact that Sass has the two variants **SCSS and Indented Syntax** remains part of the relevant lecture content. However, the **detailed comparison on slide 28** is NP.

### Correct exam-focused distinction

- **Relevant:** Sass has two syntax variants: SCSS (`.scss`) and Indented Syntax (`.sass`).
- **Not exam relevant:** Their detailed syntax differences and comparative advantages.

Everything else in the summary-variables, CSS custom properties, mixins, imports, nesting, and the conclusion-is not marked NP in this lecture.
