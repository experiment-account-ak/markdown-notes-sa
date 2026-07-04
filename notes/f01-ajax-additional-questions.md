# F01 AJAX — Additional Questions

[Source chat](https://chatgpt.com/g/g-p-6a295be0712c8191a00e1149bb7206ea/c/6a465343-9ef0-83eb-b90d-63fa20b79044)

## 1. What is `index.html`?

`index.html` is the **main web page file** that the browser opens first.

In our small example, the project could look like this:

```text
project/
├── index.html
└── message.txt
```

`index.html` contains the visible page:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>XHR Example</title>
</head>
<body>

  <button id="loadButton">Load message</button>

  <p id="output">The message will appear here.</p>

  <script>
    document.getElementById("loadButton").onclick = function () {
      const xhr = new XMLHttpRequest();

      xhr.open("GET", "message.txt");

      xhr.onload = function () {
        document.getElementById("output").textContent =
          xhr.responseText;
      };

      xhr.send();
    };
  </script>

</body>
</html>
```

So:

- `index.html` defines the page structure.
- It contains the button and paragraph.
- It contains the JavaScript that sends the request.
- `message.txt` contains the data returned by the server.

When the browser opens:

```text
http://localhost/index.html
```

it displays the page.

Then, after the user clicks the button, JavaScript sends another request for:

```text
http://localhost/message.txt
```

The relationship is:

```text
index.html
   ├── displays the interface
   ├── contains the JavaScript
   └── requests message.txt later
```

The name `index.html` is conventional. Web servers often treat it as the default page of a folder, so opening:

```text
http://localhost/
```

may automatically load:

```text
http://localhost/index.html
```

## 2. What does “thin client” mean in an MPA, and how does the flow work?

## What does **thin client** mean?

In an MPA, **thin client** means:

> The browser/client does only a small amount of application work.  
> The server does most of the real work and sends back a ready-made HTML page.

In the lecture, the MPA client is described as a **thin client**, while the main work happens on the server: creating/delivering HTML pages, URL navigation/routing, and access to business logic. User actions also cause server communication and page reloads. `F-01-javascript-ajax_en.pdf`

So the browser is mostly a **display machine**.

It mainly does:

```text
Receive HTML → render/display HTML → wait for next user action
```

The server mainly does:

```text
Understand request → choose page → run logic → get data → create HTML → send response
```

## Simple example

Suppose the user clicks:

```text
/todo/list
```

In a classic MPA:

1. Browser sends request to server.
2. Server decides which page this URL means.
3. Server may call business logic.
4. Server may access database.
5. Server creates the HTML page.
6. Server sends the full HTML page back.
7. Browser reloads and displays it.

The browser does **not** decide how to build the todo list.  
It just receives the final HTML and renders it.

## Flowchart: thin client in an MPA

```text
User clicks link/button
        ↓
Browser sends HTTP request
        ↓
Server receives request
        ↓
Server handles routing
        ↓
Server calls business logic
        ↓
Server accesses data if needed
        ↓
Server creates full HTML page
        ↓
Server sends HTML response
        ↓
Browser reloads page
        ↓
Browser renders HTML
```

## PlantUML flow diagram

> **IMAGE PLACEHOLDER:** Thin client in an MPA flow diagram

## Why is it called “thin”?

Because the client’s responsibility is **small/thin**:

| Browser / thin client | Server |
|---|---|
| Sends request | Understands request |
| Waits for response | Decides what to do |
| Receives HTML | Runs business logic |
| Renders HTML | Gets data |
| Displays page | Creates full HTML |

A thin client is not “bad.” It just means the browser is not doing much application logic. In classic MPAs, the intelligence of the application mostly lives on the server.

## 3. How should the MPA distribution scenario diagram be understood?

> **IMAGE PLACEHOLDER:** MPA distribution scenario diagram

This diagram explains **where the different parts of a web application live: on the client/browser or on the server**.

The lecture uses it to show that a classic **MPA** is a **thin-client architecture**: the browser does little work, and the server does most of the work. In the next slide, the lecture explicitly says: “The client is a thin client” and the main work happens on the server, such as creating/delivering HTML pages, routing URLs, and accessing business logic. `F-01-javascript-ajax_en.pdf`

## 1. First understand the colors

```text
ORANGE area = Client side
BLUE area   = Server side
```

So the top half is the **client**, meaning mainly the browser.

The bottom half is the **server**, meaning the backend application plus database/service access.

## 2. The three layers in the boxes

The diagram uses three common application layers.

### Presentation Layer

This is the **user interface layer**.

Examples:

```text
HTML pages
CSS
JavaScript
forms
buttons
layout
rendering
```

In an MPA, the presentation layer is split:

- the **server** creates or selects HTML pages;
- the **browser** renders/displays those pages.

That is why you see a **Presentation Layer box on both client and server**.

### Business Logic Layer

This contains the actual rules of the application.

Example:

```text
Can this user create a todo?
Is the entered data valid?
How should a booking be calculated?
What happens when an order is submitted?
```

In this diagram, the **Business Logic Layer is on the server**.

The browser does not decide the important rules.

### Persistence Layer

This is about storing and loading data.

Examples:

```text
database access
saving todos
loading users
reading orders
writing bookings
```

In this diagram, the **Persistence Layer is also on the server**.

The browser does not directly talk to the database.

## 3. Why is only the left side highlighted?

The diagram shows many possible ways to distribute an application between client and server.

But for classic MPAs, the lecture highlights the first scenario:

```text
Thin Client: Distributed GUI
```

This means:

> The graphical user interface is distributed between browser and server, but the browser is still thin.

The browser has only a small part of the presentation layer: mainly rendering the HTML.

The server has:

```text
Presentation Layer
Business Logic Layer
Persistence Layer
```

So the server is doing most of the application work.

## 4. What does “Distributed GUI” mean here?

“GUI” means **Graphical User Interface**.

“Distributed GUI” means the UI work is split across two places.

```text
Server:
  creates/selects the HTML page

Browser:
  displays/renders the HTML page
```

For example, when you open:

```text
/todo/list
```

the server may create this HTML:

```html
<ul>
  <li>Buy milk</li>
  <li>Study AJAX</li>
</ul>
```

Then the browser receives this HTML and renders it visually.

So the UI is not only on the browser. Part of the UI work is already done by the server.


## 5. What happens in an MPA request?

The flow is:

```text
User clicks a link
        ↓
Browser sends request to server
        ↓
Server handles URL/routing
        ↓
Server calls business logic
        ↓
Server loads data using persistence layer
        ↓
Server creates/selects HTML
        ↓
Server sends full HTML page
        ↓
Browser renders the page
```

This matches the MPA property from the lecture: user actions cause client-server communication and page reloads. `F-01-javascript-ajax_en.pdf`


## 6. PlantUML flowchart

> **IMAGE PLACEHOLDER:** MPA thin-client distribution flowchart


## 7. The key meaning of the diagram

The diagram is saying:

> In a classic MPA, the browser is not the “brain” of the application.  
> It mainly displays pages.  
> The server contains the important application logic and data access.

So:

| Part | In classic MPA |
|---|---|
| Browser/client | mostly renders HTML |
| Server | creates pages, routes URLs, runs business logic |
| Database access | server-side |
| Result | full-page reload after many user actions |

The most important exam sentence:

> A classic MPA is a **thin-client architecture** because the client mainly renders HTML, while presentation generation, business logic, state management, and persistence access are mostly handled on the server.
