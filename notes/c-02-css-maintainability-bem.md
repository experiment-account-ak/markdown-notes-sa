# C-02 - CSS Scalability and Maintainability: BEM

## Mental model: **Give every CSS class a meaningful address**

As a website grows, class names such as these become difficult to understand:

```css
.red {
  color: red;
}

.big {
  font-size: 24px;
}

.active {
  font-style: italic;
}
```

The problem is that the names do not clearly tell us:

- which part of the website they belong to;
- whether they represent a complete component;
- whether they represent a smaller part;
- whether they only describe a variation.

BEM solves this by dividing names into three roles:

```text
BEM
│
├── Block     → independent component
├── Element   → part of that component
└── Modifier  → variation or setting
```

💡 Think of a **car**:

```text
car              → Block
car__wheel       → Element
car__wheel--flat → Modifier
```

The same idea is applied to CSS class names. `C-02-css-maintainability-bem.pdf`
## 1. Why is a structured CSS methodology needed?

The previous lecture introduced CSS preprocessors such as Sass as one possible solution for maintainability problems.

This lecture introduces a second approach:

```text
CSS maintainability problems
│
├── Additional tools
│   └── Sass preprocessor
│
└── Methodical/structured approach
    └── BEM naming convention
```

▣ **CSS methodology**  
A collection of conventions and rules that guides developers in writing CSS so that it remains maintainable and scalable.

Such approaches may define:

- naming conventions;
- rules for choosing selectors;
- patterns for structuring CSS rules.

They are often supported by tools such as linters.

▣ **Linter**  
A tool that checks source code for violations of defined rules or conventions.

💡 For example, a BEM linter could warn about a class such as:

```css
.menu_item
```

because the expected BEM element syntax is:

```css
.menu__item
```

❗ A preprocessor adds language features, while a methodology primarily adds **rules and discipline**.
## 2. What is BEM?

▣ **BEM - Block Element Modifier**  
A CSS naming convention based on dividing parts of a user interface into blocks, elements and modifiers.

BEM was originally developed by Yandex.

Its central goal is to create a CSS structure that is:

- well-defined;
- easy to read;
- scalable;
- reusable.

BEM works exclusively with CSS classes and deliberately avoids:

- IDs;
- deeply nested selectors;
- selectors that depend too strongly on HTML structure.

## Why does BEM avoid IDs and nesting?

There are two main reasons.

### 1. Avoid linking presentation too closely to structure

Consider:

```css
nav ul li a {
  color: blue;
}
```

This style depends on a very specific HTML structure:

```html
<nav>
  <ul>
    <li>
      <a>...</a>
    </li>
  </ul>
</nav>
```

If the HTML structure changes, the CSS may stop applying.

With BEM:

```css
.menu__item {
  color: blue;
}
```

The class describes the role directly. It does not matter whether the element is an `<a>`, `<li>` or another tag.

### 2. Keep specificity low

Consider:

```css
#header nav ul li a.active {
  color: red;
}
```

This selector has high specificity and can be difficult to override.

A BEM selector normally uses one class:

```css
.menu__item--active {
  color: red;
}
```

❗ BEM prefers simple class selectors so that CSS remains easier to extend and override.

→ Result: CSS is less dependent on the exact HTML hierarchy and remains more reusable.
## 3. The BEM ecosystem

BEM is primarily a methodology, but the lecture notes that it is surrounded by additional conventions and tools, such as:

- conventions for project file structures;
- JavaScript support such as `i-bem.js`;
- linters such as `postcss-bem-linter`.

BEM can also be combined with preprocessors such as Sass.

💡 These are not competing ideas:

```text
Sass
→ helps write and generate CSS

BEM
→ helps name and structure CSS classes
```

A project could therefore use both:

```scss
$activeColor: red;

.menu__item--active {
  color: $activeColor;
}
```

Here:

- the variable comes from Sass;
- the class name follows BEM.
## 4. What are the three basic parts of BEM?

## 4.1 Block

▣ **Block**  
A logically and functionally independent, reusable unit of a website.

Examples from the lecture:

- menu block;
- login block.

Possible block class names:

```css
.menu
```

```css
.login
```

A block should make sense as its own component.

💡 Examples:

```text
menu
login form
search bar
card
button
```

Blocks can be placed inside other blocks.

For example:

```html
<header class="header">
  <nav class="menu">
    ...
  </nav>
</header>
```

Here:

- `header` is one block;
- `menu` is another block;
- the menu happens to be placed inside the header.

❗ Nesting blocks in HTML does not mean their CSS class names must be combined.

You normally write:

```css
.header {
  ...
}

.menu {
  ...
}
```

rather than:

```css
.header .menu {
  ...
}
```

because the `menu` should remain reusable elsewhere.
## 4.2 Element

▣ **Element**  
A component that belongs to a block and is semantically tied to that block.

An element cannot meaningfully exist independently from its block.

Examples from the lecture:

- a menu item inside a menu;
- a password field inside a login block.

BEM syntax:

```text
block__element
```

Examples:

```css
.menu__item
```

```css
.login__password
```

The two underscores `__` mean:

> “This is an element belonging to this block.”

💡 Mental model:

```text
menu
└── menu__item

login
└── login__password
```

An element is not merely any child in the HTML structure. It is a meaningful part of a block.

For example:

```html
<nav class="menu">
  <a class="menu__item">Home</a>
</nav>
```

Here:

- `.menu` is the independent component;
- `.menu__item` is a part of that component.
## 4.3 Modifier

▣ **Modifier**  
A class that represents a setting, state or variation of a block or element.

Modifiers can change:

- appearance;
- behavior;
- size;
- state;
- theme.

Examples from the lecture:

- a menu element is highlighted;
- a login password element has a large input size.

BEM syntax for a block modifier:

```text
block--modifier
```

Example:

```css
.button--large
```

BEM syntax for an element modifier:

```text
block__element--modifier
```

Examples:

```css
.menu__item--active
```

```css
.login__password--big
```

The two hyphens `--` mean:

> “This is a modified version or state.”

💡 Mental model:

```text
menu                         → Block
menu__item                   → Element
menu__item--active           → Modified element
```
## 5. How can you identify Block, Element and Modifier?

Use these three questions:

### Is it an independent reusable component?

Then it is probably a **Block**.

```css
.menu
```

### Is it a meaningful part that belongs to a block?

Then it is probably an **Element**.

```css
.menu__item
```

### Does it describe a state or variation?

Then it is probably a **Modifier**.

```css
.menu__item--active
```

A quick map:

```text
What is it?
│
├── Independent component?
│      └── Block
│
├── Part of a block?
│      └── Element
│
└── Different state/version?
       └── Modifier
```
## 6. BEM naming conventions

The lecture gives the following naming rules.

## Block name

Permitted characters include:

- letters;
- numbers;
- hyphens.

Examples:

```css
.menu
```

```css
.login
```

```css
main-menu
```
## Element name

Pattern:

```text
.blockName__elementName
```

Examples:

```css
.menu__item
```

```css
.login__password
```

The element name is connected to the block name with two underscores:

```text
block + __ + element
```
## Modifier name

Modifier of a block:

```text
.blockName--modifier
```

Example:

```css
.menu--vertical
```

Modifier of an element:

```text
.blockName__elementName--modifier
```

Examples from the lecture:

```css
.menu__item--active
```

```css
.login__password--big
```

The modifier is connected using two hyphens:

```text
block or element + -- + modifier
```
## Visual syntax map

```text
.menu__item--active
│      │       │
│      │       └── Modifier
│      └────────── Element
└───────────────── Block
```

Or:

```text
Block __ Element -- Modifier
```

❗ Remember:

```text
__ = belongs to the block
-- = variation or state
```
## 7. How does the lecture’s complete BEM example work?

The lecture contains two files:

```text
style.css
page.html
```
## `style.css`

```css
/* Block */
.menu {
  background-color: lightblue;
}

/* Element */
.menu__item {
  text-transform: uppercase;
}

/* Modifier */
.menu__item--active {
  color: red;
  font-style: italic;
}
```

Let us examine each rule.
### Block rule

```css
.menu {
  background-color: lightblue;
}
```

`.menu` represents the complete navigation menu.

It gives the entire menu a light-blue background.

```text
.menu
→ the whole navigation block
```
### Element rule

```css
.menu__item {
  text-transform: uppercase;
}
```

`.menu__item` represents every item belonging to the menu.

```css
text-transform: uppercase;
```

causes the visible text to be displayed in uppercase.

For example:

```text
Home
```

is displayed as:

```text
HOME
```
### Modifier rule

```css
.menu__item--active {
  color: red;
  font-style: italic;
}
```

This class represents the currently active menu item.

It makes that item:

- red;
- italic.

The modifier does not replace the element class. It adds a variation to it.
## `page.html`

```html
<!DOCTYPE html>
<html>
[...]
<body>
  [...]
  <nav class="menu">
    <a
      class="menu__item menu__item--active"
      href="home.html">
      Home
    </a>

    <a
      class="menu__item"
      href="articles.html">
      Articles
    </a>

    <a
      class="menu__item"
      href="contact.html">
      Contact
    </a>
  </nav>
  [...]
</body>
</html>
```

The `[...]` marks omitted HTML that is not relevant to the example.
## 8. Why does the active item have two classes?

This is one of the most important ideas in the example:

```html
<a class="menu__item menu__item--active">
  Home
</a>
```

The element has both:

```text
menu__item
```

and:

```text
menu__item--active
```

Why?

Because it is simultaneously:

1. a normal menu item;
2. an active version of that menu item.

The first class provides the base styling:

```css
.menu__item {
  text-transform: uppercase;
}
```

The second class provides only the additional active styling:

```css
.menu__item--active {
  color: red;
  font-style: italic;
}
```

Therefore, the browser combines both rules.

```text
.menu__item
→ uppercase

.menu__item--active
→ red + italic
```

→ Result for `Home`:

```text
HOME
```

displayed in uppercase, red and italic.

❗ A modifier normally supplements the base class rather than replacing it.
## 9. How is each link styled?

## Home

```html
<a
  class="menu__item menu__item--active"
  href="home.html">
  Home
</a>
```

Matching rules:

```css
.menu__item
```

and:

```css
.menu__item--active
```

→ Result:

- uppercase;
- red;
- italic.
## Articles

```html
<a class="menu__item" href="articles.html">
  Articles
</a>
```

Matching rule:

```css
.menu__item
```

→ Result:

- uppercase;
- normal colour;
- normal font style.
## Contact

```html
<a class="menu__item" href="contact.html">
  Contact
</a>
```

Matching rule:

```css
.menu__item
```

→ Result:

- uppercase;
- normal colour;
- normal font style.
## Entire navigation

```html
<nav class="menu">
```

Matching rule:

```css
.menu
```

→ Result:

- light-blue background for the whole menu.

The final visible result shown on page 13 is approximately:

```text
HOME ARTICLES CONTACT
```

with:

- a light-blue navigation background;
- all items uppercase;
- `HOME` red and italic because it is the active item.
## 10. Why not write the CSS using nested selectors?

Without BEM, someone might write:

```css
nav {
  background-color: lightblue;
}

nav a {
  text-transform: uppercase;
}

nav a.active {
  color: red;
  font-style: italic;
}
```

This works, but it links the styling to:

- the `<nav>` element;
- `<a>` elements inside it;
- an `active` class inside that structure.

The BEM version is:

```css
.menu {
  background-color: lightblue;
}

.menu__item {
  text-transform: uppercase;
}

.menu__item--active {
  color: red;
  font-style: italic;
}
```

Advantages:

- the role of each class is visible;
- the styles do not depend on specific HTML tags;
- selectors remain simple;
- the component is easier to move or reuse.

For example, this could still work:

```html
<div class="menu">
  <button class="menu__item menu__item--active">
    Home
  </button>
</div>
```

The tags changed, but the BEM roles remain clear.
## 11. What does the page-10 diagram demonstrate?

The example image on page 10 marks several parts of a website as blocks, elements and modifiers.

Examples illustrated in the image include:

- a `logo` as a block;
- an `input` as a block;
- a `menu` as a block;
- individual menu entries as menu elements;
- a `button` as a block;
- a large input as a modified input;
- a green-themed button as a modified button.

The mental distinction is:

```text
button
→ reusable independent component

button with green theme
→ same block with a modifier
```

And:

```text
menu
→ independent block

menu entry
→ element belonging to menu
```

❗ Whether something is a block or an element depends on its role in the design.

For example, a button can be an independent block even when it appears inside a larger login block.
## 12. Can blocks be nested?

Yes. The lecture explicitly states that blocks can be nested inside one another.

Example:

```html
<section class="login">
  <button class="button button--green">
    Sign in
  </button>
</section>
```

Here:

- `login` is a block;
- `button` is also an independent block;
- the button is physically located inside the login block.

This is different from an element such as:

```html
<input class="login__password">
```

because `login__password` is specifically defined as belonging to the login block.

Mental model:

```text
login
├── login__password    → element of login
└── button             → separate block nested inside login
```
## 13. Is every HTML child automatically a BEM element?

No.

HTML nesting and BEM categorization are not the same thing.

Consider:

```html
<div class="card">
  <button class="button">
    Save
  </button>
</div>
```

The button is an HTML child of the card, but it can remain a separate block:

```text
card
└── button block
```

It does not necessarily have to be named:

```css
.card__button
```

Use `.card__button` only when the button is semantically specific to the card and is not intended as an independent reusable component.

❗ BEM is based on semantic relationships, not merely the DOM hierarchy.
## 14. Why does BEM use only classes?

Classes offer a practical balance:

- they can be reused;
- they have relatively low specificity;
- they are easy to combine;
- they clearly express BEM names.

Compare:

```css
#menu {
  ...
}
```

with:

```css
.menu {
  ...
}
```

The ID selector has higher specificity and is intended to identify a unique HTML element.

The class selector is easier to reuse and override.

Similarly, BEM avoids selectors such as:

```css
header nav ul li a {
  ...
}
```

because they depend heavily on structure.

❗ The objective is not merely shorter selectors. The objective is **predictable, reusable selectors**.
## 15. Benefits and limitations of BEM

## Benefits

BEM and similar methodologies can produce more maintainable and scalable CSS through:

- better readability;
- standardized structures;
- predictable naming;
- low selector specificity;
- reduced dependence on HTML structure.

Tools can also help developers follow the methodology.

For example, a linter can automatically check whether class names comply with the selected convention.
## Limitations

### 1. The methodology must be learned

Developers must correctly understand:

- what qualifies as a block;
- what qualifies as an element;
- what qualifies as a modifier;
- how the naming syntax works.

### 2. It requires discipline

Without tool support, developers must consistently follow the rules themselves.

For example, a team might accidentally mix:

```css
.menu__item
```

with:

```css
.menu-item
```

and:

```css
.active-menu-link
```

The CSS would still technically work, but the project would lose the consistency that BEM is intended to provide.

❗ BEM only improves maintainability when the team applies it consistently.
## 16. How does BEM fit into the larger CSS-maintainability topic?

The lecture ends by presenting three broad approaches:

```text
CSS maintainability
│
├── 1. Additional tools
│      └── Sass preprocessors
│
├── 2. Methodical structure
│      └── BEM naming convention
│
└── 3. Component-based web development
       └── each component has its own CSS
```

The third approach is only introduced here. Its details belong to later lecture material.

❗ For this lecture, the important focus is the second approach: BEM.
## 17. Likely exam questions

## What is BEM, and what problem does it solve?

▣ BEM is a CSS naming convention based on blocks, elements and modifiers. It aims to create readable, reusable and scalable CSS while keeping selector specificity low and avoiding excessive coupling between HTML structure and presentation.
## What is a Block?

▣ A block is a logically and functionally independent, reusable unit of a website.

Examples:

```css
.menu
```

```css
.login
```

Blocks can be nested inside other blocks.
## What is an Element?

▣ An element is a component of a block that is semantically tied to that block and cannot meaningfully exist independently.

Pattern:

```text
.block__element
```

Example:

```css
.menu__item
```
## What is a Modifier?

▣ A modifier represents a state, setting or variation of a block or element.

Patterns:

```text
.block--modifier
```

```text
.block__element--modifier
```

Examples:

```css
.menu--vertical
```

```css
.menu__item--active
```
## Explain the BEM syntax

```text
Block __ Element -- Modifier
```

- `__` connects a block to its element.
- `--` connects a block or element to a modifier.

Example:

```css
.login__password--big
```

means:

```text
login       → block
password    → element
big         → modifier
```
## Why does the active menu link use two classes?

```html
class="menu__item menu__item--active"
```

Because the link needs:

- the normal element styling from `.menu__item`;
- the additional state styling from `.menu__item--active`.

The browser combines both classes.
## Why does BEM avoid IDs and nested selectors?

BEM avoids them to:

- reduce coupling between CSS and HTML structure;
- keep specificity low;
- improve reusability;
- make styles easier to extend and override.
## Can BEM be combined with Sass?

Yes. BEM controls naming and structure, while Sass provides preprocessing features such as variables and mixins.

Example:

```scss
$activeColor: red;

.menu__item--active {
  color: $activeColor;
}
```
## What are the advantages and disadvantages of BEM?

### Advantages

- standardized naming;
- improved readability;
- low specificity;
- better scalability;
- better reuse;
- possible tool support.

### Disadvantages

- must be learned and understood;
- requires consistency and discipline;
- without tooling, developers must manually ensure compliance.
## 18. Final lecture map

```text
CSS becomes difficult to maintain
│
├── unclear class names
├── high selector specificity
├── strong dependency on HTML structure
└── inconsistent project structure
        │
        ▼
BEM methodology
        │
        ├── Block
        │    └── independent reusable component
        │
        ├── Element
        │    └── meaningful part of a block
        │
        └── Modifier
             └── state or variation
        │
        ▼
Naming syntax
        │
        ├── .block
        ├── .block__element
        ├── .block--modifier
        └── .block__element--modifier
        │
        ▼
Simple class selectors
        │
        ├── lower specificity
        ├── less structural coupling
        ├── clearer meaning
        └── improved scalability
```

## Core takeaway

❗ BEM does not add new capabilities to CSS. It adds a predictable way of **thinking about and naming user-interface parts**.

```text
What is the independent component?
→ Block

What part belongs to it?
→ Element

What state or variation does it have?
→ Modifier
```

→ Result: Developers can look at a class such as:

```css
.menu__item--active
```

and immediately understand:

> This is the active version of an item belonging to the menu block.
