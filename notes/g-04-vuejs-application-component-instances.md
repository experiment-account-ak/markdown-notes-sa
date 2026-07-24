## Lecture Summary Request

# Vue.js 04 - Application and Component Instances

## Mental model: a Vue application is a small reactive machine

Think of the lecture as explaining four connected parts:

```text
HTML template
     ↕
Root component / component instance
 ┌───────────────┐
 │ data          │ → stores reactive state
 │ methods       │ → reacts to events and changes state
 │ computed      │ → derives values from other state
 └───────────────┘
     ↕
Application instance
     ↓
Mounts everything into the HTML page
```

The central idea is:

> **The component instance connects the data, presentation logic, and HTML template.**

The lecture uses the **Options API**, where the component is described using options such as `data`, `methods`, and `computed`. `G-04-vuejs-application-component-instances_en.pdf`
## 1. How does MVVM map to Vue.js?

The diagram on page 2 maps Vue.js concepts to the earlier MVVM architecture.

```text
MVVM concept          Vue.js implementation

View                   HTML template
Model                  Reactive data returned by data()
ViewModel              Component instance
Binding                Vue's reactive binding system
```

## View

▣ **View:** The visible user interface.

In Vue.js, the view is represented by the HTML template:

```html
<div id="app">
  <h1>Hallo {{text}}</h1>
  <input v-on:input="changeText">
</div>
```

The template:

- displays data using `{{text}}`
- listens for input events using `v-on:input`
- connects the user interface to the component
## Model

▣ **Model:** The data used by the user interface.

In Vue.js, the model is normally represented by the object returned from `data()`:

```javascript
data() {
  return {
    text: "WEB2"
  };
}
```

Here, `text` is application data.
## ViewModel

▣ **ViewModel:** The part that connects the view with the model and contains presentation logic.

In Vue.js, the **component instance** takes on the role of the ViewModel.

It provides:

- data to the template
- methods that react to user actions
- computed values
- automatic synchronization between data and the displayed interface

→ Result: When the component's data changes, Vue updates the connected parts of the HTML automatically.
## 2. What is a root component?

▣ **Root component:** The top-level component from which a Vue application begins.

A root component is defined as a normal JavaScript object:

```javascript
const MyApp = {
  data() {
    // ...
  },

  methods: {
    // ...
  },

  computed: {
    // ...
  }
};
```

The object contains different configuration properties called **options**.

That is why this style is called the **Options API**.

## Common component options

| Option | Purpose |
|---|---|
| `data` | Stores reactive data for the view |
| `methods` | Stores functions containing presentation logic |
| `computed` | Stores values calculated from other reactive data |

❗ The more general term is **component instance**. The root component is simply the component at the top of the application.

A larger application can contain many component instances, but one of them is the root component.
## Options API and Composition API

The lecture focuses on the **Options API**.

▣ **Options API:** Component code is organized according to option categories such as `data`, `methods`, and `computed`.

Vue also provides the **Composition API**.

▣ **Composition API:** An alternative way of organizing component code, intended to improve modularization and reuse.

❗ The lecture only mentions the Composition API. The remaining examples continue with the Options API, so its details are outside this lecture's scope.
## 3. What does the `data` property do?

▣ **`data`:** A function that returns an object containing the data used by the view.

Example:

```javascript
data() {
  return {
    text: ""
  };
}
```

## Syntax explanation

```javascript
data()
```

Declares a method named `data`.

```javascript
return {
  text: ""
};
```

Returns an object with a property named `text`.

The initial value of `text` is an empty string.
## Why must `data` return an object?

The returned object contains the component's state:

```javascript
{
  text: ""
}
```

Vue makes the properties of this object available to the component and its template.

Therefore, this can be used directly in HTML:

```html
<h1>Hello {{text}}</h1>
```

You do not write:

```html
<h1>Hello {{data.text}}</h1>
```

Instead, the property is exposed directly as:

```html
{{text}}
```
## Reactive data

▣ **Reactive property:** A property monitored by Vue so that dependent parts of the view can be updated automatically when its value changes.

Suppose the initial data is:

```javascript
data() {
  return {
    text: "World"
  };
}
```

And the template contains:

```html
<h1>Hello {{text}}</h1>
```

The browser displays:

```text
Hello World
```

Later, if the property changes:

```javascript
this.text = "Anna";
```

Vue notices the change.

→ Result:

```text
Hello Anna
```

❗ The programmer does not manually locate and rewrite the `<h1>` element. Vue's binding system performs the necessary update.
## 4. What does the `methods` property do?

▣ **`methods`:** An object containing functions that implement presentation logic.

Example:

```javascript
methods: {
  changeText(event) {
    this.text = event.target.value;
  }
}
```

Methods often react to things happening in the user interface, such as:

- typing into an input
- clicking a button
- submitting a form
## Syntax explanation

```javascript
methods: {
```

Defines an object containing the component's methods.

```javascript
changeText(event) {
```

Defines a function named `changeText`.

The `event` parameter contains information about the browser event that caused the function to run.

```javascript
this.text = event.target.value;
```

This line:

1. reads the current value of the input element
2. assigns that value to the component's reactive `text` property
## 5. Why is `this.text` used inside methods?

Inside a component method, properties from `data()` are accessed through `this`.

```javascript
this.text
```

Here:

- `this` refers to the component instance
- `.text` refers to the reactive `text` property belonging to that component

The lecture states that Vue binds `this` to the component instance.

❗ Inside the template, write:

```html
{{text}}
```

❗ Inside a method, write:

```javascript
this.text
```

Comparison:

```text
Template                  Component method

{{text}}                  this.text
```
## Common beginner mistake

Incorrect:

```javascript
changeText(event) {
  text = event.target.value;
}
```

This does not explicitly access the component property.

Correct:

```javascript
changeText(event) {
  this.text = event.target.value;
}
```

→ Result: Vue changes the reactive `text` property belonging to the component.
## 6. Complete simple example

The lecture provides two files:

```text
hello.html
hello.js
```
## `hello.html`

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
    <input v-on:input="changeText" />
  </div>

  <script
    type="module"
    src="hello.js">
  </script>
</body>
</html>
```

## Line-by-line explanation

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

Sets the browser-tab title.

```html
<meta charset="utf-8" />
```

Uses UTF-8 character encoding.

```html
<div id="app">
```

Creates the HTML element into which the Vue application will be mounted.

The ID is important because the JavaScript later uses:

```javascript
.mount("#app")
```

```html
<h1>Hello {{text}}</h1>
```

Displays the reactive `text` property through interpolation.

```html
<input v-on:input="changeText" />
```

Creates an input field.

The directive means:

```text
When an input event occurs,
call the changeText method.
```

```html
<script type="module" src="hello.js"></script>
```

Loads the JavaScript file as an ES module.
## `hello.js`

```javascript
// Source for import shortened
import { createApp } from "...";

const HelloApp = {
  data() {
    return {
      text: ""
    };
  },

  methods: {
    changeText(event) {
      this.text = event.target.value;
    }
  }
};

createApp(HelloApp).mount("#app");
```

## Line-by-line explanation

```javascript
import { createApp } from "...";
```

Imports Vue's `createApp` function.

The actual import source is shortened in the lecture.
```javascript
const HelloApp = {
```

Creates an object describing the root component.
```javascript
data() {
  return {
    text: ""
  };
}
```

Creates a reactive property named `text`, initially containing an empty string.
```javascript
methods: {
  changeText(event) {
    this.text = event.target.value;
  }
}
```

Defines the `changeText` method.

Whenever the user types, the input's current value is copied into `this.text`.
```javascript
createApp(HelloApp).mount("#app");
```

This performs two connected steps:

```javascript
createApp(HelloApp)
```

Creates a Vue application using `HelloApp` as its root component.

```javascript
.mount("#app")
```

Connects the application to the first HTML element matching the CSS selector `#app`.
## Complete execution flow

```text
1. Browser loads hello.html
2. Browser loads hello.js
3. createApp(HelloApp) creates the Vue application
4. mount("#app") connects it to <div id="app">
5. User types into the input
6. The browser emits an input event
7. v-on:input calls changeText(event)
8. event.target.value contains the typed text
9. this.text is updated
10. Vue detects the reactive change
11. {{text}} is re-rendered
```

💡 Suppose the user types:

```text
Peter
```

The method executes:

```javascript
this.text = "Peter";
```

→ Result:

```html
<h1>Hello Peter</h1>
```
## 7. What does the `computed` property do?

▣ **`computed`:** An object containing functions that define values derived from other reactive properties.

Example:

```javascript
computed: {
  fullName() {
    return `${this.firstname} ${this.lastname}`;
  }
}
```

The value of `fullName` depends on:

```javascript
this.firstname
```

and:

```javascript
this.lastname
```
## Mental model

```text
firstname ──┐
            ├──> fullName
lastname ───┘
```

For example:

```text
firstname = "Ada"
lastname  = "Lovelace"
```

The computed property produces:

```text
fullName = "Ada Lovelace"
```
## Why is it called a computed property rather than a method?

Although it is defined using function syntax:

```javascript
fullName() {
  return `${this.firstname} ${this.lastname}`;
}
```

it is used in the template like a normal property:

```html
{{fullName}}
```

It is not called with parentheses:

```html
{{fullName()}}
```

❗ In the template, a computed property is accessed as a value, not as a function call.
## 8. Computed-property caching

Vue caches computed properties.

▣ **Caching:** Reusing a previously calculated result until one of its dependencies changes.

For:

```javascript
computed: {
  fullName() {
    return `${this.firstname} ${this.lastname}`;
  }
}
```

Vue observes that `fullName` depends on:

- `firstname`
- `lastname`

Vue recalculates `fullName` only when one or both of these properties change.

```text
firstname changes → recompute fullName
lastname changes  → recompute fullName
unrelated data changes → reuse cached fullName
```

❗ This is one of the main differences between a computed property and a normal method.
## 9. Complete `computed` example

## `computed.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Example: Computed</title>
  <meta charset="utf-8" />
</head>
<body>
  <div id="app">
    <input v-model="firstname" />
    <input v-model="lastname" />

    <!-- The computed property is
         accessed like a normal property -->
    Full Name: {{fullName}}
  </div>

  <script
    type="module"
    src="computed.js">
  </script>
</body>
</html>
```
## Important template parts

```html
<input v-model="firstname" />
```

Connects the first input to the reactive `firstname` property.

```html
<input v-model="lastname" />
```

Connects the second input to the reactive `lastname` property.

▣ **`v-model`:** A directive that binds an input value to a reactive property.

When the user types in the first input:

```text
input value ↔ firstname
```

When the user types in the second input:

```text
input value ↔ lastname
```
```html
Full Name: {{fullName}}
```

Displays the computed property.

Notice that there are no parentheses:

```html
{{fullName}}
```
## `computed.js`

```javascript
// Source for import shortened
import { createApp } from "...";

const app = {
  data() {
    return {
      firstname: "",
      lastname: ""
    };
  },

  computed: {
    // Caching: value of "fullName"
    // is only recalculated
    // if "firstname" and/or
    // "lastname" change
    fullName() {
      return `${this.firstname} ${this.lastname}`;
    }
  }
};

createApp(app).mount("#app");
```
## Syntax explanation

```javascript
const app = {
```

Creates the root component object.

```javascript
data() {
  return {
    firstname: "",
    lastname: ""
  };
}
```

Defines two reactive properties.

```javascript
computed: {
```

Begins the object containing computed properties.

```javascript
fullName() {
```

Defines a computed property named `fullName`.

```javascript
return `${this.firstname} ${this.lastname}`;
```

Uses a JavaScript template literal to combine the two values.

The syntax:

```javascript
`${value1} ${value2}`
```

inserts the values into a string with a space between them.

💡 With:

```javascript
this.firstname = "Ada";
this.lastname = "Lovelace";
```

the expression returns:

```text
Ada Lovelace
```
## Complete execution flow

```text
1. Vue mounts the component on #app
2. firstname and lastname begin as empty strings
3. User types into the first input
4. v-model updates firstname
5. User types into the second input
6. v-model updates lastname
7. Vue sees that fullName depends on these properties
8. Vue recalculates fullName
9. {{fullName}} is updated in the HTML
```

💡 User enters:

```text
First input: Grace
Second input: Hopper
```

→ Result:

```text
Full Name: Grace Hopper
```
## 10. Methods versus computed properties

This distinction is likely relevant for an exam.

## What is the difference between `methods` and `computed`?

| `methods` | `computed` |
|---|---|
| Represents an action or presentation logic | Represents a derived value |
| Often triggered by an event | Evaluated from reactive dependencies |
| Called as a function | Accessed as a property in templates |
| Example: `changeText(event)` | Example: `fullName` |
| Not described here as cached | Cached until dependencies change |

### Method

```javascript
methods: {
  changeText(event) {
    this.text = event.target.value;
  }
}
```

Used from a template through an event directive:

```html
<input v-on:input="changeText" />
```

### Computed property

```javascript
computed: {
  fullName() {
    return `${this.firstname} ${this.lastname}`;
  }
}
```

Used from the template as:

```html
{{fullName}}
```

💡 A useful decision rule:

```text
Does something happen?       → method
Is a value derived?          → computed
```
## 11. What is an application instance?

▣ **Application instance:** An object representing an entire Vue application.

It is created using:

```javascript
createApp(rootComponent)
```

Example:

```javascript
const vueApplication = createApp(HelloApp);
```

Here:

- `HelloApp` is the root component
- `vueApplication` is the application instance

The application instance is responsible for starting and mounting the component hierarchy.
## 12. What does `mount()` do?

▣ **Mounting:** Connecting a Vue application and its root component to an existing DOM element.

Example:

```javascript
createApp(HelloApp).mount("#app");
```

The argument:

```javascript
"#app"
```

is a CSS selector.

It means:

```text
Find an element whose id is app.
```

Corresponding HTML:

```html
<div id="app">
```

Vue mounts the root component on the **first element** in the document that matches the selector.

❗ The selector in JavaScript and the HTML element must match.

Correct:

```html
<div id="app"></div>
```

```javascript
createApp(HelloApp).mount("#app");
```

Incorrect combination:

```html
<div id="application"></div>
```

```javascript
createApp(HelloApp).mount("#app");
```

In the incorrect example, Vue cannot find the intended mounting element.
## 13. Root component versus application instance

These two concepts are closely related but not identical.

## Root component

```javascript
const HelloApp = {
  data() {
    return {
      text: ""
    };
  }
};
```

This describes:

- reactive data
- methods
- computed properties
- the behavior of the root component

## Application instance

```javascript
createApp(HelloApp)
```

This creates the Vue application around the root component.

## Mounting

```javascript
.mount("#app")
```

This attaches the application to the page.

The complete relationship is:

```text
Root component definition
        ↓
createApp(rootComponent)
        ↓
Application instance
        ↓
mount("#app")
        ↓
Connected HTML interface
```
## 14. Full lecture map

```text
Vue application
│
├── Application instance
│     ├── created with createApp(rootComponent)
│     └── connected to the DOM using mount(selector)
│
└── Root component / component instance
      │
      ├── data()
      │     ├── returns the model object
      │     ├── properties are available in templates
      │     └── properties are reactive
      │
      ├── methods
      │     ├── contains presentation-logic functions
      │     ├── functions can be called from templates
      │     └── data is accessed using this.property
      │
      └── computed
            ├── contains derived properties
            ├── accessed without () in templates
            └── cached until dependencies change
```
## 15. Most important points to remember

❗ A Vue component instance acts as the **ViewModel** in MVVM.

❗ `data()` returns the component's reactive model.

❗ Properties returned by `data()` can be accessed directly inside templates.

❗ When reactive data changes, Vue automatically updates the connected view.

❗ Inside component methods, data properties are accessed through `this`, for example:

```javascript
this.text
```

❗ `methods` represents actions or presentation logic.

❗ `computed` represents values derived from other reactive properties.

❗ Computed properties are used without parentheses in templates:

```html
{{fullName}}
```

❗ Computed properties are cached and recalculated only when their dependencies change.

❗ `createApp(rootComponent)` creates the application instance.

❗ `.mount("#app")` connects the root component to the first DOM element matching the CSS selector.
## 16. Possible exam questions

## What role does a component instance perform in Vue's MVVM architecture?

A component instance acts as the ViewModel. It connects reactive model data with the HTML view and provides presentation logic through methods and computed properties.
## Why are properties returned from `data()` called reactive?

Vue monitors these properties. When one changes, Vue automatically updates the parts of the template that depend on it.
## Why must `this.text` be used inside a method?

Vue binds `this` to the component instance. Therefore, `this.text` accesses the `text` property belonging to that component.
## How is a computed property used in a Vue template?

Although defined using function syntax, it is accessed like a normal property:

```html
{{fullName}}
```

not:

```html
{{fullName()}}
```
## What advantage does a computed property have?

Vue caches its result and only recalculates it when one of its reactive dependencies changes.
## What is the difference between the root component and application instance?

The root component describes data and component behavior. The application instance is created with `createApp(rootComponent)` and is responsible for mounting the component to the DOM.
## What does the following statement do?

```javascript
createApp(HelloApp).mount("#app");
```

It creates a Vue application whose root component is `HelloApp` and mounts that application onto the first HTML element matching the CSS selector `#app`.

## Difference Between Root Component and Application Instance

## First, separate the two ideas

```javascript
const HelloApp = {
  data() {
    return {
      text: ""
    };
  },

  methods: {
    changeText(event) {
      this.text = event.target.value;
    }
  }
};

createApp(HelloApp).mount("#app");
```

There are two different things here:

```text
HelloApp
```

and:

```text
createApp(HelloApp)
```

They are related, but they are not the same.
## 1. Root component

▣ **Root component:** The main component definition at the top of the Vue component tree.

In the example:

```javascript
const HelloApp = {
  data() {
    return {
      text: ""
    };
  },

  methods: {
    changeText(event) {
      this.text = event.target.value;
    }
  }
};
```

`HelloApp` is the root component.

It describes:

- what data exists
- what methods exist
- how the component behaves
- what the template can access

You can think of it as the **instructions for the main component**.

It says:

```text
This component has a text property.
This component has a changeText method.
```

But by itself, it is only a component definition. It has not yet been connected to the webpage.
## 2. Application instance

▣ **Application instance:** The actual Vue application object created by Vue.

It is created here:

```javascript
createApp(HelloApp)
```

Vue receives the root component and creates an application around it.

That application instance is then mounted:

```javascript
createApp(HelloApp).mount("#app");
```

The application instance is responsible for:

- starting the Vue application
- using `HelloApp` as the root component
- mounting the component into the HTML page
- managing the application's component tree
## Analogy: architectural plan and construction company

Imagine building a house.

## Root component = architectural plan

The architectural plan describes:

- how many rooms there are
- where the doors are
- where the kitchen is
- how the house should behave and be organized

In Vue:

```javascript
const HelloApp = {
  data() {
    return {
      text: ""
    };
  },

  methods: {
    changeText(event) {
      this.text = event.target.value;
    }
  }
};
```

This is the plan.

It describes what the component should contain.

But a plan alone does not produce a real house.
## Application instance = construction company

The construction company takes the plan and builds the house at a specific location.

In Vue:

```javascript
createApp(HelloApp).mount("#app");
```

This means:

```text
Take the HelloApp plan,
create a Vue application from it,
and place it inside the HTML element #app.
```

So:

```text
Root component = what should be built
Application instance = the Vue system that builds and runs it
mount("#app") = where it should be placed
```
## Complete analogy

```text
Architectural plan      → Root component
Construction company    → Application instance
Building location       → DOM element #app
Finished house          → Running Vue interface
```
## Example step by step

## HTML

```html
<div id="app">
  <h1>Hello {{text}}</h1>
  <input v-on:input="changeText">
</div>
```

At first, the browser only sees HTML containing Vue syntax such as:

```html
{{text}}
```

The browser itself does not understand what `text` means.
## Root component

```javascript
const HelloApp = {
  data() {
    return {
      text: ""
    };
  },

  methods: {
    changeText(event) {
      this.text = event.target.value;
    }
  }
};
```

This explains what `text` and `changeText` mean.

```text
text       → reactive data
changeText → method
```

But Vue has not started yet.
## Create application instance

```javascript
const app = createApp(HelloApp);
```

Now Vue creates an application instance using `HelloApp` as its root component.

You can separate the original one-line statement like this:

```javascript
const app = createApp(HelloApp);
app.mount("#app");
```

This is equivalent to:

```javascript
createApp(HelloApp).mount("#app");
```

Here:

```javascript
HelloApp
```

is the root component definition.

And:

```javascript
app
```

is the application instance.
## A very direct comparison

```javascript
const HelloApp = {
  data() {
    return {
      text: ""
    };
  }
};
```

This is like saying:

> “My main component should contain a reactive property called `text`.”

Then:

```javascript
const app = createApp(HelloApp);
```

means:

> “Vue, create an application using this component as the main component.”

Then:

```javascript
app.mount("#app");
```

means:

> “Place and activate that Vue application inside the HTML element with `id="app"`.”
## Another analogy: recipe and restaurant

## Root component = recipe

A recipe describes:

- ingredients
- preparation steps
- expected result

But a recipe is not a working restaurant.

```javascript
const HelloApp = {
  data() {
    return {
      text: ""
    };
  }
};
```

This describes the component.
## Application instance = restaurant operation

The restaurant uses the recipe, prepares the food, and serves it at a location.

```javascript
const app = createApp(HelloApp);
app.mount("#app");
```

So:

```text
Recipe               → Root component
Restaurant operation → Application instance
Serving table        → #app
```
## Why is it called the root component?

A Vue application can contain multiple components.

For example:

```text
HelloApp
├── HeaderComponent
├── FormComponent
└── FooterComponent
```

`HelloApp` is at the top, so it is the root.

It is similar to the root of a tree:

```text
          HelloApp
          /      \
      Header     Form
                   \
                  Button
```

The application instance manages this entire tree.

❗ The root component is one component at the top.

❗ The application instance represents and manages the whole Vue application.
## Small example with child components

```javascript
const HeaderComponent = {
  template: `<h1>My Website</h1>`
};

const HelloApp = {
  components: {
    HeaderComponent
  },

  data() {
    return {
      text: "World"
    };
  }
};

const app = createApp(HelloApp);
app.mount("#app");
```

Possible HTML:

```html
<div id="app">
  <header-component></header-component>
  <p>Hello {{text}}</p>
</div>
```

Here:

```text
HelloApp          → root component
HeaderComponent   → child component
app               → application instance
#app              → mounting location
```

The application instance manages both the root component and everything below it.
## The most useful mental model

```text
Root component
= the main component's definition

Application instance
= the running Vue application created from that definition
```

Or even more simply:

```text
Root component = blueprint
Application instance = running system
```
## Final mapping of the code

```javascript
const HelloApp = {
```

→ Defines the root component.

```javascript
const app = createApp(HelloApp);
```

→ Creates an application instance from the root component.

```javascript
app.mount("#app");
```

→ Connects the application to the HTML page.

→ Result:

```text
Component definition
        ↓
Vue application created
        ↓
Mounted into the page
        ↓
Reactive interface starts working
```

## Can the Root Component, Application Instance, and Mount Element Have Different Names?

Yes. They can have completely different variable names.

```javascript
const RootComponent = {
  data() {
    return {
      text: ""
    };
  }
};

const vueApplication = createApp(RootComponent);

vueApplication.mount("#app");
```

Here:

```text
RootComponent   → root component
vueApplication  → application instance
```

The names are chosen by the programmer.

For example, this is also valid:

```javascript
const MainPage = {
  data() {
    return {
      text: ""
    };
  }
};

const myApp = createApp(MainPage);

myApp.mount("#app");
```

Here:

```text
MainPage → root component
myApp    → application instance
```

The important part is not the names. The important part is the role:

```javascript
createApp(MainPage)
```

`MainPage` is passed into `createApp`, so it becomes the root component.

```javascript
const myApp = createApp(MainPage);
```

The returned object is stored in `myApp`, so `myApp` is the application instance.

❗ The HTML ID can also have a different name, as long as it matches the selector:

```html
<div id="vue-root"></div>
```

```javascript
myApp.mount("#vue-root");
```

So all three names may differ:

```text
Root component variable:      MainPage
Application instance variable: myApp
HTML mounting element ID:      vue-root
```
