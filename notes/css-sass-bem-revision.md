# Lecture 1: CSS Preprocessors - Sass  
## Last-Minute Exam Summary

## 1. Main problem kya hai?

Normal CSS large project mein difficult ho sakti hai because:

- stylesheet bahut bada ho jata hai;
- same values aur declarations repeat hote hain;
- readability aur maintainability poor ho jati hai;
- selectors over-specific ho sakte hain;
- unused ya dead CSS code reh sakta hai.

❗ Main reason: CSS mein traditionally modularization aur reuse ke mechanisms limited the.

→ Result: Lecture ka solution hai **CSS preprocessor**, example: **Sass**. `C-01-css-maintainability-preprocessors.pdf`
## 2. CSS Preprocessor kya hai?

▣ **CSS Preprocessor**  
Ek tool jo CSS ko extra features ke saath extend karta hai aur phir source code ko normal CSS mein translate karta hai.

```text
SCSS/Sass code
      ↓
Sass preprocessor
      ↓
Normal CSS
      ↓
Browser
```

❗ Browser Sass directly nahi samajhta. Browser sirf generated CSS run karta hai.

💡 Analogy:  
Sass ek translator hai. Developer advanced language mein likhta hai, translator usse browser ki language-CSS-mein convert karta hai.
## 3. Sass kya hai?

▣ **Sass** = Syntactically Awesome Style Sheets

Sass CSS ko mainly in features se extend karta hai:

- Variables
- Mixins
- Imports
- Nested rules

Basic fact:

- `.scss` → SCSS syntax
- `.sass` → indented syntax

❗ Detailed SCSS vs indented-syntax comparison NP tha, isliye exam ke liye detail mein nahi karna.
## 4. Sass Variables

▣ **Variable**  
Ek named value jo multiple CSS rules mein reuse hoti hai.

Variable `$` se start hota hai.

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

Generated CSS:

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

💡 Meaning:

```scss
$primaryColor: #ffe4e1;
```

means color ek jagah define hui. Agar value badli, Sass compile karne par har usage update ho jayega.

→ Result: Frequently used values centralize ho jati hain.
## 5. Sass Variables vs CSS Custom Properties

Native CSS mein bhi variables jaisa mechanism hota hai:

```css
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

### Difference

### Sass variable

```scss
$primaryColor: red;
```

- compile time par replace hota hai;
- generated CSS mein variable nahi bachta.

### CSS custom property

```css
--primaryColor: red;
```

- browser runtime tak available rehta hai;
- cascade mein participate karta hai;
- JavaScript se change kiya ja sakta hai.

❗ Exam line:

> Sass variables are processed at compile time, while CSS custom properties remain available at runtime.
## 6. Mixins

▣ **Mixin**  
Reusable block of CSS declarations.

Variable sirf ek value reuse karta hai.  
Mixin poora declaration block reuse karta hai.

General syntax:

```scss
@mixin mixinName($parameter) {
  /* declarations */
}

@include mixinName(argument);
```

Lecture example:

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

Generated CSS:

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

💡 `@include box(200px)` ka matlab:

- `$side = 200px`
- width aur height dono 200px.

→ Result: Duplicate declaration blocks avoid hote hain.
## 7. Imports

▣ **Import**  
Stylesheet ko multiple files mein divide karke modular banane ka mechanism.

Syntax:

```scss
@import 'base';
```

Lecture idea:

### `base.scss`

```scss
$baseColor: #2471a3;
$fontStack: Arial, sans-serif;

@mixin tile($side) {
  width: $side;
  height: $side;
}
```

### Another SCSS file

```scss
@import 'base';

@mixin box($side) {
  @include tile($side);
  border-radius: 5px;
}

.header-box {
  @include box(150px);
  background-color: $baseColor;
}
```

Generated CSS:

```css
.header-box {
  width: 150px;
  height: 150px;
  border-radius: 5px;
  background-color: #2471a3;
}
```

❗ `$fontStack` generated CSS mein nahi aaya because use hi nahi hua.

→ Result: Source multiple files mein organized ho sakta hai, but final CSS combined hoti hai.
## Sass import vs native CSS `@import`

Native CSS:

```css
@import 'basis.css';
```

Browser imported CSS file ke liye additional request karta hai.

Lecture ke according disadvantage:

- separate HTTP requests;
- sequential loading;
- loading time increase ho sakta hai.

Sass import build time par files combine karta hai.

```text
Multiple SCSS files
       ↓
Sass compilation
       ↓
One CSS file
```
## 8. Nested Rules

▣ **Nesting**  
Related selectors ko ek doosre ke andar likhna.

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

Generated CSS:

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

## `&` kya karta hai?

▣ `&` current parent selector ko represent karta hai.

```scss
a {
  &:hover {
    font-size: larger;
  }
}
```

Nested inside `.navbar`, this becomes:

```css
.navbar a:hover {
  font-size: larger;
}
```

❗ Too much nesting avoid karna chahiye because it creates overspecific selectors.

Example:

```scss
.page {
  .content {
    .article {
      span {
        color: red;
      }
    }
  }
}
```

Generated:

```css
.page .content .article span {
  color: red;
}
```

→ Result: HTML structure ke saath tight coupling aur high specificity.
## 9. Sass ke Benefits aur Costs

## Benefits

- modularization;
- reuse;
- less duplicate code;
- better readability;
- DRY principle support.

▣ **DRY** = Don’t Repeat Yourself.

## Costs

- extra compilation/build step;
- additional tools required;
- debugging/source support needed;
- kuch Sass features native CSS mein bhi available hain.

❗ Exam conclusion:

> Before using a preprocessor feature, check whether native CSS already provides a suitable solution.
## 10. Sass One-Minute Revision

```text
Problem              Sass Solution
----------------------------------------
Repeated value       Variable
Repeated CSS block   Mixin
Large stylesheet     Import
Scattered selectors  Nesting
```

### Must remember

```scss
$color: red;              // variable
@mixin box($side) {...}   // mixin definition
@include box(200px);      // mixin use
@import 'base';           // import
&:hover                   // parent selector
```
## Lecture 2: BEM
## Last-Minute Exam Summary

## 1. Main idea kya hai?

BEM ek tool ya programming language nahi hai.

▣ **BEM - Block Element Modifier**  
CSS classes ko consistently name aur structure karne ki methodology.

Mental model:

```text
Block     → independent component
Element   → block ka part
Modifier  → state ya variation
```

Example:

```text
menu
menu__item
menu__item--active
```

BEM ka goal:

- readable CSS;
- scalable CSS;
- reusable components;
- low selector specificity;
- HTML structure se less coupling. `C-02-css-maintainability-bem.pdf`
## 2. CSS Methodology kya hoti hai?

▣ **CSS Methodology**  
Rules aur conventions ka set jo developers ko consistent aur maintainable CSS likhne mein help karta hai.

It may define:

- naming conventions;
- selector rules;
- CSS structure patterns.

Tools such as linters methodology ko enforce kar sakte hain.

▣ **Linter**  
Tool jo code ko defined conventions ke against check karta hai.

❗ Other methodologies ka examples wala page NP tha. Exam ke liye OOCSS, SMACSS, SUIT CSS details ignore karo.
## 3. BEM sirf classes kyun use karta hai?

BEM deliberately avoid karta hai:

- IDs;
- deeply nested selectors;
- selectors dependent on HTML hierarchy.

## Reason 1: HTML structure se less coupling

Without BEM:

```css
nav ul li a {
  color: blue;
}
```

Ye exact structure par depend karta hai.

BEM:

```css
.menu__item {
  color: blue;
}
```

Element `<a>`, `<button>` ya kuch aur ho sakta hai. Class role ko describe karti hai.

## Reason 2: Low specificity

High specificity:

```css
#header nav ul li a.active {
  color: red;
}
```

BEM:

```css
.menu__item--active {
  color: red;
}
```

→ Result: Styles easier to extend and override.
## 4. Block

▣ **Block**  
Logically aur functionally independent, reusable unit of a website.

Examples:

```css
.menu
.login
```

💡 Examples:

- menu;
- login form;
- button;
- search box.

Blocks ek doosre ke andar nested ho sakte hain.

```html
<header class="header">
  <nav class="menu">
    ...
  </nav>
</header>
```

Yahan `header` aur `menu` dono separate blocks hain.

❗ HTML ke andar nested hone ka matlab yeh nahi ki CSS selector bhi nested hona chahiye.
## 5. Element

▣ **Element**  
Block ka meaningful part jo apne block se semantically linked hota hai.

Syntax:

```text
block__element
```

Examples:

```css
.menu__item
.login__password
```

Mental model:

```text
menu
└── menu__item
```

❗ Element independently meaningful nahi hota. `menu__item` menu block ka part hai.
## 6. Modifier

▣ **Modifier**  
Block ya element ki state, setting ya variation.

Syntax:

```text
block--modifier
```

or:

```text
block__element--modifier
```

Examples:

```css
.menu--vertical
.menu__item--active
.login__password--big
```

Modifiers appearance, behavior, size ya state change kar sakte hain.

Mental map:

```text
menu                   → block
menu__item             → element
menu__item--active     → modified element
```
## 7. Naming Convention

## Block

```css
.menu
.login
```

## Element

```css
.block__element
```

Example:

```css
.menu__item
```

## Block modifier

```css
.block--modifier
```

Example:

```css
.menu--vertical
```

## Element modifier

```css
.block__element--modifier
```

Example:

```css
.menu__item--active
```

Most important memory trick:

```text
__ = belongs to block
-- = variation/state
```

Visual breakdown:

```text
.menu__item--active
  │      │       │
Block  Element  Modifier
```
## 8. Complete Lecture Example

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

    <a class="menu__item" href="articles.html">
      Articles
    </a>

    <a class="menu__item" href="contact.html">
      Contact
    </a>
  </nav>
  [...]
</body>
</html>
```
## 9. Active item ke paas two classes kyun hain?

```html
class="menu__item menu__item--active"
```

Because `Home` simultaneously:

1. normal menu item hai;
2. active menu item bhi hai.

Base class:

```css
.menu__item {
  text-transform: uppercase;
}
```

Modifier:

```css
.menu__item--active {
  color: red;
  font-style: italic;
}
```

Browser dono classes ke styles combine karega.

→ Result for Home:

- uppercase;
- red;
- italic.

❗ Modifier generally base class ko replace nahi karta. Usko supplement karta hai.
## 10. Final Output of Example

Entire navigation:

```css
.menu
```

→ light-blue background.

All links:

```css
.menu__item
```

→ uppercase.

Home only:

```css
.menu__item--active
```

→ red and italic.

Approximate result:

```text
HOME ARTICLES CONTACT
```

with `HOME` red and italic.
## 11. Block vs Element ka tricky point

Har HTML child automatically element nahi hota.

```html
<div class="card">
  <button class="button">
    Save
  </button>
</div>
```

Button card ke andar hai, but it can remain a separate reusable block:

```text
card block
└── button block
```

It does not automatically become:

```css
.card__button
```

Use `.card__button` only when button specifically card ka meaningful dependent part ho.

❗ BEM categorization semantic relationship par based hai, sirf DOM nesting par nahi.
## 12. BEM with Sass

BEM aur Sass combine ho sakte hain.

```scss
$activeColor: red;

.menu__item--active {
  color: $activeColor;
}
```

Here:

- BEM class naming deta hai;
- Sass reusable variable deta hai.

```text
BEM  → structure and naming
Sass → preprocessing features
```
## 13. Benefits and Limitations

## Benefits

- predictable naming;
- better readability;
- low specificity;
- less dependency on HTML structure;
- better reusability;
- scalable CSS;
- linter support possible.

## Limitations

- methodology learn karni padti hai;
- team ko consistently follow karna padta hai;
- tool support ke bina discipline required hai.

❗ BEM automatically maintainability guarantee nahi karta. Team ko rules correctly apply karne honge.
## 14. BEM One-Minute Revision

```text
Question                           Answer
------------------------------------------------
Independent reusable component?   Block
Part of a block?                   Element
State or variation?                Modifier
```

Syntax:

```css
.block
.block__element
.block--modifier
.block__element--modifier
```

Example:

```css
.menu
.menu__item
.menu__item--active
```
## Final Comparison: Sass vs BEM

```text
Sass
→ CSS ko extra features deta hai
→ variables, mixins, imports, nesting
→ compile karke normal CSS banata hai

BEM
→ CSS naming methodology hai
→ Block, Element, Modifier
→ browser ke liye koi compilation required nahi
```

❗ Best exam sentence:

> Sass is a tool-based approach for CSS maintainability, while BEM is a methodological approach based on structured class naming.

### Ultra-short memory map

```text
Sass = How to write reusable CSS source

BEM  = How to name and organize CSS classes
```
