# G-06 - Vue.js Single File Components

## Mental model of the lecture

Imagine that every Vue component is a **small self-contained room**:

```text
Component.vue
│
├── <template>  → What the room looks like
├── <script>    → How the room behaves
└── <style>     → How the room is decorated
```

A browser cannot directly understand this `.vue` file. Therefore, a build tool processes it first:

```text
.vue files
    │
    ▼
Vite / bundler
    │
    ▼
Browser-compatible HTML + CSS + JavaScript
```

The complete lecture follows this path:

```text
Problem with earlier components
        ↓
Single File Components
        ↓
.vue file structure
        ↓
Browser cannot understand .vue
        ↓
Bundler and Vite
        ↓
Create a Vue project
        ↓
Understand the project structure
        ↓
Import and register SFCs
        ↓
Control whether component CSS is global or scoped
```

This summary is based on the uploaded lecture. `G-06-vuejs-single-file-components_en.pdf`
## 1. Why are Single File Components needed?

Earlier in Vue, a component could be written as a JavaScript object:

```javascript
const HelloComponent = {
  template: `
    <p>
      <strong>{{ helloText }}</strong>
    </p>
  `,

  data() {
    return {
      helloText: "Hello WEB2!",
    };
  },
};
```

This works for small examples, but it becomes inconvenient when an application contains many components.

## Problems with the previous approach

### 1. Poor modularization

The HTML template is embedded inside JavaScript as a string.

```javascript
template: `
  <p>
    <strong>{{ helloText }}</strong>
  </p>
`
```

This means HTML and JavaScript are mixed in a way that becomes difficult to manage.

### 2. Poor editor support

Because the template is only a JavaScript string, the development environment may provide weaker support for:

- HTML syntax highlighting
- HTML validation
- automatic formatting
- code completion
- error detection

Quotation marks and escaping can also become inconvenient.

### 3. CSS is outside the component

The component definition contains its HTML and JavaScript, but its CSS normally has to be written somewhere else.

```text
Component JavaScript → one place
Component template   → inside JavaScript
Component CSS        → another file
```

❗Therefore, everything belonging to one component is not grouped together.

→ Result: Vue introduces **Single File Components** to package a component’s template, behavior and styling into one file.
## 2. What is a Single File Component?

▣ **Single File Component**

A Single File Component, abbreviated as **SFC**, is a Vue component defined in a file with the extension:

```text
.vue
```

For example:

```text
Hello.vue
TodoCard.vue
UserProfile.vue
```

A Single File Component can contain three main aspects:

```text
1. HTML template
2. JavaScript component definition
3. CSS rules
```

These are written in three blocks:

```vue
<template>
  <!-- HTML -->
</template>

<script>
  // JavaScript
</script>

<style>
  /* CSS */
</style>
```

## Mental model

```text
Hello.vue
┌───────────────────────────────┐
│ <template>                    │
│   What should be displayed?   │
├───────────────────────────────┤
│ <script>                      │
│   What data and behavior?     │
├───────────────────────────────┤
│ <style>                       │
│   How should it look?         │
└───────────────────────────────┘
```

❗The three blocks do not represent three separate components.

Together, they define **one Vue component**.
## 3. Complete `Hello.vue` example

```vue
<template>
  <p class="helloBlock">
    <strong>{{ helloText }}</strong>
  </p>
</template>

<script>
export default {
  data() {
    return {
      helloText: "Hello WEB2!",
    };
  },
};
</script>

<style>
.helloBlock {
  color: orange;
  font-size: xx-large;
}
</style>
```

The three blocks are connected:

```text
<script>
helloText: "Hello WEB2!"
        │
        │ used through interpolation
        ▼
<template>
{{ helloText }}
        │
        │ element uses this CSS class
        ▼
<style>
.helloBlock
```

→ Result displayed in the browser:

```text
Hello WEB2!
```

It is shown in a very large orange font.
## 4. What does the `<template>` block do?

▣ **Template block**

The `<template>` block contains the HTML structure of the component.

```vue
<template>
  <p class="helloBlock">
    <strong>{{ helloText }}</strong>
  </p>
</template>
```

Annotated:

```vue
<template>
  <!-- Root element of this component -->
  <p class="helloBlock">

    <!-- Read the helloText property from the component -->
    <strong>{{ helloText }}</strong>

  </p>
</template>
```

The expression:

```vue
{{ helloText }}
```

uses Vue interpolation to display a property supplied by the component’s JavaScript.

## Rules for the template block

### It may only appear once

An SFC normally contains one `<template>` block.

```vue
<!-- Valid -->
<template>
  ...
</template>
```

You should not define two separate template blocks for the same component.

### The lecture requires a unique root element

The HTML inside the template must be wrapped in one root element.

Correct:

```vue
<template>
  <div>
    <h1>Hello</h1>
    <p>Welcome</p>
  </div>
</template>
```

Here, `<div>` is the root element.

Incorrect according to the lecture’s rule:

```vue
<template>
  <h1>Hello</h1>
  <p>Welcome</p>
</template>
```

There are two top-level elements.

💡 Think of the root element as the **outer box** containing the entire component.
## 5. What does the `<script>` block do?

▣ **Script block**

The `<script>` block contains the JavaScript required by the component.

```vue
<script>
export default {
  data() {
    return {
      helloText: "Hello WEB2!",
    };
  },
};
</script>
```

## Annotated version

```vue
<script>
// Export this object so that it becomes the component definition
export default {

  // Defines the component's reactive local data
  data() {
    return {
      helloText: "Hello WEB2!",
    };
  },

};
</script>
```

## What does `export default` mean?

The `.vue` file is treated as an **ECMAScript module**.

```javascript
export default {
  // component options
};
```

This exports the component’s options object as the main value of the file.

Another file can then import it:

```javascript
import Hello from "./components/Hello.vue";
```

Mental model:

```text
Hello.vue
   │
   │ export default
   ▼
Component definition leaves the file
   │
   │ import
   ▼
Another component can use it
```

❗`export default` does not display the component.

It only makes the component available for import elsewhere.

## What is the exported object?

It is the Vue **options object**.

It may contain familiar Vue options such as:

```javascript
export default {
  props: [],
  data() {},
  methods: {},
  computed: {},
  components: {},
};
```

### The script block may only be defined once

The lecture presents the regular `<script>` block as appearing once in an SFC.
## 6. What does the `<style>` block do?

▣ **Style block**

The `<style>` block contains CSS rules associated with the component.

```vue
<style>
.helloBlock {
  color: orange;
  font-size: xx-large;
}
</style>
```

Annotated:

```vue
<style>
/* Select the element whose class is helloBlock */
.helloBlock {

  /* Make its text orange */
  color: orange;

  /* Make its text very large */
  font-size: xx-large;
}
</style>
```

The class is used in the template:

```vue
<p class="helloBlock">
```

Connection:

```text
Template:
class="helloBlock"
       │
       ▼
Style:
.helloBlock { ... }
```

### A style block may appear multiple times

Unlike the regular template and script blocks, an SFC may contain several style blocks.

For example:

```vue
<style>
/* normal CSS */
</style>

<style scoped>
/* component-specific CSS */
</style>
```
## 7. Do SFCs still provide separation of concerns?

At first, an SFC appears to mix HTML, JavaScript and CSS in one file:

```vue
<template>...</template>
<script>...</script>
<style>...</style>
```

This can appear to violate separation of concerns.

However, the lecture asks us to consider how relevant this criticism is.

## Traditional technical separation

A traditional project may separate files by technology:

```text
template.html
component.js
component.css
```

This is separation by **file type**:

```text
all HTML together
all JavaScript together
all CSS together
```

## SFC separation

An SFC groups code by **component responsibility**:

```text
Hello.vue
├── Hello's HTML
├── Hello's JavaScript
└── Hello's CSS
```

This is separation by **feature or component**.

💡 Analogy:

Suppose a company has different documents for every employee.

### Technology-based organization

```text
folder: all employee photos
folder: all employee contracts
folder: all employee addresses
```

### Component-based organization

```text
Alice folder:
- photo
- contract
- address

Bob folder:
- photo
- contract
- address
```

The information types are still separated inside each folder, but everything belonging to one employee is kept together.

❗An SFC does not remove the distinction between HTML, JavaScript and CSS. The `<template>`, `<script>` and `<style>` blocks still make those roles explicit.

→ Result: SFCs prioritize **cohesion around a component** rather than placing all files of one technology together.
## 8. React comparison from the lecture

The lecture provides a React component:

```jsx
class ShoppingList extends React.Component {
  render() {
    return (
      <div className="shopping-list">
        <h1>Shopping List for {this.props.name}</h1>
        <ul>
          <li>Instagram</li>
          <li>WhatsApp</li>
          <li>Oculus</li>
        </ul>
      </div>
    );
  }
}

// Example usage:
<ShoppingList name="Mark" />
```

In this example, markup is written directly inside JavaScript through JSX.

The point of the comparison is that modern component frameworks often group closely related concerns around a component.

Vue still provides visibly separate sections:

```vue
<template>
  ...
</template>

<script>
  ...
</script>

<style>
  ...
</style>
```

React’s example places rendering markup inside the JavaScript component:

```jsx
render() {
  return (
    <div>...</div>
  );
}
```

❗The lecture uses this example to encourage thinking about whether “separation of concerns” must always mean “separate files.”
## 9. Why can the browser not directly run a `.vue` file?

A normal browser understands technologies such as:

```text
HTML
CSS
JavaScript
```

It does not natively understand the special SFC structure:

```vue
<template>...</template>
<script>...</script>
<style>...</style>
```

Therefore, this cannot simply be sent to the browser as-is.

▣ **Build step**

A build step converts source files into a form that the browser can execute.

```text
Hello.vue
    │
    │ build transformation
    ▼
Browser-compatible JavaScript + CSS
```

The lecture compares this with a CSS preprocessor:

```text
Sass source
    │ compiler
    ▼
Normal CSS
```

Similarly:

```text
Vue SFC
    │ Vue build tooling
    ▼
Normal browser resources
```

❗SFCs require tooling. They are not directly interpreted by the browser.
## 10. What is a bundler?

▣ **Bundler**

A bundler is a tool that processes a collection of project artifacts and prepares them for the browser.

Artifacts can include:

```text
.vue files
JavaScript modules
CSS files
.scss files
images
other assets
```

Its core task is:

```text
Transform artifacts
        +
Connect their dependencies
        +
Bundle the result for the browser
```

Mental model:

```text
TodoCard.vue ──┐
App.vue ───────┤
main.js ───────┤
main.css ──────┤
logo.svg ──────┘
       │
       ▼
    Bundler
       │
       ▼
Browser-ready application
```

Bundler examples shown in the lecture include:

- esbuild
- Parcel
- Turbopack
- Webpack
- Rollup

The lecture indicates that Turbopack is a successor to Webpack.
## 11. What tooling is used for Vue?

## Vite

▣ **Vite**

Vite is the officially recommended build tool for Vue.js in the lecture.

It combines:

```text
Native ECMAScript modules
        +
esbuild during development
        +
Rollup for production
```

## Development

During development, Vite aims to provide a fast development environment.

```text
Source file changes
       │
       ▼
Vite development server
       │
       ▼
Browser updates quickly
```

## Production

For production, Vite uses Rollup to create an optimized build.

```text
Application source
       │
       ▼
Rollup production bundle
       │
       ▼
dist directory
```

## `create-vue`

▣ **Project scaffolding**

Project scaffolding means automatically generating the initial files, folders and configuration of a project.

Vue provides:

```text
create-vue
```

It helps generate and configure a Vite-based Vue project.

💡 Analogy:

Instead of manually building a house’s foundation, walls and plumbing, scaffolding gives you a prepared house structure. You then replace and extend the rooms.
## 12. How is an SFC-capable Vue project created?

## Step 1: Install Node.js

Node.js installation also provides:

```text
npm
```

▣ **npm**

npm is the package manager used to install project dependencies and execute project scripts.
## Step 2: Run `create-vue`

```bash
npm init vue@latest
```

This launches an interactive setup process.

Example questions from the lecture:

```text
✔ Project name: … vue-example
✔ Add TypeScript? … No / Yes
✔ Add JSX Support? … No / Yes
✔ Add Vue Router for Single Page Application development? … No / Yes
✔ Add Pinia for state management? … No / Yes
✔ Add Vitest for Unit Testing? … No / Yes
✔ Add an End-to-End Testing Solution? › No
✔ Add ESLint for code quality? … No / Yes
```

The example creates the project in:

```text
vue-example/
```

❗The lecture introduces these choices as project-configuration questions. It does not yet explain all these technologies in detail, so they should not be treated as the main topic of this lecture.
## Step 3: Enter the generated project

Conceptually:

```bash
cd vue-example
```

The slide does not explicitly show this command, but the following dependency installation is performed inside the generated project directory.
## Step 4: Install dependencies

```bash
npm install
```

▣ **Dependency**

A dependency is an external package required by the project.

`npm install` reads the project configuration and installs the necessary packages.

These packages are placed in:

```text
node_modules/
```

→ Result: The generated project is ready to run.
## 13. Vue project structure

The project structure in the lecture looks approximately like this:

```text
vue-example/
│
├── .vscode/
├── node_modules/
├── public/
│   └── favicon.ico
│
├── src/
│   ├── assets/
│   │   ├── base.css
│   │   ├── logo.svg
│   │   └── main.css
│   │
│   ├── components/
│   │   ├── icons/
│   │   ├── HelloWorld.vue
│   │   ├── TheWelcome.vue
│   │   └── WelcomeItem.vue
│   │
│   ├── App.vue
│   └── main.js
│
├── .gitignore
├── index.html
├── package-lock.json
├── package.json
├── README.md
└── vite.config.js
```

Pages 15-19 progressively highlight `public`, `components`, `index.html`, `App.vue` and `main.js`.
## `public/`

The lecture describes this as a directory for static resources.

```text
public/
└── favicon.ico
```

Static resources may include items such as:

```text
images
icons
other files delivered directly
```
## `src/`

This is where the application’s source code is placed.

```text
src/
├── assets/
├── components/
├── App.vue
└── main.js
```
## `src/assets/`

Contains resources used by the source application, such as:

```text
CSS files
SVG images
other imported assets
```

Example:

```text
assets/
├── base.css
├── logo.svg
└── main.css
```
## `src/components/`

The lecture specifically identifies this as the directory for components.

```text
components/
├── HelloWorld.vue
├── TheWelcome.vue
└── WelcomeItem.vue
```

💡 A larger application can place each reusable component in its own `.vue` file:

```text
components/
├── TodoCard.vue
├── NavigationBar.vue
├── UserProfile.vue
└── SubmitButton.vue
```
## `index.html`

The lecture identifies `index.html` as the **entry point of the application**.

A simplified form might contain:

```html
<div id="app"></div>
```

This is the normal HTML page into which Vue mounts the application.

Mental model:

```text
index.html
└── contains mounting location
    <div id="app"></div>
```
## `App.vue`

The lecture identifies `App.vue` as the **root component**.

```text
App.vue
   │
   ├── may display HTML
   ├── may import child components
   └── forms the top of the component tree
```

Example tree:

```text
App.vue
├── TodoCard.vue
├── TodoCard.vue
└── TodoCard.vue
```

▣ **Root component**

The root component is the top-level Vue component from which the rest of the component tree begins.
## `main.js`

The lecture states that `main.js`:

```text
creates the application instance
and mounts the root component
```

A typical generated file is conceptually:

```javascript
import { createApp } from "vue";
import App from "./App.vue";

createApp(App).mount("#app");
```

Annotated:

```javascript
// Import Vue's function for creating an application
import { createApp } from "vue";

// Import App.vue, the root component
import App from "./App.vue";

// Create the application using App as its root component,
// then mount it in the HTML element with id="app"
createApp(App).mount("#app");
```

Connection:

```text
index.html
<div id="app"></div>
       ▲
       │ mount("#app")
       │
main.js
createApp(App)
       │
       │ uses
       ▼
App.vue
root component
```

❗`App.vue` and the Vue application instance are related but not identical:

```text
App.vue              → describes the root component
createApp(App)        → creates the Vue application instance
.mount("#app")        → connects it to the HTML page
```
## `package.json`

Although the slide mainly presents it in the project tree, this file typically contains:

```text
project metadata
dependencies
development dependencies
npm scripts
```

The commands:

```bash
npm run dev
npm run build
```

refer to scripts defined in the project configuration.
## `node_modules/`

Contains packages installed by:

```bash
npm install
```

❗You normally do not manually write application code inside this directory.
## `vite.config.js`

Contains Vite-related project configuration.

The lecture does not go into its configuration details.
## 14. Important commands

## Start the development application

```bash
npm run dev
```

This starts the application for development.

The lecture mentions **hot reload**.

▣ **Hot reload**

When source code changes, the development environment updates the running application quickly without requiring a completely manual rebuild-and-restart cycle.

Mental model:

```text
Edit TodoCard.vue
      │
      ▼
Vite notices change
      │
      ▼
Browser displays updated version
```

→ Result: You can develop and immediately inspect changes.
## Build the application for deployment

```bash
npm run build
```

This creates a production build.

The result is placed in:

```text
dist/
```

Mental model:

```text
Development source files
.vue + .js + .css
        │
        ▼
npm run build
        │
        ▼
dist/
browser-ready production files
```

❗Difference:

```text
npm run dev
→ Run a development server

npm run build
→ Create files intended for deployment
```
## 15. Complete Todo application example with SFCs

The lecture divides the application into two `.vue` files:

```text
src/
├── App.vue
└── components/
    └── TodoCard.vue
```

Mental model:

```text
App.vue
│
│ owns the todo list
│ loops through the todos
│ passes one todo to each child
▼
TodoCard.vue
displays one todo
and manages its own checked state
```
## 16. `components/TodoCard.vue`

```vue
<template>
  <div
    class="todoCard"
    v-on:click="switchCheck"
  >
    <div class="cardTitle">{{ todo.title }}</div>

    <div class="cardText">{{ todo.text }}</div>

    <span
      class="cardCheck"
      v-if="done"
    >
      &check;
    </span>
  </div>
</template>

<script>
export default {
  props: ["todo"],

  data() {
    return {
      done: false,
    };
  },

  methods: {
    switchCheck() {
      this.done = !this.done;
    },
  },
};
</script>

<style>
.todoCard {
  /* CSS rules omitted on the slide */
}
</style>
```

## What does this component do?

It represents **one todo card**.

It receives a todo object from its parent:

```javascript
props: ["todo"]
```

The todo is expected to contain properties such as:

```javascript
{
  title: "Learn JavaScript",
  text: "..."
}
```
## Template explanation

```vue
<div
  class="todoCard"
  v-on:click="switchCheck"
```

- `class="todoCard"` applies CSS styling.
- `v-on:click="switchCheck"` calls the method when the card is clicked.

Equivalent shorter Vue syntax:

```vue
<div class="todoCard" @click="switchCheck">
```
```vue
<div class="cardTitle">{{ todo.title }}</div>
```

Displays the title received through the `todo` prop.

For this object:

```javascript
{
  title: "Learn JavaScript",
  text: "..."
}
```

the output is:

```text
Learn JavaScript
```
```vue
<div class="cardText">{{ todo.text }}</div>
```

Displays the todo’s text.
```vue
<span class="cardCheck" v-if="done">
  &check;
</span>
```

`v-if="done"` means:

```text
done === true  → render the check mark
done === false → do not render the span
```

`&check;` is an HTML entity for:

```text
✓
```
## Local data explanation

```javascript
data() {
  return {
    done: false,
  };
}
```

Every `TodoCard` component instance receives its own `done` state.

Initially:

```text
done = false
```

Therefore, the check mark is not displayed.
## Method explanation

```javascript
methods: {
  switchCheck() {
    this.done = !this.done;
  },
}
```

`!` reverses a Boolean value:

```text
!false → true
!true  → false
```

Thus, every click toggles the state:

```text
First click:
false → true

Second click:
true → false

Third click:
false → true
```

→ Result:

```text
Click card → check mark appears
Click again → check mark disappears
```

❗Each card has its own `done` property because `data()` creates local state for each component instance.
## 17. `App.vue`

```vue
<template>
  <div id="app">
    <h1>Liste der Todos</h1>

    <todo-card
      v-for="todo in todos"
      v-bind:todo="todo"
    ></todo-card>
  </div>
</template>

<script>
// Import TodoCard component
import TodoCard from "./components/TodoCard.vue";

export default {
  components: {
    TodoCard, // register component
  },

  data() {
    return {
      todos: [
        {
          title: "Learn JavaScript",
          text: "...",
        },
        {
          title: "Take a look at Vue",
          text: "...",
        },
      ],
    };
  },
};
</script>
```
## Importing the child component

```javascript
import TodoCard from "./components/TodoCard.vue";
```

Annotated:

```javascript
// Give the imported component the local name TodoCard
// and load it from the indicated file
import TodoCard from "./components/TodoCard.vue";
```

Breakdown:

```text
TodoCard
│
└── local JavaScript name

"./components/TodoCard.vue"
│
└── file location relative to App.vue
```
## Registering the child component

```javascript
components: {
  TodoCard,
}
```

This is shorthand for:

```javascript
components: {
  TodoCard: TodoCard,
}
```

Meaning:

```text
Registration name/key → TodoCard
Component definition  → imported TodoCard
```

After registration, the component can be used in the template as:

```vue
<todo-card></todo-card>
```

Vue maps the PascalCase JavaScript name:

```text
TodoCard
```

to the kebab-case template name:

```text
todo-card
```
## The todo array

```javascript
data() {
  return {
    todos: [
      {
        title: "Learn JavaScript",
        text: "...",
      },
      {
        title: "Take a look at Vue",
        text: "...",
      },
    ],
  };
}
```

`App.vue` owns the list of todo objects.

```text
todos
├── todo object 1
└── todo object 2
```
## Creating one child component per todo

```vue
<todo-card
  v-for="todo in todos"
  v-bind:todo="todo"
></todo-card>
```

### `v-for`

```vue
v-for="todo in todos"
```

means:

```text
For every object in the todos array,
create one TodoCard component instance.
```

With two todos:

```text
TodoCard instance 1
TodoCard instance 2
```

### `v-bind:todo`

```vue
v-bind:todo="todo"
```

means:

```text
Pass the current todo object
to the child's todo prop.
```

Short form:

```vue
:todo="todo"
```

Connection:

```text
App.vue loop variable
todo
 │
 │ v-bind:todo="todo"
 ▼
TodoCard.vue prop
props: ["todo"]
 │
 ▼
{{ todo.title }}
{{ todo.text }}
```
## Overall data flow

```text
App.vue
todos array
│
├── todo 1
│      │ prop
│      ▼
│   TodoCard instance 1
│
└── todo 2
       │ prop
       ▼
    TodoCard instance 2
```

Meanwhile, the checked state stays inside each card:

```text
TodoCard 1 → done: false/true
TodoCard 2 → done: false/true
```

❗The parent supplies the todo information, while each child manages its own checked state.
## 18. How does the complete application start?

```text
index.html
│
│ contains <div id="app">
▼
main.js
│
│ imports App.vue
│ creates application
│ mounts application
▼
App.vue
│
│ imports and registers TodoCard.vue
│ loops through todos
▼
TodoCard.vue instances
```

Typical connection:

```javascript
// main.js
import { createApp } from "vue";
import App from "./App.vue";

createApp(App).mount("#app");
```

```vue
<!-- App.vue -->
<script>
import TodoCard from "./components/TodoCard.vue";

export default {
  components: {
    TodoCard,
  },
};
</script>
```

This demonstrates two different levels:

```text
main.js imports App.vue
→ App becomes the root component

App.vue imports TodoCard.vue
→ TodoCard becomes a child component
```
## 19. Are CSS rules in an SFC automatically private?

No.

Consider:

```vue
<style>
.helloBlock {
  color: orange;
  font-size: xx-large;
}
</style>
```

Technically, the CSS rules from the style block end up in an internal stylesheet of the resulting page.

Conceptually:

```html
<head>
  <style>
    .helloBlock {
      color: orange;
      font-size: xx-large;
    }
  </style>
</head>
```

This selector can match any element on the page with:

```html
class="helloBlock"
```

It is not automatically restricted to the component where it was written.

## Possible problem

Suppose two components use the same class name:

```vue
<!-- Hello.vue -->
<p class="helloBlock">Hello</p>
```

```vue
<!-- OtherComponent.vue -->
<p class="helloBlock">Other text</p>
```

The rule:

```css
.helloBlock {
  color: orange;
}
```

may affect both components.

❗A normal `<style>` block behaves globally.

→ Result: CSS rules can accidentally affect other components.
## 20. What does `<style scoped>` do?

To restrict CSS rules to one component, add the `scoped` attribute:

```vue
<style scoped>
.helloBlock {
  color: orange;
  font-size: xx-large;
}
</style>
```

▣ **Scoped style**

A scoped style contains rules that are transformed so that they affect only the HTML generated by that SFC.

Example:

```vue
<template>
  <p class="helloBlock">
    <strong>{{ helloText }}</strong>
  </p>
</template>

<script>
export default {
  data() {
    return {
      helloText: "Hello WEB2!",
    };
  },
};
</script>

<style scoped>
.helloBlock {
  color: orange;
  font-size: xx-large;
}
</style>
```

## How does Vue implement scoped CSS?

Vue adds a generated attribute to the component’s HTML elements.

Conceptually:

```html
<p class="helloBlock" data-v-abc123>
  <strong data-v-abc123>Hello WEB2!</strong>
</p>
```

It also transforms the CSS selector.

Original:

```css
.helloBlock {
  color: orange;
}
```

Conceptually transformed into:

```css
.helloBlock[data-v-abc123] {
  color: orange;
}
```

Now the rule matches only an element that has:

```text
class="helloBlock"
and
data-v-abc123
```

An element in another component may have a different generated attribute:

```html
<p class="helloBlock" data-v-xyz789>
```

Therefore, it will not match:

```css
.helloBlock[data-v-abc123]
```

## Mental model

Without `scoped`:

```text
.helloBlock
→ style every matching element on the page
```

With `scoped`:

```text
.helloBlock + this component's generated ID
→ style matching elements belonging to this component
```

❗`scoped` does not create an iframe or completely separate document. Vue rewrites attributes and selectors to restrict matching.
## 21. Can an SFC use Sass or another CSS preprocessor?

Yes.

The `<style>` block can use an extended CSS language by specifying the language with the `lang` attribute.

Lecture example:

```vue
<style lang="sass" scoped>
$main-color: orange;

.helloBlock {
  color: $main-color;
  font-size: xx-large;
}
</style>
```

## Explanation

```vue
<style lang="sass" scoped>
```

contains two attributes:

```text
lang="sass"
→ interpret the block as Sass

scoped
→ restrict the resulting CSS to this component
```
```scss
$main-color: orange;
```

Defines a Sass variable.
```scss
.helloBlock {
  color: $main-color;
  font-size: xx-large;
}
```

Uses the variable as the text color.

After processing, the browser receives normal CSS conceptually similar to:

```css
.helloBlock[data-v-some-id] {
  color: orange;
  font-size: xx-large;
}
```

❗The browser itself does not understand the Sass variable. The build tool and configured preprocessor transform it into normal CSS.

The lecture refers to the Vite documentation for the required configuration details.
## 22. Important distinctions for the exam

## What is the difference between a normal Vue component definition and an SFC?

A normal component definition may keep the template inside a JavaScript object:

```javascript
const Component = {
  template: `<p>Hello</p>`,
};
```

An SFC places the component in a `.vue` file:

```vue
<template>
  <p>Hello</p>
</template>

<script>
export default {};
</script>

<style>
p {
  color: orange;
}
</style>
```

→ Result: Better modularization and better development-tool support.
## Why does an SFC require a build step?

Because browsers do not directly understand the `.vue` format.

```text
.vue source
   │
   ▼
Vite/bundler transforms it
   │
   ▼
Browser-compatible resources
```
## What is the role of Vite?

Vite provides the Vue development and build environment.

```text
Development:
native ES modules + esbuild

Production:
Rollup
```

It also works together with Vue project tooling.
## What is the difference between `create-vue` and Vite?

```text
create-vue
→ creates and configures the initial Vue project

Vite
→ runs and builds the generated project
```

Analogy:

```text
create-vue → prepares the workshop
Vite       → operates the workshop
```
## What is the difference between `App.vue`, `main.js` and `index.html`?

```text
index.html
→ browser HTML entry point and mounting location

main.js
→ creates the Vue application instance and mounts it

App.vue
→ root component displayed by the Vue application
```

Flow:

```text
index.html ← main.js mounts App.vue here
```
## What is the difference between importing and registering a component?

Importing loads the component definition into a file:

```javascript
import TodoCard from "./components/TodoCard.vue";
```

Registering makes it available to that component’s template:

```javascript
components: {
  TodoCard,
}
```

Using it creates component instances:

```vue
<todo-card></todo-card>
```

Mental model:

```text
import    → bring the tool into the room
register  → add the tool to the usable tool list
template  → actually use the tool
```
## What is the difference between normal and scoped styles?

```vue
<style>
```

→ CSS may affect matching elements in other components.

```vue
<style scoped>
```

→ Vue transforms the selectors so that the rules target this component.
## What does `lang="sass"` mean?

```vue
<style lang="sass">
```

means that the style block uses Sass syntax and must be transformed into standard CSS during the build process.
## 23. Compact final map

```text
Earlier component approach
│
├── templates stored as strings
├── poor editor support
├── weak modularization
└── CSS outside component definition
        │
        ▼
Single File Component
ComponentName.vue
│
├── <template>
│   └── HTML structure
│
├── <script>
│   └── exported component options object
│
└── <style>
    └── component-related CSS
        │
        ▼
Browser cannot understand .vue
        │
        ▼
Build tool / bundler
        │
        ▼
Vite
├── development with esbuild
├── production with Rollup
└── project setup through create-vue
        │
        ▼
Project structure
├── index.html → HTML entry point
├── main.js    → create and mount application
├── App.vue    → root component
└── components → reusable child SFCs
        │
        ▼
Component composition
App.vue
├── imports TodoCard.vue
├── registers TodoCard
├── loops through todos
└── passes each todo as a prop
        │
        ▼
TodoCard.vue
├── displays title and text
├── stores local done state
└── toggles check mark on click
        │
        ▼
SFC styling
├── <style> → potentially global
├── <style scoped> → restricted to component
└── <style lang="sass"> → preprocessor syntax
```

## Core takeaway

❗A Vue Single File Component is not merely “HTML, JavaScript and CSS placed in one file.”

It is a **module representing one coherent UI component**, which can be imported, registered, composed with other components and transformed by Vite into browser-compatible code.
