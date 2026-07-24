# G-03 Vue.js Templates - Lecture Summary

This lecture explains **how a Vue component connects its JavaScript data and behavior to the HTML displayed in the browser**.

The central mental model is:

```text
JavaScript component
        ↓
provides data and methods
        ↓
Vue template
        ↓
Vue evaluates interpolation and directives
        ↓
Browser DOM
```

A Vue template looks mostly like normal HTML, but Vue enriches it with:

1. **Interpolation** - placing dynamic values inside text.
2. **Directives** - adding dynamic behavior to HTML elements.

The lecture can therefore be mapped as:

```text
Vue Template
│
├── Interpolation
│   ├── Displays values
│   ├── Evaluates JavaScript expressions
│   └── Works only in text content
│
└── Directives
    ├── v-bind       → dynamic HTML attributes
    ├── v-on         → event handling
    ├── v-if         → conditional rendering
    ├── v-else-if
    ├── v-else
    ├── v-for        → repeated rendering
    └── v-model      → two-way form binding
```

This summary is based only on the uploaded lecture. `G-03-vuejs-templates_en.pdf`
## 1. How templates fit into MVVM

The diagram on page 2 places the **template inside the View part** of Vue’s MVVM structure.

```html
<div id="app">
  <h1>Hallo {{text}}</h1>
  <input v-on:input="changeText">
</div>
```

The corresponding component contains data and methods:

```javascript
const MyApp = {
  data() {
    // ...
  },

  methods: {
    // ...
  }
};
```

Example reactive data:

```javascript
data() {
  return {
    text: "WEB2"
  };
}
```

## Mapping the pieces

```text
Model
└── Reactive data
    └── text: "WEB2"

ViewModel
└── Vue component
    ├── data()
    └── methods

View
└── HTML template
    ├── {{text}}
    └── v-on:input="changeText"
```

▣ **Template**  
A template describes what the user interface should look like and how it is connected to the component’s data and methods.

❗ The template is not simply static HTML. Vue reads the template, evaluates its expressions and keeps the displayed DOM synchronized with the component’s reactive data.

💡 Suppose `text` initially contains `"WEB2"`:

```html
<h1>Hello {{text}}</h1>
```

→ Result:

```html
<h1>Hello WEB2</h1>
```

When `text` changes, Vue updates the displayed heading automatically.
## 2. What is a Vue template?

▣ **Vue template language**  
Vue’s template language is a **superset of HTML**.

A superset means:

```text
Every valid HTML structure is also valid in a Vue template.
```

Vue adds extra capabilities to HTML:

1. Interpolation
2. Directives

For example, this is ordinary HTML:

```html
<h1>Hello</h1>
```

This is a Vue template:

```html
<h1>Hello {{text}}</h1>
```

The element is still an ordinary `<h1>`, but `{{text}}` is processed by Vue.

❗ Vue does not replace HTML with a completely different language. It adds dynamic expressions and special attributes to familiar HTML.
## 3. What is interpolation in Vue.js?

▣ **Interpolation**  
Interpolation is the dynamic evaluation of placeholders inside a template.

Vue uses **Mustache syntax**:

```vue
{{ expression }}
```

The expression can be:

- A property from `data()`
- A JavaScript function call
- A relational expression
- An arithmetic expression
- A ternary expression

The general process is:

```text
Template contains {{ expression }}
              ↓
Vue evaluates expression
              ↓
Result is inserted as text into the DOM
```
## 3.1 Interpolating a data property

Component:

```javascript
const app = {
  data() {
    return {
      text: "WEB2"
    };
  }
};
```

Template:

```html
<h1>Hello {{text}}</h1>
```

`text` refers to the property returned by `data()`.

→ Result:

```html
<h1>Hello WEB2</h1>
```

### Syntax explanation

```html
{{text}}
```

- `{{` starts the interpolation.
- `text` is the JavaScript expression.
- `}}` ends the interpolation.
## 3.2 Calling a function inside interpolation

```html
<strong>{{Date()}}</strong>
```

`Date()` is a JavaScript function call.

Vue evaluates the function and places its returned value inside the `<strong>` element.

→ Result could look like:

```html
<strong>Sun Jul 19 2026 15:30:00 GMT+0200</strong>
```

The exact text depends on the current date and environment.
## 3.3 Using expressions inside interpolation

```html
<span>{{number % 2 === 0 ? "even" : "odd"}}</span>
```

This expression checks whether `number` is even or odd.

### Step-by-step

```javascript
number % 2
```

Calculates the remainder after division by 2.

```javascript
number % 2 === 0
```

Checks whether that remainder is zero.

```javascript
condition ? "even" : "odd"
```

This is a ternary expression:

```text
If condition is true  → "even"
Otherwise             → "odd"
```

💡 For:

```javascript
number = 6;
```

→ Result:

```html
<span>even</span>
```

For:

```javascript
number = 5;
```

→ Result:

```html
<span>odd</span>
```
## 4. What happens when interpolated data changes?

When a property from `data()` is referenced in interpolation, Vue establishes a **data binding**.

```text
Reactive property
      ↓
Interpolation reads property
      ↓
Property changes
      ↓
Vue updates the corresponding DOM text
```

Example:

```javascript
data() {
  return {
    text: "WEB2"
  };
}
```

```html
<h1>Hello {{text}}</h1>
```

Initially:

```text
text = "WEB2"
```

→ Result:

```html
<h1>Hello WEB2</h1>
```

Later:

```text
text = "Vue"
```

→ Updated result:

```html
<h1>Hello Vue</h1>
```

❗ You do not manually find the `<h1>` element and replace its text. Vue performs the DOM update because the property is reactive.
## 5. What are the limitations of interpolation?

The Mustache syntax can only be used where **text content** can appear.

▣ **DOM text node**  
A text node is the textual content located between an element’s opening and closing tags.

Valid:

```html
<h1>Hello {{text}}</h1>
```

Here, `{{text}}` is used as text content.

Invalid usage:

```html
<h1 title="{{tooltip}}">Hello</h1>
```

The `title` value is an HTML attribute, not a text node.

❗ Mustache interpolation cannot be used to dynamically set HTML attributes.

For dynamic attributes, Vue uses the `v-bind` directive:

```html
<h1 v-bind:title="tooltip">Hello</h1>
```

or its shorthand:

```html
<h1 :title="tooltip">Hello</h1>
```
## 6. What is a Vue directive?

▣ **Directive**  
A directive is a special HTML attribute that begins with the prefix `v-`.

Directives are used for operations such as:

- Changing HTML attributes
- Reacting to events
- Adding or removing elements
- Repeating elements
- Connecting form controls to data

Examples:

```html
<h1 v-bind:title="tooltip">Hello</h1>
```

```html
<button v-on:click="validateData">Validate</button>
```

```html
<p v-if="hasError">An error occurred.</p>
```

The value assigned to a directive is normally a JavaScript expression.

For example:

```html
<p v-if="list.length > 0">
```

The expression is:

```javascript
list.length > 0
```

Vue evaluates it to either `true` or `false`.
## 7. How is a directive structured?

The lecture provides this general form:

```text
v-directive[:argument][.modifier]="argument"
```

A clearer representation is:

```text
v-directive[:directiveArgument][.modifier]="JavaScript expression"
```

Example:

```html
<button v-on:click.prevent="submitForm">
```

Breakdown:

```text
v-on          → directive name
click         → directive argument
prevent       → modifier
submitForm    → directive value/expression
```

## Directive name

Identifies what Vue should do.

Examples:

```text
v-bind
v-on
v-if
v-for
v-model
```

## Directive argument

Provides additional information to the directive.

Example:

```html
v-bind:title
```

Here, `title` tells `v-bind` which HTML attribute to control.

Another example:

```html
v-on:click
```

Here, `click` tells `v-on` which event to listen for.

## Modifier

Changes or configures the directive’s behavior.

Example:

```html
v-on:submit.prevent
```

The `.prevent` modifier tells Vue to execute:

```javascript
event.preventDefault();
```

## Directive value

Usually a JavaScript expression.

```html
v-if="list.length > 0"
```

The value is:

```javascript
list.length > 0
```
## 8. Built-in and custom directives

Vue provides a collection of **built-in directives**.

This lecture considers examples including:

```text
v-bind
v-on
v-if
v-else-if
v-else
v-for
v-model
```

It is also possible to create custom directives, but custom directives are explicitly outside the scope of this lecture.

❗ The lecture only introduces selected options of the built-in directives. Many directives support additional capabilities that are not discussed here.
## 9. How does `v-bind` dynamically set HTML attributes?

▣ **`v-bind`**  
`v-bind` connects an HTML attribute to a JavaScript expression or reactive property.

General structure:

```html
v-bind:attributeName="expression"
```

Example:

```html
<h1 v-bind:title="tooltip">Hello {{text}}</h1>
```

Here:

```text
v-bind       → use attribute binding
title        → HTML attribute being controlled
tooltip      → component property whose value is assigned
```

Component data might be:

```javascript
data() {
  return {
    text: "Horst",
    tooltip: "A Tooltip"
  };
}
```

→ Result:

```html
<h1 title="A Tooltip">Hello Horst</h1>
```

The slide writes the resulting text with an exclamation mark:

```html
<h1 title="A Tooltip">Hello Horst!</h1>
```

The exact output depends on whether the exclamation mark is included in the template.
## 9.1 `v-bind` shorthand

Instead of:

```html
<h1 v-bind:title="tooltip">Hello {{text}}</h1>
```

you can write:

```html
<h1 :title="tooltip">Hello {{text}}</h1>
```

Therefore:

```text
v-bind:attribute
```

and:

```text
:attribute
```

mean the same thing.

❗ The colon `:` is Vue syntax. It means that the attribute value should be evaluated as a JavaScript expression.

Compare:

```html
<h1 title="tooltip">
```

This sets the literal text `"tooltip"`.

```html
<h1 :title="tooltip">
```

This reads the value of the JavaScript property `tooltip`.
## 10. How does `v-bind` dynamically set CSS classes?

Vue can bind the `class` attribute to an object:

```html
<div v-bind:class="{ active: isActive, error: hasError }">
  [...]
</div>
```

The object contains:

```javascript
{
  active: isActive,
  error: hasError
}
```

Each key is a CSS class name:

```text
active
error
```

Each value determines whether the class should be included:

```text
isActive
hasError
```

Assume:

```javascript
isActive = false;
hasError = true;
```

Vue evaluates:

```text
active → false → class excluded
error  → true  → class included
```

→ Result:

```html
<div class="error">[...]</div>
```

💡 With:

```javascript
isActive = true;
hasError = true;
```

→ Result:

```html
<div class="active error">[...]</div>
```

❗ Vue is not applying or removing the styles directly here. It is dynamically changing the element’s class list. The browser then applies the corresponding CSS rules.
## 11. How does `v-bind` dynamically set inline CSS?

Vue can bind the `style` attribute to an object:

```html
<span v-bind:style="{ color: fcolor, fontSize: fsize + 'em' }">
  Hello WEB2
</span>
```

Assume:

```javascript
fcolor = "orange";
fsize = 3;
```

Vue evaluates:

```javascript
color: fcolor
```

as:

```javascript
color: "orange"
```

It evaluates:

```javascript
fontSize: fsize + "em"
```

as:

```javascript
fontSize: "3em"
```

→ Result:

```html
<span style="color: orange; font-size: 3em;">
  Hello WEB2
</span>
```

❗ CSS properties containing a hyphen are normally written in camelCase inside JavaScript objects.

CSS:

```css
font-size
```

JavaScript object property:

```javascript
fontSize
```

Another example:

```text
background-color → backgroundColor
```
## 12. How does `v-on` handle events?

▣ **`v-on`**  
`v-on` registers an event listener on a DOM element.

General syntax:

```html
v-on:eventName="handler"
```

Example:

```html
<button v-on:click="validateData"></button>
```

Here:

```text
v-on          → event directive
click         → DOM event
validateData  → method to execute
```

The corresponding component may contain:

```javascript
const app = {
  methods: {
    validateData() {
      // validation logic
    }
  }
};
```

When the user clicks the button, Vue calls:

```javascript
validateData();
```
## 12.1 `v-on` shorthand

Instead of:

```html
<button v-on:click="validateData"></button>
```

you can write:

```html
<button @click="validateData"></button>
```

Therefore:

```text
v-on:event
```

and:

```text
@event
```

mean the same thing.

Examples:

```html
<input @input="changeText">
```

```html
<form @submit="submitForm">
```

```html
<button @click="validateData">
  Validate
</button>
```
## 12.2 Event modifiers

A modifier can configure event handling.

Example:

```html
<form v-on:submit.prevent="submitForm">
```

or:

```html
<form @submit.prevent="submitForm">
```

The `.prevent` modifier causes Vue to call:

```javascript
event.preventDefault();
```

This prevents the browser’s normal form-submission behavior.

Then Vue calls:

```javascript
submitForm();
```

❗ Without `.prevent`, submitting a normal HTML form may reload or navigate away from the current page.
## 13. How do `v-if`, `v-else-if` and `v-else` work?

These directives conditionally display elements.

```html
<span v-if="list.length > 0">
  {{list.length}} data records found.
</span>

<span v-else-if="hasError">
  Error reading the data.
</span>

<span v-else>
  No data records found.
</span>
```

Vue evaluates the conditions from top to bottom.

## Case 1: The list contains elements

```javascript
list.length > 0
```

is true.

→ Result:

```html
<span>3 data records found.</span>
```

The other branches are not rendered.

## Case 2: The list is empty and an error exists

```javascript
list.length > 0
```

is false.

```javascript
hasError
```

is true.

→ Result:

```html
<span>Error reading the data.</span>
```

## Case 3: The list is empty and there is no error

Both earlier conditions are false.

→ Result:

```html
<span>No data records found.</span>
```
## Does `v-if` only hide the element visually?

No.

❗ When the expression is falsy, the element is either:

- Not added to the DOM, or
- Removed from the DOM

That is different from merely hiding an existing element with CSS.

Conceptually:

```text
v-if condition is true
→ element exists in DOM

v-if condition is false
→ element does not exist in DOM
```

▣ **Falsy**  
A falsy value is a JavaScript value that behaves like `false` in a Boolean condition.

Examples include:

```javascript
false
0
""
null
undefined
```
## 14. How does `v-for` repeat elements?

▣ **`v-for`**  
`v-for` renders an element multiple times based on an iterable collection, such as an array or object.

The required pattern is:

```text
element in expression
```

Example:

```html
<ul>
  <li v-for="element in list">
    {{element.name}}
  </li>
</ul>
```

Assume:

```javascript
data() {
  return {
    list: [
      { name: "HTML" },
      { name: "CSS" },
      { name: "JavaScript" }
    ]
  };
}
```

Vue processes the array one item at a time:

```text
First iteration  → element = { name: "HTML" }
Second iteration → element = { name: "CSS" }
Third iteration  → element = { name: "JavaScript" }
```

→ Result:

```html
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>
```

### Syntax explanation

```html
<li v-for="element in list">
```

- `v-for` tells Vue to repeat the `<li>`.
- `list` is the iterable collection.
- `element` is a local variable representing the current item.

Inside the repeated element:

```html
{{element.name}}
```

reads the `name` property of the current item.

❗ `element` only represents one entry during the current iteration. `list` is the complete collection.
## 15. What is `v-model`?

▣ **`v-model`**  
`v-model` creates a bidirectional, or two-way, binding between an HTML form element and a component property.

It can be applied to:

```text
input
select
textarea
```

The data flows in both directions:

```text
Component property changes
        ↓
Form element is updated

User changes form element
        ↓
Component property is updated
```

This corresponds to the **binder component** in the MVVM mental model.
## 16. One-way binding versus two-way binding

Interpolation gives data flow from the model to the view:

```text
data property
     ↓
{{ interpolation }}
     ↓
displayed text
```

`v-model` supports both directions:

```text
data property
     ⇅
form control
```

Example:

```html
<input v-model="text">
```

If:

```javascript
text = "Vue";
```

the input displays:

```text
Vue
```

If the user changes the input to:

```text
Spring
```

Vue updates:

```javascript
text = "Spring";
```

Any other template location using `text` is also updated.
## 17. Complete `v-model` example

The lecture provides two files:

```text
hello.html
hello.js
```
## 17.1 `hello.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Hello Vue</title>
  <meta charset="utf-8" />
</head>

<body>
  <div id="app">
    <h1>Hello {{text}}</h1>

    <!-- text field is bound to
         property "text" -->
    <input v-model="text" />
  </div>

  <script type="module"
          src="hello.js"></script>
</body>
</html>
```

### Explanation

```html
<!DOCTYPE html>
```

Declares an HTML5 document.

```html
<html lang="en">
```

Starts the HTML document and declares English as its language.

```html
<title>Hello Vue</title>
```

Sets the browser tab title.

```html
<meta charset="utf-8" />
```

Specifies UTF-8 character encoding.

```html
<div id="app">
```

Creates the HTML element where the Vue application will be mounted.

```html
<h1>Hello {{text}}</h1>
```

Displays the current value of `text`.

```html
<input v-model="text" />
```

Creates two-way binding between the input field and `text`.

```html
<script type="module" src="hello.js"></script>
```

Loads `hello.js` as a JavaScript module.
## 17.2 `hello.js`

```javascript
// Source for import shortened
import { createApp } from "...";

const app = {
  data() {
    return {
      text: ""
    };
  }
};

createApp(app).mount("#app");
```

### Explanation

```javascript
import { createApp } from "...";
```

Imports Vue’s `createApp` function.

The actual source URL or package path is shortened in the lecture.

```javascript
const app = {
```

Creates the root component definition.

```javascript
data() {
```

Defines the component’s reactive data.

```javascript
return {
  text: ""
};
```

Creates a reactive property named `text`.

Its initial value is an empty string.

```javascript
createApp(app)
```

Creates a Vue application using the component definition.

```javascript
.mount("#app");
```

Mounts the Vue application on the HTML element whose ID is `app`:

```html
<div id="app">
```
## 18. Step-by-step execution of the complete example

At application start:

```javascript
text = "";
```

Therefore:

```html
<h1>Hello {{text}}</h1>
```

appears approximately as:

```html
<h1>Hello </h1>
```

The input is also empty:

```html
<input value="">
```

Now suppose the user types:

```text
Vue
```

Because of:

```html
<input v-model="text">
```

Vue updates:

```javascript
text = "Vue";
```

Because the heading uses:

```html
{{text}}
```

Vue also updates the heading.

→ Result:

```html
<h1>Hello Vue</h1>
```

The complete data flow is:

```text
User types "Vue"
        ↓
<input v-model="text">
        ↓
text becomes "Vue"
        ↓
{{text}} is reevaluated
        ↓
Heading becomes "Hello Vue"
```

❗ Every change to the text field is immediately transferred to the `text` property, and changes to the `text` property are immediately reflected in the text field.
## 19. How the directives relate to one another

| Requirement | Vue syntax | Meaning |
|---|---|---|
| Display data as text | `{{text}}` | Interpolation |
| Set an attribute dynamically | `:title="tooltip"` | `v-bind` |
| Apply classes conditionally | `:class="{ active: isActive }"` | Class binding |
| Set inline styles dynamically | `:style="{ color: fcolor }"` | Style binding |
| React to a click | `@click="method"` | `v-on` |
| Render conditionally | `v-if="condition"` | Conditional rendering |
| Add another condition | `v-else-if="condition"` | Alternative branch |
| Add a fallback | `v-else` | Final branch |
| Repeat an element | `v-for="item in list"` | List rendering |
| Bind a form control | `v-model="property"` | Two-way binding |
## 20. One combined example using the lecture concepts

The following example combines the ideas introduced in the lecture without introducing a different architectural topic.

```html
<div id="app">
  <h1 :title="tooltip">
    Hello {{text}}
  </h1>

  <input v-model="text">

  <button @click="validateData">
    Validate
  </button>

  <p v-if="list.length > 0">
    {{list.length}} data records found.
  </p>

  <p v-else-if="hasError">
    Error reading the data.
  </p>

  <p v-else>
    No data records found.
  </p>

  <ul>
    <li v-for="element in list">
      {{element.name}}
    </li>
  </ul>
</div>
```

Possible component:

```javascript
import { createApp } from "...";

const app = {
  data() {
    return {
      text: "",
      tooltip: "Enter your name",
      hasError: false,
      list: [
        { name: "HTML" },
        { name: "CSS" },
        { name: "JavaScript" }
      ]
    };
  },

  methods: {
    validateData() {
      this.hasError = this.text === "";
    }
  }
};

createApp(app).mount("#app");
```

### What each connection does

```html
{{text}}
```

Displays the property as text.

```html
:title="tooltip"
```

Sets the `title` attribute dynamically.

```html
v-model="text"
```

Synchronizes the input and `text`.

```html
@click="validateData"
```

Calls a component method when the button is clicked.

```html
v-if="list.length > 0"
```

Displays a message only when the list contains entries.

```html
v-else-if="hasError"
```

Displays an error when the earlier condition is false and `hasError` is true.

```html
v-else
```

Provides the fallback.

```html
v-for="element in list"
```

Creates one `<li>` for every list entry.

→ Result: the component’s data, event behavior and rendered HTML are connected declaratively through the template.
## 21. Exam-focused questions

## What is the difference between interpolation and `v-bind`?

▣ **Interpolation** inserts evaluated values into text content:

```html
<h1>Hello {{text}}</h1>
```

▣ **`v-bind`** assigns evaluated values to HTML attributes:

```html
<h1 :title="tooltip">Hello</h1>
```

❗ Mustache syntax cannot be used for HTML attributes.
## What is the general structure of a directive?

```text
v-directive[:argument][.modifier]="JavaScript expression"
```

Example:

```html
<form v-on:submit.prevent="submitForm">
```

```text
v-on        → directive
submit      → argument
prevent     → modifier
submitForm  → expression/handler
```
## What is the difference between `v-bind` and `v-on`?

```text
v-bind
→ sends component data into an HTML attribute

v-on
→ reacts to a DOM event and invokes component behavior
```

Example:

```html
<button :title="tooltip" @click="validateData">
  Validate
</button>
```
## What happens when a `v-if` expression is false?

The corresponding element is not added to the DOM or is removed from the DOM.

❗ It is not merely hidden visually.
## What is the purpose of `v-for`?

It repeatedly renders an element for every item in an iterable collection.

```html
<li v-for="element in list">
  {{element.name}}
</li>
```
## What does two-way binding mean in `v-model`?

```text
Property change → form control updates
Form change     → property updates
```

Example:

```html
<input v-model="text">
```
## 22. Final mental model

Think of the Vue component as a box containing:

```text
Data
Methods
```

The template is the visible interface connected to that box:

```text
{{...}}
→ read data into text

v-bind / :
→ read data into attributes

v-on / @
→ send user events to methods

v-if
→ decide whether an element exists

v-for
→ create elements from a collection

v-model
→ synchronize form input and data in both directions
```

The complete cycle is:

```text
Component data
      ↓
Interpolation and directives evaluate it
      ↓
Vue creates or updates the DOM
      ↓
User interacts with the DOM
      ↓
Event directives or v-model update the component
      ↓
Vue updates the DOM again
```

→ Result: Vue templates provide a declarative connection between **reactive component state**, **HTML presentation**, and **user interaction**.
