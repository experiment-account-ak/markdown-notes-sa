# F-01 - AJAX

This lecture explains how web applications move from **whole-page request-response interactions** toward **small, asynchronous updates inside the current page**. `F-01-javascript-ajax_en.pdf`

## Mental model: replacing a whole page versus editing one part

Imagine an application as a document displayed on your screen.

### Classic multi-page application

Every time something changes, you throw away the document and request a newly printed version from the server.

### Application using AJAX

You keep the current document. JavaScript asks the server for only the required data and edits the relevant part of the document.

The technical mapping is:

| Mental-model element | Technical meaning |
|---|---|
| Document currently displayed | Current HTML page |
| Editable document structure | DOM |
| User pressing or typing something | Browser event |
| Person reacting to the event | JavaScript event handler |
| Background message to the server | AJAX request |
| Information returned by server | JSON, XML, text or binary data |
| Editing one part of the document | DOM manipulation |

The complete idea to remember is:

> **Event → JavaScript handler → asynchronous HTTP request → server data → DOM update**

# Lecture map

The lecture follows this progression:

1. How a classic **multi-page application**, or MPA, works.
2. Why the classic request-response cycle is unsuitable for highly interactive features.
3. How AJAX solves this problem.
4. How the DOM and browser events support AJAX.
5. Which APIs can perform asynchronous communication.
6. How `XMLHttpRequest` is used for GET and POST requests.
7. What AJAX improves and what limitations remain.

# 1. What is a classic multi-page application ❓

The Web is fundamentally based on a **request-response cycle**:

1. The browser sends an HTTP request.
2. The server processes it.
3. The server sends a response.
4. The browser renders the returned page.

A traditional web application that works mainly by loading new HTML pages is called a **multi-page application**, or **MPA**.

## MPA basic principle

> **IMAGE PLACEHOLDER:** MPA basic request-response cycle

The sequence diagram on page 6 shows:

1. The user requests `index.html`.
2. The browser sends an HTTP request to the web server.
3. The server returns `index.html`.
4. The browser renders the page.
5. The user waits during this process.
6. When the user navigates to `page.html`, the whole process happens again.

The dashed server-to-browser arrows represent the **responses**, even though the diagram labels them with `request : index.html` and `request : page.html`.

## Important properties of an MPA

### Full-page reload

A user action normally causes communication with the server and then a reload of the website.

### Synchronous user experience

The user must wait between sending the request and receiving and rendering the response.

Here, “synchronous” describes the experience:

> The current interaction cannot meaningfully continue until the new page has arrived.

### Thin client

The browser is mainly responsible for **HTML rendering**.

Most work remains on the server:

- presentation logic;
- HTML generation;
- state management;
- business logic;
- authentication;
- authorization;
- database and service access;
- URL navigation and routing.

The distribution diagram on pages 8-9 therefore describes the browser as a **thin client**. It displays what the server provides but performs relatively little application logic itself.


# 2. Why is the classic MPA cycle problematic for interactive components ❓

## What would happen if autocomplete were implemented as a classic MPA interaction❓

Consider a search suggestion list that should update after every typed letter.

In a completely traditional MPA:

1. The user types `s`.
2. The browser submits a request.
3. A new page is returned and rendered.
4. The user types `i`.
5. Another full-page request and reload happens.
6. The process repeats for every character.

This creates three problems.

### Poor user experience

The page would continually reload, forcing the user to wait after every character.

### Strong dependency on network performance

Bandwidth and network latency would heavily influence how responsive the component feels.

- **Bandwidth** concerns how much data can be transferred.
- **Latency** concerns how long a request takes to travel and return.

### Client-side state must be reconstructed

The application must preserve the letters that the user has already entered across multiple requests.

For example, after sending `sing`, the newly generated page must still display `sing` in the input field.

# 3. What did web applications need from desktop applications❓

Desktop applications normally provide:

- suggestion lists;
- maps and other rich interface elements;
- immediate reactions to input;
- updates without replacing the entire interface.

To provide a similar experience in a browser, two capabilities are required:

1. **Exchange data with the server without blocking the interface.**
2. **Update the interface locally in the browser.**

AJAX provides this combination.

# 4. What is AJAX❓

**AJAX** stands for:

> **Asynchronous JavaScript and XML**

AJAX enables communication with a server **without reloading the complete website**.

The server can expose the required data through an interface such as a REST API.

## AJAX is a concept, not one individual technology

AJAX combines several client-side technologies:

1. **DOM**  
   A manipulable representation of the current HTML document.

2. **JavaScript**  
   Used for event handling, asynchronous communication and DOM manipulation.

3. **A data format**  
   Examples include JSON, XML, text and binary data.

The name includes XML for historical reasons, but AJAX is **not restricted to XML**. The lecture examples use JSON.


# 5. How does an AJAX interaction work❓

> **IMAGE PLACEHOLDER:** AJAX request, JSON response and DOM update

The diagrams on pages 14-16 build the process gradually.

## Initial page load

The initial page is still loaded normally:

1. The user requests `index.html`.
2. The browser sends an HTTP request.
3. The server sends the HTML page.
4. The browser renders it.

## Later AJAX interaction

Suppose the user types inside a search field:

1. Typing produces an `onkeyup` event.
2. JavaScript handles the event.
3. The browser sends an HTTP request in the background.
4. The server returns data, such as JSON.
5. JavaScript modifies the DOM.
6. Only the relevant part of the page changes.

## What does “asynchronous” mean here❓

It does **not** mean that the response arrives instantly.

It means:

> The browser interface is not blocked while the request is being processed.

The user can continue viewing or interacting with the page while the request is in progress.

# 6. What is the DOM❓

The **Document Object Model**, or **DOM**, is the data structure in which the browser manages an HTML document.

It also defines an API that JavaScript can use to:

- find elements;
- read their values;
- change their text;
- add or remove elements;
- change attributes;
- register event handlers.

## Code example: HTML document represented by the DOM

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>My Title</title>
</head>
<body>
  <h1>Document Object Model</h1>
  <section>
    <h2>Description</h2>
    <p>
      The DOM is a tree structure.
    </p>
  </section>
</body>
</html>
```

## DOM tree

> **IMAGE PLACEHOLDER:** HTML document represented as a DOM tree

The DOM is a tree because elements are nested inside other elements:

```text
document
└── html
    ├── head
    │   └── title
    │       └── "My Title"
    └── body
        ├── h1
        │   └── "Document Object Model"
        └── section
            ├── h2
            │   └── "Description"
            └── p
                └── "The DOM is a tree structure."
```

Important relationships include:

- `html` is the parent of `head` and `body`.
- `head` and `body` are children of `html`.
- `h2` and `p` are children of `section`.
- The visible words are text nodes inside the elements.

AJAX uses this structure because JavaScript can update a single branch without requesting and rendering a completely new page.

# 7. What are browser events and event handlers❓

An **event** represents something that happens in the browser.

Examples from the lecture include:

| Event | Meaning |
|---|---|
| `blur` | An element loses focus |
| `change` | The value of an input element changes |
| `click` | A mouse or pointing-device button is pressed and released |
| `keydown` | A keyboard key is pressed |
| `load` | A document or resource has finished loading |
| `unload` | A document is being exited |
| `mouseover` | The pointer moves over an element |
| `mouseout` | The pointer moves away from an element |

## Event target

The object or HTML element where the event occurs is the **event target**.

For example:

```html
<button id="btn">Load</button>
```

When the button is clicked:

- event type: `click`;
- event target: the button.

## Event handler

An **event handler** is a JavaScript function registered for a particular event.

The browser calls that function when the event occurs.

```javascript
document.getElementById("btn").onclick = () => {
  console.log("Button clicked");
};
```

Meaning:

1. `document.getElementById("btn")` finds the button in the DOM.
2. `.onclick` specifies the event.
3. `() => { ... }` is the function that will be called.
4. The browser invokes that function after the click.

This is an example of **Inversion of Control**:

> Your code does not continuously ask whether the button was clicked.  
> The browser calls your function when the click occurs.

# 8. Which technologies can perform asynchronous communication❓

The lecture presents two native browser APIs:

- `XMLHttpRequest`;
- Fetch API.

It also names libraries that offer related functionality:

- jQuery;
- Axios.

The lecture concentrates on `XMLHttpRequest`.

The Fetch API is identified as the newer alternative, but the PDF does not contain a Fetch code example; it only refers to a separate video.

# 9. What is `XMLHttpRequest`❓

`XMLHttpRequest`, commonly abbreviated as **XHR**, is the classic browser API for transferring data between a browser and a server.

Despite its name:

> It is not limited to XML.

It can work with JSON, text, HTML/XML documents and other data.

An XHR interaction uses an object created in JavaScript:

```javascript
let xhr = new XMLHttpRequest();
```

# 10. Important `XMLHttpRequest` functions

## `open()`

Initializes the HTTP request.

```javascript
xhr.open("GET", "http://localhost:8080/todo/api");
```

Important parameters include:

- HTTP method, such as `GET` or `POST`;
- URL to which the request should be sent.

`open()` prepares the request. It does not send it yet.

## `send()`

Sends the HTTP request.

For a GET request without a request body:

```javascript
xhr.send();
```

For a POST request with data:

```javascript
xhr.send(JSON.stringify(todo));
```

# 11. Important `XMLHttpRequest` properties

| Property | Purpose |
|---|---|
| `responseType` | Configures the expected format of the response |
| `status` | Contains the HTTP response status code |
| `response` | Contains the response data |

Example:

```javascript
xhr.responseType = "json";
```

This tells the browser to interpret the response as JSON.

After the response arrives, the converted value is available through:

```javascript
xhr.response
```

# 12. Important `XMLHttpRequest` events

After a request is sent, the XHR object produces events describing what happened.

| Event | Meaning |
|---|---|
| `load` | The HTTP response has been completely transmitted |
| `error` | A transmission error occurred |
| `timeout` | The configured maximum transmission time was exceeded |

An event handler can be registered for these events:

```javascript
xhr.onload = () => {
  console.log("Response received");
};
```

The function is not called immediately. The browser calls it after the response has arrived.

# 13. Code example 1: GET request with XHR

This example loads a list of todos from the server and inserts them into the current page.

## `todoList.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>ToDo-Liste</title>
  <meta charset="utf-8">
</head>
<body>
  <ul id="list"></ul>

  <button id="btn">Load</button>

  <script src="todoList.js"></script>
</body>
</html>
```

## What does the HTML do❓

```html
<ul id="list"></ul>
```

Creates an initially empty unordered list. JavaScript will later insert `<li>` elements into it.

```html
<button id="btn">Load</button>
```

Creates the button that starts the AJAX request.

```html
<script src="todoList.js"></script>
```

Loads the JavaScript file containing the event handler and AJAX logic.

## `todoList.js`

```javascript
document.getElementById("btn").onclick = () => {
  // 1. Create XHR instance
  let xhr = new XMLHttpRequest();

  // 2. Initialize HTTP request
  // REST service that returns a list of todos
  xhr.open("GET", "http://localhost:8080/todo/api");

  // 3. Set desired response data format
  xhr.responseType = "json";

  // 4. Send request with an empty body
  xhr.send();

  // 5. Register callback for the "load" event
  // The browser calls this when the response is complete
  xhr.onload = () => {
    let list = document.getElementById("list");

    list.innerHTML = "";

    for (let todo of xhr.response) {
      list.innerHTML +=
        `<li>${todo.title} (${todo.id})</li>`;
    }
  };
};
```

## Step-by-step execution

### 1. Register the click handler

```javascript
document.getElementById("btn").onclick = () => {
```

JavaScript finds the button and registers a function for its click event.

Nothing is requested until the user clicks the button.

### 2. Create an XHR object

```javascript
let xhr = new XMLHttpRequest();
```

This object represents and manages the asynchronous request.

### 3. Configure a GET request

```javascript
xhr.open("GET", "http://localhost:8080/todo/api");
```

The browser will send a GET request to the todo API.

A GET request normally asks the server to return data.

### 4. Expect JSON

```javascript
xhr.responseType = "json";
```

The server response should be interpreted as JSON.

Suppose the response represents:

```json
[
  {
    "id": 1,
    "title": "Study AJAX"
  },
  {
    "id": 2,
    "title": "Complete exercise"
  }
]
```

Then `xhr.response` behaves like a JavaScript array of objects.

### 5. Send the request

```javascript
xhr.send();
```

The request is sent without a body.

### 6. React when the response arrives

```javascript
xhr.onload = () => {
```

The browser calls this function after the complete response has arrived.

### 7. Find and clear the list

```javascript
let list = document.getElementById("list");
list.innerHTML = "";
```

JavaScript retrieves the `<ul>` element and removes its previous contents.

### 8. Process every todo

```javascript
for (let todo of xhr.response) {
```

The loop visits every object in the returned JSON array.

### 9. Generate list items

```javascript
list.innerHTML +=
  `<li>${todo.title} (${todo.id})</li>`;
```

The backtick string is a **template literal**.

For a todo with title `Study AJAX` and ID `1`, it generates:

```html
<li>Study AJAX (1)</li>
```

The important result is:

> The browser does not replace the whole page. It changes only the contents of the `<ul>` element.

# 14. Code example 2: POST request with XHR

This example reads a title from an input field and sends a new todo to the server.

## `todoForm.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>ToDo-Form</title>
  <meta charset="utf-8">
</head>
<body>
  <input id="title">

  <button id="add-btn">
    Add
  </button>

  <script src="todoForm.js"></script>
</body>
</html>
```

## What does the HTML do?

```html
<input id="title">
```

Creates the input field from which JavaScript reads the todo title.

```html
<button id="add-btn">
  Add
</button>
```

Creates the button that starts the POST request.

## `todoForm.js`

```javascript
document.getElementById("add-btn").onclick = () => {
  // Create todo object
  let todo = {
    title: document.getElementById("title").value
  };

  // 1. Create XHR instance
  let xhr = new XMLHttpRequest();

  // 2. Initialize HTTP request
  xhr.open("POST", "http://localhost:8080/todo/api");

  // 3. Set request data format
  xhr.setRequestHeader(
    "Content-Type",
    "application/json"
  );

  // 4. Set desired response format
  xhr.responseType = "json";

  // 5. Convert the object to JSON and send it
  xhr.send(JSON.stringify(todo));

  // 6. Callback for the "load" event
  xhr.onload = () => console.log("Todo created!");
};
```

## Step-by-step execution

### 1. Register the click handler

```javascript
document.getElementById("add-btn").onclick = () => {
```

The function runs when the user clicks **Add**.

### 2. Read the input value

```javascript
let todo = {
  title: document.getElementById("title").value
};
```

Suppose the user entered:

```text
Study AJAX
```

The resulting JavaScript object is:

```javascript
{
  title: "Study AJAX"
}
```

### 3. Create and configure an XHR object

```javascript
let xhr = new XMLHttpRequest();
xhr.open("POST", "http://localhost:8080/todo/api");
```

A POST request normally sends data to the server, for example to create a new resource.

### 4. Describe the request body

```javascript
xhr.setRequestHeader(
  "Content-Type",
  "application/json"
);
```

This HTTP header tells the server:

> The data contained in this request body is JSON.

### 5. Describe the expected response

```javascript
xhr.responseType = "json";
```

This concerns the data coming **back from the server**.

The distinction is important:

| Code | Describes |
|---|---|
| `Content-Type: application/json` | Format of the request body sent to the server |
| `responseType = "json"` | Format expected in the server response |

### 6. Convert and send the object

```javascript
xhr.send(JSON.stringify(todo));
```

`JSON.stringify()` converts the JavaScript object:

```javascript
{
  title: "Study AJAX"
}
```

into JSON text:

```json
{"title":"Study AJAX"}
```

That JSON text becomes the HTTP request body.

### 7. React to completion

```javascript
xhr.onload = () => console.log("Todo created!");
```

After the response has been received, the browser prints:

```text
Todo created!
```

to the developer console.

# 15. GET and POST example comparison

| Aspect | GET example | POST example |
|---|---|---|
| Purpose | Read todos | Create a todo |
| HTTP method | `GET` | `POST` |
| Request body | Empty | JSON todo object |
| Main input | Button click | Input value and button click |
| Response format | JSON | JSON |
| UI effect | Todo list inserted into DOM | Message written to console |

Both examples follow the same general structure:

```text
Find an HTML element
        ↓
Register an event handler
        ↓
Create XMLHttpRequest
        ↓
Configure the request
        ↓
Send the request
        ↓
Wait without blocking the page
        ↓
Handle the load event
        ↓
Process the response or update the DOM
```

# 16. What are the advantages of AJAX❓

## Better user experience

The application can respond more like a desktop application.

For example:

- autocomplete suggestions can appear while typing;
- a list can update without reloading the surrounding page;
- map information can be loaded dynamically.

## Better perceived performance

The browser updates only the relevant part instead of rebuilding the entire page.

## Lower network load

The server can return only the required data, such as JSON, rather than repeatedly transferring a complete HTML page with its surrounding layout.

# 17. How does AJAX change the distribution of tasks❓

> **IMAGE PLACEHOLDER:** Comparison of MPA and MPA with AJAX

## Traditional MPA

The client mainly performs:

- HTML rendering.

The server performs:

- presentation logic;
- HTML generation;
- state management;
- business logic;
- authentication;
- authorization.

## MPA with AJAX

The client now additionally performs parts of:

- presentation logic;
- HTML generation;
- DOM manipulation.

For example, the GET code generates this HTML in the browser:

```javascript
`<li>${todo.title} (${todo.id})</li>`
```

However, the server may still generate other HTML pages and perform presentation logic.

This causes **fragmentation**:

> Some presentation logic and HTML generation exist on the server, while other presentation logic and HTML generation exist in the browser.

# 18. What limitations remain in an MPA with AJAX❓

AJAX improves individual interactions, but it does not automatically turn an MPA into a completely different application architecture.

The lecture highlights three remaining limitations.

## Presentation logic is split

Some interface construction happens on the server, while some happens in JavaScript on the client.

## Page navigation may still reload the application

Moving from one complete page to another still uses the traditional request-response cycle.

AJAX prevents reloads for selected interactions, not necessarily for all navigation.

## Application state remains mainly on the server

The actual application state is still primarily managed by the server.

Therefore:

> An MPA enhanced with AJAX is still an MPA.

The lecture has not yet introduced single-page application architecture; AJAX is the intermediate step that makes an MPA more interactive.

# Exam-ready comparison

| Characteristic | Classic MPA | MPA with AJAX |
|---|---|---|
| Initial page load | Full HTML page | Full HTML page |
| Small interaction | Usually new page request | Background data request |
| Browser blocked from the user's perspective | Yes, during page transition | No, during AJAX communication |
| Typical server response | Complete HTML | JSON, XML, text or other data |
| UI update | Whole page rendered again | Selected DOM elements changed |
| Client responsibility | Mostly rendering | Rendering plus some presentation logic |
| Server responsibility | Most application work | Still most application work |
| Navigation between complete pages | Reload | Usually still reload |
| Main advantage | Simple request-response model | More responsive interaction |


# Core definitions!

**MPA:**  
A web application in which navigation and user actions commonly load separate HTML pages through request-response cycles.

**AJAX:**  
A concept combining JavaScript, asynchronous server communication, data formats and DOM manipulation to update a page without fully reloading it.

**DOM:**  
The browser's tree-structured representation of an HTML document and the API used to manipulate that representation.

**Event target:**  
The element or object where an event occurs.

**Event handler:**  
A JavaScript function that the browser calls when a registered event occurs.

**XHR:**  
The classic browser API for asynchronous HTTP communication.

**Asynchronous:**  
The request is processed while the page remains usable; the response is handled later by a callback or event handler.

# Walkthrough

Suppose the user presses the **Load** button:

1. The browser produces a `click` event.
2. The button is the event target.
3. The registered JavaScript event handler runs.
4. It creates an `XMLHttpRequest`.
5. It configures a GET request.
6. It sends the request.
7. The browser remains usable.
8. The server returns JSON.
9. The XHR object produces a `load` event.
10. The registered `onload` handler runs.
11. JavaScript reads `xhr.response`.
12. JavaScript generates `<li>` elements.
13. The DOM is updated.
14. The user sees the todo list without a page reload.

That single sequence connects almost every important concept in the lecture.