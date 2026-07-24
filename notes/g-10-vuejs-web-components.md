## Lecture Summary Request

# G-10 - Web Components

This lecture explains how to build **reusable browser-native components** that are not tied specifically to Vue, React, or Angular. It introduces three technologies that work together:

```text
Web Component
│
├── Custom Elements → Gives the component its own HTML tag and behaviour
├── Shadow DOM      → Protects the component’s internal DOM and CSS
└── HTML Templates
    ├── <template>  → Reusable internal structure
    └── <slot>      → Places where users can insert custom content
```

The lecture’s examples mainly build a reusable `<person-box>` component and a specialized text input. `G-vuejs-web-componentes.pdf`
## 1. Mental model: a packaged electronic device

Imagine you are building a reusable digital display:

| Web Component concept | Analogy |
|---|---|
| Custom Element | The device’s name and outer casing |
| Shadow DOM | The protected internal electronics |
| `<template>` | The factory blueprint |
| `<slot>` | A replaceable section, such as a label |
| Attributes | Configuration knobs given by the user |

For example:

```html
<person-box
  name="Sue Miller"
  position="Chief Technology Officer"
  img="img/sue.jpg">
</person-box>
```

Here, `<person-box>` is the device, while `name`, `position`, and `img` configure it.
## 2. Why are Web Components needed?

Vue, React, Angular, and other frontend frameworks have their own component systems.

A Vue component, for example, is designed for Vue. It cannot necessarily be copied directly into an Angular or React application.

❗ **Problem:** Framework-specific components are difficult to reuse across different frameworks.

▣ **Web Components** are a standardized browser-based approach for creating reusable components using native browser APIs.

→ Result: A Web Component can potentially be used in plain HTML or inside different frameworks.
## 3. What technologies form Web Components?

▣ **Web Components are not one single standard.** They are formed from three browser technologies.

## 3.1 Custom Elements

A JavaScript API for defining new HTML elements together with their behaviour.

Example:

```html
<person-box></person-box>
```

The browser does not normally have a `<person-box>` element. JavaScript defines what it means and how it behaves.
## 3.2 Shadow DOM

A JavaScript API for creating an **encapsulated DOM subtree**.

It protects the internal structure and styling of a component from unwanted outside effects.
## 3.3 HTML Templates

HTML elements used to describe reusable structures.

The two important elements discussed in the lecture are:

```html
<template>
<slot>
```
## 4. What are Custom Elements?

▣ **Custom Elements** allow developers to define their own HTML elements, including their structure and behaviour.

There are two types.

## 4.1 Autonomous custom elements

These are completely new and independent elements.

Example:

```html
<person-box></person-box>
```

Their JavaScript class extends:

```javascript
HTMLElement
```
## 4.2 Customized built-in elements

These extend an already existing HTML element.

Example:

```html
<input is="limit-text-field">
```

This is still fundamentally an `<input>`, but its behaviour has been extended.

Its JavaScript class extends:

```javascript
HTMLInputElement
```

❗ Do not confuse the two forms:

```html
<person-box></person-box>
```

is an autonomous element.

```html
<input is="limit-text-field">
```

is a customized built-in element.
## 5. How is a Custom Element created?

A Custom Element is normally defined in two steps:

```text
Step 1: Implement a JavaScript class
        ↓
Step 2: Register that class with the browser
        ↓
Result: The element can be used in HTML
```
## 6. Step 1: Implementing a Custom Element

A Custom Element is implemented as an ES6 class.

## 6.1 Inheritance

For an autonomous element:

```javascript
class PersonBox extends HTMLElement {
}
```

For a customized input:

```javascript
class LimitTextField extends HTMLInputElement {
}
```

This places the component in the browser’s DOM object hierarchy.

💡 The class defines the element’s:

- structure;
- data processing;
- event handling;
- lifecycle behaviour;
- rendering.
## 7. Custom Element lifecycle callbacks

Custom Elements provide callbacks similar to Vue lifecycle hooks.

## 7.1 `connectedCallback()`

▣ Called when the element is inserted or mounted into the DOM.

```javascript
connectedCallback() {
  this.render();
}
```

Analogy: The component has been plugged into the webpage, so it can now start working.
## 7.2 `disconnectedCallback()`

▣ Called when the element is removed or unmounted from the DOM.

It can be used for cleanup, such as removing event listeners or stopping timers.
## 7.3 `attributeChangedCallback()`

▣ Called when one of the monitored attributes is added, changed, or removed.

For example, it could react when:

```html
<person-box name="New Name">
```

changes to another name.

❗ The lecture names this callback but does not provide its implementation.
## 8. Example 1: autonomous `<person-box>`

## Complete code from the lecture

```javascript
class PersonBox extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.render();
  }

  render() {
    const name = this.getAttribute("name");
    const position = this.getAttribute("position");
    const img = this.getAttribute("img");

    this.innerHTML = `
      <img src="${img}" alt="Image of ${name}">
      <h2>${name}</h2>
      <p>${position}</p>
    `;

    /* Add styling etc... */
  }
}
```
## 8.1 What does `extends HTMLElement` mean?

```javascript
class PersonBox extends HTMLElement
```

`PersonBox` inherits the basic capabilities of normal HTML elements.

It can therefore:

- appear in the DOM;
- have attributes;
- contain HTML;
- receive events;
- use standard DOM methods.
## 8.2 Why is `super()` required?

```javascript
constructor() {
  super();
}
```

`super()` calls the constructor of `HTMLElement`.

In simple terms:

```text
Create the normal HTML-element part first
                  ↓
Then create the special PersonBox part
```

❗ In a derived class, `super()` must be called before using `this`.
## 8.3 When does rendering happen?

```javascript
connectedCallback() {
  this.render();
}
```

When the browser attaches `<person-box>` to the DOM, it automatically calls `connectedCallback()`.

That callback then calls:

```javascript
this.render();
```

→ Result: The element builds its internal HTML when it appears on the page.
## 8.4 Reading attributes

```javascript
const name = this.getAttribute("name");
const position = this.getAttribute("position");
const img = this.getAttribute("img");
```

Suppose HTML contains:

```html
<person-box
  name="Sue Miller"
  position="Chief Technology Officer"
  img="img/sue.jpg">
</person-box>
```

Then:

```javascript
this.getAttribute("name")
```

returns:

```text
Sue Miller
```

Similarly:

```javascript
this.getAttribute("position")
```

returns:

```text
Chief Technology Officer
```
## 8.5 Creating the internal HTML

```javascript
this.innerHTML = `
  <img src="${img}" alt="Image of ${name}">
  <h2>${name}</h2>
  <p>${position}</p>
`;
```

This is a JavaScript **template literal**.

The `${...}` expressions insert JavaScript values.

For example:

```javascript
const name = "Sue Miller";
```

makes this:

```html
<h2>${name}</h2>
```

become:

```html
<h2>Sue Miller</h2>
```

→ Result:

```html
<person-box>
  <img src="img/sue.jpg" alt="Image of Sue Miller">
  <h2>Sue Miller</h2>
  <p>Chief Technology Officer</p>
</person-box>
```

At this stage, these children are placed in the normal DOM.
## 9. Example 2: customized `<input>`

The second component extends an existing input field.

## Complete code from the lecture

```javascript
class LimitTextField extends HTMLInputElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.render();
  }

  render() {
    const max = this.getAttribute("maxlength");

    const span = document.createElement("span");
    span.textContent = `0/${max}`;
    this.after(span);

    this.addEventListener("input", (event) => {
      let inputLength = event.target.value.length;
      this.nextSibling.textContent = `${inputLength}/${max}`;
    });
  }
}
```
## 9.1 What does it inherit?

```javascript
class LimitTextField extends HTMLInputElement
```

It inherits the functionality of an ordinary HTML `<input>`.

Therefore, it already knows how to:

- accept keyboard input;
- store a value;
- use `maxlength`;
- fire input events;
- participate in forms.

The class only adds new behaviour.
## 9.2 Reading the maximum length

```javascript
const max = this.getAttribute("maxlength");
```

With:

```html
<input is="limit-text-field" maxlength="5">
```

the value of `max` is:

```text
5
```
## 9.3 Creating the counter

```javascript
const span = document.createElement("span");
span.textContent = `0/${max}`;
this.after(span);
```

Step by step:

```javascript
document.createElement("span");
```

creates:

```html
<span></span>
```

Then:

```javascript
span.textContent = `0/${max}`;
```

sets its text:

```html
<span>0/5</span>
```

Finally:

```javascript
this.after(span);
```

places it immediately after the input.

→ Result:

```html
<input ...>
<span>0/5</span>
```
## 9.4 Updating the counter

```javascript
this.addEventListener("input", (event) => {
  let inputLength = event.target.value.length;
  this.nextSibling.textContent = `${inputLength}/${max}`;
});
```

The `"input"` event occurs whenever the user changes the field’s value.

Suppose the user types:

```text
Hey
```

Then:

```javascript
event.target.value
```

is:

```text
Hey
```

and:

```javascript
event.target.value.length
```

is:

```text
3
```

The component changes the next sibling from:

```html
<span>0/5</span>
```

to:

```html
<span>3/5</span>
```

💡 `this.nextSibling` refers to the span that was inserted after the input.

→ Result:

```text
[Hey  ] 3/5
```

❗ Despite one slide’s wording about showing how many characters “can still be entered,” the implemented counter displays **used characters / maximum characters**, such as `3/5`.
## 10. Step 2: Registering a Custom Element

Creating the class is not enough. The browser must be told which HTML name belongs to which class.

This is done with:

```javascript
customElements.define(...)
```

▣ `customElements` provides access to the browser’s `CustomElementRegistry`.
## 10.1 Parameters of `define()`

The method can receive:

```javascript
customElements.define(name, class, options);
```

### Parameter 1: name

```javascript
"person-box"
```

The name must:

- use kebab-case;
- contain a hyphen.

Valid:

```text
person-box
user-card
limit-text-field
```

Invalid for a Custom Element:

```text
person
usercard
button
```

❗ The hyphen helps distinguish custom element names from native HTML element names.
### Parameter 2: implementation class

```javascript
PersonBox
```

This is the class that defines the element’s behaviour.
### Parameter 3: extended built-in element

Used only for customized built-in elements.

```javascript
{ extends: "input" }
```

This tells the browser that the component specializes `<input>`.
## Registration code

```javascript
customElements.define("person-box", PersonBox);

customElements.define(
  "limit-text-field",
  LimitTextField,
  { extends: "input" }
);
```

→ Result: The browser now understands both custom elements.
## 11. Using Custom Elements in HTML

## Complete `index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Web Components Demo</title>

  <script src="PersonBox.js" type="module"></script>
  <script src="LimitTextField.js" type="module"></script>
</head>

<body>
  <h2>PersonBox component:</h2>

  <person-box
    name="Sue Miller"
    position="Chief Technology Officer"
    img="img/sue.jpg">
  </person-box>

  <h2>LimitTextField component:</h2>

  <input is="limit-text-field" maxlength="5" />
</body>
</html>
```
## 11.1 Loading the JavaScript files

```html
<script src="PersonBox.js" type="module"></script>
<script src="LimitTextField.js" type="module"></script>
```

These files contain the implementation and registration code.

The lecture loads them as ECMAScript modules using:

```html
type="module"
```
## 11.2 Using the autonomous element

```html
<person-box
  name="Sue Miller"
  position="Chief Technology Officer"
  img="img/sue.jpg">
</person-box>
```

This uses a completely new HTML tag.
## 11.3 Using the customized built-in element

```html
<input is="limit-text-field" maxlength="5" />
```

The element is still written as `<input>`.

The `is` attribute selects the registered specialization:

```html
is="limit-text-field"
```
## 12. Are Custom Elements alone sufficient?

No.

When the basic `<person-box>` uses:

```javascript
this.innerHTML = ...
```

its internal elements are inserted into the normal DOM.

That causes three problems.

## 12.1 External CSS can affect the component

For example, the page may contain:

```css
img {
  width: 500px;
}
```

That rule could unintentionally affect the image inside `<person-box>`.
## 12.2 Component CSS can affect the page

If the component inserts:

```css
p {
  font-weight: bold;
}
```

into the normal document, it may affect paragraphs outside the component.
## 12.3 Outside JavaScript can modify the component

For example:

```javascript
document.querySelector("person-box img").remove();
```

could accidentally remove the internal image.

❗ **Open problem:** There is no proper encapsulation.

→ Result: CSS and JavaScript conflicts or unwanted cross-effects may occur.

This motivates the second technology: **Shadow DOM**.
## 13. What is the Shadow DOM?

▣ **Shadow DOM** is a DOM structure and JavaScript API for managing encapsulated subtrees.

A normal DOM element can receive a hidden internal DOM tree called a **shadow tree**.

```text
Regular document
│
└── <person-box>              ← Shadow host
      │
      └── #shadow-root        ← Shadow root
           ├── <img>
           ├── <h2>
           ├── <p>
           └── <style>
```
## 14. Important Shadow DOM terms

## Shadow host

▣ The normal DOM element to which the Shadow DOM is attached.

Example:

```html
<person-box></person-box>
```

`<person-box>` is the shadow host.
## Shadow root

▣ The root node of the shadow tree.

Created using:

```javascript
this.attachShadow(...)
```
## Shadow tree

▣ The hidden internal DOM tree contained below the shadow root.
## Shadow boundary

▣ The transition or border between the regular DOM and the Shadow DOM.

The diagram on page 27 illustrates the regular document tree, the shadow host, shadow root, shadow tree, and the boundary separating the two scopes. `G-vuejs-web-componentes.pdf`
## 15. Creating a Shadow DOM

A shadow root is attached using:

```javascript
myDomElement.attachShadow({ mode: "open" });
```

Example:

```javascript
let root = this.attachShadow({ mode: "open" });
```

The shadow root can then be accessed with:

```javascript
myDomElement.shadowRoot
```

Elements can be added through the standard DOM API.
## 16. Open versus closed Shadow DOM

`attachShadow()` receives an object containing a `mode` property.

## 16.1 Open Shadow DOM

```javascript
this.attachShadow({ mode: "open" });
```

Outside JavaScript can access the shadow root:

```javascript
element.shadowRoot
```

→ Result: The internal tree is encapsulated from ordinary DOM queries, but it can still be deliberately accessed through `shadowRoot`.
## 16.2 Closed Shadow DOM

```javascript
this.attachShadow({ mode: "closed" });
```

Outside JavaScript cannot retrieve the shadow root through:

```javascript
element.shadowRoot
```

It returns:

```javascript
null
```

❗ Closed mode provides stronger hiding through this API, although the lecture’s example uses open mode.
## 17. `<person-box>` with Shadow DOM

## Complete code from the lecture

```javascript
class PersonBox extends HTMLElement {
  /* [...] constructor, connectedCallback etc. */

  render() {
    const name = this.getAttribute("name");
    const position = this.getAttribute("position");
    const img = this.getAttribute("img");

    let root = this.attachShadow({ mode: "open" });

    root.innerHTML = `
      <img src="${img}" alt="Image of ${name}">
      <h2>${name}</h2>
      <p>${position}</p>
    `;

    let style = document.createElement("style");

    style.textContent = `
      :host {
        border: 1px solid lightgray;
        display: block;
      }

      img {
        float: left;
        [...]
      }
    `;

    root.appendChild(style);
  }
}
```

The lecture abbreviates part of the image CSS using `[...]`; the missing rules are not provided in the slides.
## 17.1 Attaching the shadow root

```javascript
let root = this.attachShadow({ mode: "open" });
```

`this` is the current `<person-box>` element.

Therefore:

```text
<person-box> becomes the shadow host
```

and `root` refers to its newly created shadow root.
## 17.2 Building the shadow tree

```javascript
root.innerHTML = `
  <img src="${img}" alt="Image of ${name}">
  <h2>${name}</h2>
  <p>${position}</p>
`;
```

The HTML is now added inside the shadow root-not directly into the normal document DOM.
## 17.3 Adding encapsulated CSS

```javascript
let style = document.createElement("style");
```

creates a style element.

```javascript
style.textContent = `...`;
```

adds CSS rules.

```javascript
root.appendChild(style);
```

puts the style element inside the Shadow DOM.

→ Result: The CSS rules apply to this shadow tree rather than the whole document.
## 18. What does the `:host` selector mean?

```css
:host {
  border: 1px solid lightgray;
  display: block;
}
```

▣ `:host` is a special CSS pseudo-class that selects the element hosting the Shadow DOM.

In this example, it selects:

```html
<person-box>
```

Even though the `<style>` element is inside the Shadow DOM, `:host` lets it style the outer component element.

So:

```css
:host {
  border: 1px solid lightgray;
}
```

means:

> Give the `<person-box>` itself a light-grey border.
## 19. How does Shadow DOM hide internal elements?

## Code from the lecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Web Components Demo</title>
  <script src="PersonBox.js"></script>
</head>

<body>
  <h2>PersonBox-Component:</h2>

  <person-box
    name="Sue Miller"
    position="Chief Technology Officer"
    img="img/sue.jpg">
  </person-box>

  <script>
    console.log(document.querySelector("img"));
    /*
      → Output: null because the img element is hidden
        in the Shadow DOM
    */

    let root =
      document.querySelector("person-box").shadowRoot;

    console.log(root.querySelector("img"));
    /*
      → Output:
      <img src="img/sue.jpg" alt="Image of Sue Miller">

      Access through the shadow root is possible because
      mode="open".
    */
  </script>
</body>
</html>
```
## Normal query

```javascript
document.querySelector("img");
```

searches the regular document tree.

It does not automatically cross the shadow boundary.

→ Result:

```javascript
null
```
## Explicit Shadow DOM query

```javascript
document.querySelector("person-box").shadowRoot
```

first retrieves the component’s shadow root.

Then:

```javascript
root.querySelector("img");
```

searches inside the shadow tree.

→ Result: The image is found.

❗ This works because the Shadow DOM was created with:

```javascript
mode: "open"
```
## 20. What are HTML Templates?

▣ **HTML Templates** provide reusable HTML structures that can be declared in an HTML document and instantiated through JavaScript.

Two important elements are:

```html
<template>
<slot>
```
## 21. The `<template>` element

▣ `<template>` describes reusable HTML content.

Its special behaviour is:

- the browser parses the content;
- the content exists as template data;
- the content is not displayed;
- its CSS rules are not active merely because they are inside the template;
- JavaScript can clone and insert the content later.

Analogy: It is a cookie cutter, not a baked cookie.
## 22. Declaring a template

## `index.html` from the lecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Web Components Demo</title>
</head>

<body>
  <h2>PersonBox-Component:</h2>

  <person-box
    name="Sue Miller"
    position="Chief Technology Officer"
    img="img/sue.jpg">
  </person-box>

  <template id="person-box-template">
    <img src="${img}" alt="Image of ${name}" />
    <h2>${name}</h2>
    <p>${position}</p>

    <style>
      :host {
        border: 1px solid lightgray;
        display: block;
      }

      img {
        float: left;
        [...]
      }
    </style>
  </template>

  <script src="PersonBox.js"></script>
</body>
</html>
```
## 22.1 Why is an ID assigned?

```html
<template id="person-box-template">
```

The ID allows JavaScript to find the template:

```javascript
document.getElementById("person-box-template");
```
## 22.2 Why is the template not shown?

The browser does not render the contents of `<template>` directly.

Therefore, this:

```html
<template>
  <h2>${name}</h2>
</template>
```

does not show `${name}` on the page.

The style rules inside it also do not become active until the template content is inserted somewhere.
## 22.3 Are `${name}` placeholders built into `<template>`?

No.

The lecture explicitly notes that strings such as:

```html
${name}
${position}
${img}
```

are arbitrarily chosen placeholders for the example’s JavaScript.

They are not automatically processed by the browser’s `<template>` element.

❗ JavaScript must replace them manually.
## 23. Instantiating the template in JavaScript

## Complete code from the lecture

```javascript
class PersonBox extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.render();
  }

  render() {
    const name = this.getAttribute("name");
    const position = this.getAttribute("position");
    const img = this.getAttribute("img");

    let root = this.attachShadow({ mode: "open" });

    let template =
      document.getElementById("person-box-template");

    let clone = template.content.cloneNode(true);

    root.appendChild(clone);

    root.innerHTML = root.innerHTML
      .replaceAll("${name}", name)
      .replace("${position}", position)
      .replace("${img}", img);
  }
}
```
## 23.1 Selecting the template

```javascript
let template =
  document.getElementById("person-box-template");
```

This retrieves:

```html
<template id="person-box-template">
```
## 23.2 Accessing its content

```javascript
template.content
```

The reusable nodes inside a `<template>` are available through its `content` property.
## 23.3 Cloning the template

```javascript
let clone = template.content.cloneNode(true);
```

`cloneNode(true)` creates a copy.

The argument `true` means:

> Clone the complete subtree, including all nested elements.

So the copy includes:

- `<img>`;
- `<h2>`;
- `<p>`;
- `<style>`;
- all child content.

💡 This is the actual **instantiation** of the template.
## 23.4 Inserting it into the Shadow DOM

```javascript
root.appendChild(clone);
```

The cloned template is inserted into the shadow root.

→ Result: It becomes the internal structure of this `<person-box>` instance.
## 23.5 Replacing placeholders

```javascript
root.innerHTML = root.innerHTML
  .replaceAll("${name}", name)
  .replace("${position}", position)
  .replace("${img}", img);
```

Suppose:

```javascript
name = "Sue Miller";
position = "Chief Technology Officer";
img = "img/sue.jpg";
```

Then the placeholders are converted into their actual values.

For example:

```html
<h2>${name}</h2>
```

becomes:

```html
<h2>Sue Miller</h2>
```

→ Result: One reusable template can generate different person boxes based on element attributes.
## 24. The `<slot>` element

▣ A `<slot>` defines a replaceable location inside a component template.

It provides functionality comparable to named slots in Vue.

Basic idea:

```text
Component defines an insertion point
                 ↓
User supplies content for that point
                 ↓
Browser displays supplied content there
```
## 25. Named slots

A slot receives a name:

```html
<slot name="mission-statement">
  Lorem Ipsum
</slot>
```

The user provides matching content with the `slot` attribute:

```html
<em slot="mission-statement">
  All creatures welcome.
</em>
```

The names connect the two:

```text
name="mission-statement"
          ↕
slot="mission-statement"
```
## 26. Complete slot example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Web Components Demo</title>
</head>

<body>
  <h2>PersonBox-Component:</h2>

  <person-box
    name="Sue Miller"
    position="Chief Technology Officer"
    img="img/sue.jpg">

    <em slot="mission-statement">
      All creatures welcome.
    </em>
  </person-box>

  <template id="person-box-template">
    <img src="${img}" alt="Image of ${name}" />
    <h2>${name}</h2>
    <p>${position}</p>

    <p>
      <slot name="mission-statement">
        Lorem Ipsum
      </slot>
    </p>

    <style>
      [...]
    </style>
  </template>

  <script src="PersonBox.js"></script>
</body>
</html>
```
## 26.1 Default slot content

```html
<slot name="mission-statement">
  Lorem Ipsum
</slot>
```

`Lorem Ipsum` is the fallback content.

It is shown when the user does not supply matching slot content.

Example:

```html
<person-box
  name="Sue Miller"
  position="Chief Technology Officer"
  img="img/sue.jpg">
</person-box>
```

→ Result:

```text
Lorem Ipsum
```

is displayed in that location.
## 26.2 Replacing the default content

The user supplies:

```html
<em slot="mission-statement">
  All creatures welcome.
</em>
```

The browser places it into:

```html
<slot name="mission-statement">
```

→ Result:

```html
<p>
  <em>All creatures welcome.</em>
</p>
```

appears at the slot’s position.
## 26.3 Important distinction: attributes versus slots

Attributes provide small configuration values:

```html
<person-box name="Sue Miller">
```

Slots provide actual HTML content:

```html
<em slot="mission-statement">
  All creatures welcome.
</em>
```

Use this mental model:

```text
Attribute → component data/configuration
Slot      → component content/markup
```
## 27. Full flow of the final `<person-box>`

```text
1. Browser reads:
   <person-box name="Sue Miller" ...>

2. Browser finds the registered PersonBox class.

3. PersonBox is inserted into the DOM.

4. connectedCallback() runs.

5. render() reads:
   name, position and img attributes.

6. attachShadow() creates an internal shadow root.

7. JavaScript finds the <template>.

8. template.content.cloneNode(true) copies the template.

9. The copy is appended to the shadow root.

10. Placeholder strings are replaced with attribute values.

11. Slot content is projected into the named <slot>.

12. Encapsulated HTML and CSS are displayed.
```

→ Result:

```text
<person-box>
│
├── Configuration from attributes
│   ├── Sue Miller
│   ├── Chief Technology Officer
│   └── img/sue.jpg
│
├── Internal structure from <template>
│
├── Protected internal DOM/CSS from Shadow DOM
│
└── Custom inserted content from <slot>
    └── All creatures welcome.
```
## 28. What browser support and libraries are mentioned?

The lecture states that the following are natively supported by most current browsers:

- Custom Elements;
- Shadow DOM;
- HTML Templates.

Libraries can simplify the creation and maintenance of Web Components. The lecture gives these examples:

- LitElement;
- Stencil;
- Solid.

It also names ready-made component libraries:

- Material Web Components;
- Vaadin Components;
- Elix.

Large frameworks provide support or extensions for Web Components, including:

- Vue and Web Components;
- Angular Elements;
- React support.

❗ The lecture only introduces these as examples; it does not explain their APIs.
## 29. Web Components versus Vue components

| Vue component | Web Component |
|---|---|
| Uses Vue’s component model | Uses browser standards |
| Usually defined with Vue APIs or `.vue` files | Defined with native JavaScript and HTML APIs |
| Rendering handled by Vue | Rendering is implemented manually or through a supporting library |
| Scoped CSS may be provided by Vue tooling | Encapsulation is provided by Shadow DOM |
| Vue slots | Native `<slot>` elements |
| Vue lifecycle hooks | Custom Element callbacks |
| Mainly intended for Vue applications | Intended to be usable across environments |

The conceptual relationships are:

```text
Vue mounted hook
       ≈
connectedCallback()

Vue unmounted hook
       ≈
disconnectedCallback()

Vue props
       ≈
HTML attributes

Vue named slots
       ≈
Native named <slot> elements
```

❗ They are similar concepts, but their exact APIs and behaviour are not identical.
## 30. Important exam questions

## What problem do Web Components solve?

They offer a standardized browser-native component model, reducing dependence on framework-specific component systems and improving reuse across different environments.
## What three technologies form Web Components?

1. Custom Elements;
2. Shadow DOM;
3. HTML Templates, particularly `<template>` and `<slot>`.
## What is the difference between autonomous and customized built-in elements?

An autonomous element defines a completely new HTML tag and extends `HTMLElement`.

```javascript
class PersonBox extends HTMLElement
```

A customized built-in element extends an existing native element.

```javascript
class LimitTextField extends HTMLInputElement
```

It is used through the `is` attribute:

```html
<input is="limit-text-field">
```
## How is a Custom Element defined?

1. Implement an ES6 class.
2. Register it with `customElements.define()`.
## What does `connectedCallback()` do?

It is called when the Custom Element is attached to the DOM. It is commonly used to initialize or render the component.
## Why is a hyphen required in a Custom Element name?

A Custom Element name must contain a hyphen, such as `person-box`, to distinguish it from existing and future native HTML elements.
## Why are Custom Elements alone not enough?

Their internal HTML and CSS initially remain part of the ordinary DOM, so external CSS and JavaScript can affect the component, while component styling may affect the outside page.

Shadow DOM provides the missing encapsulation.
## What is the difference between open and closed Shadow DOM?

With open mode:

```javascript
attachShadow({ mode: "open" })
```

outside code can access the internal root through `element.shadowRoot`.

With closed mode:

```javascript
attachShadow({ mode: "closed" })
```

`element.shadowRoot` returns `null`.
## What does `:host` select?

It selects the normal DOM element that hosts the Shadow DOM.

For this component:

```html
<person-box></person-box>
```

`:host` selects `<person-box>`.
## What is special about `<template>`?

Its contents are parsed but not displayed. JavaScript can clone its `content` and insert the clone into a component.
## What does `cloneNode(true)` mean?

It creates a deep copy, including the selected node’s nested descendants.
## What is the purpose of `<slot>`?

A slot defines a location in a component where the user can provide custom HTML content.
## 31. Final map of the lecture

```text
Motivation
│
├── Framework components are difficult to reuse across frameworks
│
└── Web Components provide browser standards
    │
    ├── 1. Custom Elements
    │   │
    │   ├── Autonomous elements
    │   ├── Customized built-in elements
    │   ├── ES6 classes
    │   ├── Lifecycle callbacks
    │   └── customElements.define()
    │
    ├── Problem after Custom Elements
    │   └── No proper encapsulation
    │
    ├── 2. Shadow DOM
    │   │
    │   ├── Shadow host
    │   ├── Shadow root
    │   ├── Shadow tree
    │   ├── Shadow boundary
    │   ├── Open versus closed mode
    │   └── Encapsulated HTML and CSS
    │
    └── 3. HTML Templates
        │
        ├── <template>
        │   ├── Declared but not rendered
        │   ├── Selected through JavaScript
        │   └── Cloned and inserted
        │
        └── <slot>
            ├── Insertion point
            ├── Named slot
            └── Default/fallback content
```

## Core sentence to remember

❗ **Custom Elements provide the identity and behaviour, Shadow DOM provides encapsulation, `<template>` provides reusable structure, and `<slot>` provides customizable content.**
