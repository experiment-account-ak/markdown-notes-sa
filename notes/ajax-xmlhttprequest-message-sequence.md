# AJAX Lecture Summary

## When ajax is there what the use of xmlhttprequest?

```text
7/3/2026, 9:49:51 AM
```

## Thinking

```text
● Clarifying AJAX and XMLHttpRequest with citation
I need to clarify the difference between the AJAX concept and the XMLHttpRequest API. The user didn't
explicitly ask formally, but in a previous conversation, they preferred a formal approach. I'll cite the relevant
parts from the uploaded file and provide accurate references by searching for key lines. I may need to check
the tool's guidelines for more precision on citations.

✓ Thought for 16s
```

## What is the relationship between AJAX and XMLHttpRequest?

**AJAX is the idea; `XMLHttpRequest` is one tool used to implement that idea.**

AJAX means:

```text
Communicate with the server asynchronously and update part of the page without reloading the whole
page.
```

But AJAX itself does not send an HTTP request. JavaScript needs a browser API to perform the actual communication. One such API is `XMLHttpRequest`, or XHR. `F-01-javascript-ajax_en.pdf`

## Simple analogy

| Concept | Analogy |
|---|---|
| AJAX | The idea of ordering food without leaving your table |
| `XMLHttpRequest` | The waiter who carries your order to the kitchen |
| Server | The kitchen |
| Response | The food brought back |
| DOM update | Placing the food on your table |

Saying “use AJAX” means deciding to communicate in the background.

`XMLHttpRequest` performs the actual request:

```js
const xhr = new XMLHttpRequest();

xhr.open("GET", "message.txt");

xhr.onload = function () {
  document.getElementById("output").textContent =
    xhr.responseText;
};

xhr.send();
```

Here:

```js
xhr.open("GET", "message.txt");
```

prepares the request.

```js
xhr.send();
```

actually sends it.

```js
xhr.onload = function () { ... };
```

handles the result when it arrives.

```js
document.getElementById("output").textContent =
  xhr.responseText;
```

updates part of the page without reloading it.

## AJAX does not require `XMLHttpRequest`

`XMLHttpRequest` is the classic AJAX API. AJAX can also be implemented using:

```js
fetch("message.txt")
```

or libraries such as Axios and jQuery. The lecture therefore distinguishes between the **AJAX concept** and the different APIs available for asynchronous communication. `F-01-javascript-ajax_en.pdf`

```text
AJAX
├── XMLHttpRequest  ← classic API
├── Fetch API       ← newer API
├── Axios
└── jQuery
```

So the key sentence is:

> **AJAX describes what we want to achieve; `XMLHttpRequest` describes how JavaScript can achieve it.**

```text
7/3/2026, 9:49:50 AM
```

## What is msg.txt here?

## And what are the sequence of events?

```text
7/3/2026, 9:51:27 AM
```

## What is `message.txt` / `msg.txt`?

It is simply a small text file stored on the web server.

Example content:

```text
Hello from the server!
```

Suppose your project contains:

```text
project/
├── index.html
└── message.txt
```

Then this line:

```js
xhr.open("GET", "message.txt");
```

means:

```text
Prepare an HTTP GET request asking the server for the file message.txt.
```

`message.txt` is only used to make the example simple. In a real application, the URL might point to an API:

```js
xhr.open("GET", "/api/todos");
```

The response could then be JSON instead of plain text. AJAX supports formats such as text, JSON and XML. `F-01-javascript-ajax_en.pdf`

## Sequence of events

Consider this code:

```js
document.getElementById("loadButton").onclick = function () {
  const xhr = new XMLHttpRequest();

  xhr.open("GET", "message.txt");

  xhr.onload = function () {
    document.getElementById("output").textContent =
      xhr.responseText;
  };

  xhr.send();
};
```

## Before the user clicks

The browser loads `index.html`.

JavaScript then registers this function as the button’s click handler:

```js
document.getElementById("loadButton").onclick = function () {
```

The function does not run yet. The browser waits for a click.

## After the user clicks

### 1. A click event occurs

The user clicks the button.

The browser calls the registered event handler.

```text
User clicks button
↓
Browser calls onclick function
```

### 2. An XHR object is created

```js
const xhr = new XMLHttpRequest();
```

This creates an object responsible for managing the HTTP request and response.

### 3. The request is prepared

```js
xhr.open("GET", "message.txt");
```

This specifies:

```text
HTTP method: GET
requested resource: message.txt
```

No request has been sent yet.

### 4. The response handler is registered

```js
xhr.onload = function () {
```

This tells the browser:

```text
When the complete response arrives, call this function.
```

The function is registered now but runs later.

### 5. The request is sent

```js
xhr.send();
```

The browser sends an HTTP request to the server:

```http
GET /message.txt
```

### 6. The browser does not wait in a blocked state

While the server processes the request, the JavaScript function finishes.

The page remains usable.

```text
Request travelling to server
+
User can still use the page
```

This is the **asynchronous** part.

### 7. The server returns the file

The server finds `message.txt` and sends its contents back:

```text
Hello from the server!
```

### 8. The browser produces the load event

After the complete response arrives, the browser calls:

```js
xhr.onload = function () {
```

### 9. JavaScript reads the response

The returned text is stored in:

```js
xhr.responseText
```

Its value is:

```text
Hello from the server!
```

### 10. JavaScript updates the DOM

```js
document.getElementById("output").textContent =
  xhr.responseText;
```

The paragraph changes from:

```text
The message will appear here.
```

to:

```text
Hello from the server!
```

Only the paragraph changes. The whole page does not reload.

## Complete sequence

```text
1. Browser loads index.html
2. JavaScript registers the button's onclick handler
3. User clicks the button
4. Browser calls the onclick handler
5. JavaScript creates XMLHttpRequest
6. open() prepares GET /message.txt
7. onload handler is registered
8. send() sends the HTTP request
9. Server receives the request
10. Server returns the text file
11. Browser receives the complete response
12. Browser triggers the load event
13. onload function executes
14. JavaScript reads xhr.responseText
15. JavaScript updates the paragraph in the DOM
```

The central flow is:

```text
Click event
↓
Create and send request
↓
Continue without blocking
↓
Response arrives later
↓
load event
↓
Update the DOM
```

```text
7/3/2026, 9:51:34 AM
```
