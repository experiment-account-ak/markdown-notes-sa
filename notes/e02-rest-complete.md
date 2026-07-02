# Lecture E02: REST — Complete Lecture Notes

[Source chat](https://chatgpt.com/g/g-p-6a295be0712c8191a00e1149bb7206ea/c/6a3301a8-9c04-83ed-bff8-89998dc1c7cc)

## Quick Navigation

- [Central Mental Model](#central-mental-model)
- [1. What Is REST and Why Was It Developed?](#1-what-is-rest-and-why-was-it-developed)
- [2. How Ordinary WWW Communication Works](#2-how-ordinary-www-communication-works)
- [3. The Basic Idea of REST](#3-the-basic-idea-of-rest)
- [4. The Five REST Principles](#4-the-five-rest-principles)
- [5. Unique Identification Through URIs](#5-unique-identification-through-uris)
- [6. Uniform and Restricted Interface](#6-uniform-and-restricted-interface)
- [7. Safe and Idempotent HTTP Methods](#7-safe-and-idempotent-http-methods)
- [8. Resource Versus Representation](#8-resource-versus-representation)
- [9. HATEOAS and Hypermedia Links](#9-hateoas-and-hypermedia-links)
- [10. Statelessness](#10-statelessness)
- [11. All Five Principles in One Example](#11-all-five-principles-in-one-example)
- [12. Complete Technical Mapping](#12-complete-technical-mapping)
- [13. Website Versus Web Service](#13-website-versus-web-service)
- [14. What Exactly Is a Web Service?](#14-what-exactly-is-a-web-service)
- [15. How Websites and Web Services Work Together](#15-how-websites-and-web-services-work-together)
- [16. REST Versus HTTP](#16-rest-versus-http)
- [17. What Does It Mean That REST Abstracts Away from HTTP?](#17-what-does-it-mean-that-rest-abstracts-away-from-http)
- [18. Why Is REST Needed If HTTP Already Exists?](#18-why-is-rest-needed-if-http-already-exists)
- [19. Final Exam-Ready Questions](#19-final-exam-ready-questions)
- [20. Final Memory Maps](#20-final-memory-maps)

# Central Mental Model

This lecture explains how to design a web service according to the same basic principles that made the World Wide Web successful.

A useful mental model is:

```text
A REST service is like a city containing identifiable places.
```

| REST concept | City analogy | Technical meaning | Todo API example |
|---|---|---|---|
| Resource | A place, such as a library | An entity or piece of information exposed by the server | A todo, a todo collection, or comments |
| URI | The address of the place | A unique identifier for a resource | `/todos/42` |
| HTTP method | A standard action performed at the place | The operation requested by the client | `GET /todos/42` |
| Representation | A map, photo, or written description | A concrete data format describing the resource | JSON, XML, or HTML |
| Hypermedia link | A road sign showing where to go next | A link to another resource or possible action | `/todos/42/comments` |
| Statelessness | The traveller remembers the journey, not the city | Each request contains the information needed to process it | URI, method, authentication, headers, and input |

The lecture begins with ordinary Web communication and then introduces five REST principles.

==★ **REST identifies resources with URIs, manipulates them through standard operations, exchanges representations, connects resources through links, and keeps application state on the client.**==

# 1. What Is REST and Why Was It Developed?

REST stands for:

```text
Representational State Transfer
```

REST is an **architectural style** for developing web services.

It was first described by Roy Fielding in his PhD thesis.

An architectural style is a collection of principles for structuring a system.

REST is therefore:

- not a programming language;
- not a library;
- not a framework;
- not the same thing as HTTP;
- not a concrete implementation.

REST was inspired by an observation about the Web:

- The Web grew enormously in a relatively short time.
- Despite its size, applications and services could still be delivered quickly and reliably.
- The same general principles could therefore be useful for software-accessible services.

The idea is:

```text
If the principles of the Web work well for websites,
services should be designed according to those principles too.
```

REST abstracts away from specific technologies such as HTTP.

In theory, REST principles could be implemented using another communication technology.

In practice, REST services are predominantly implemented with HTTP because HTTP already provides:

- URIs;
- methods;
- request and response messages;
- headers;
- status codes;
- content types;
- links.

==★ **REST is the design style; HTTP is the technology most commonly used to implement that style.**==

# 2. How Ordinary WWW Communication Works

The lecture introduces communication between:

- a client, such as a browser;
- the Internet;
- a server running a web server;
- resources stored or provided by that server.

## Resources on the Web

The Web contains different kinds of resources:

- HTML pages;
- images;
- videos;
- documents;
- API data.

A resource is a thing that a client can access.

Each resource normally has an address.

## URI and URL

For a beginner, the important distinction is:

- A **URI** identifies a resource.
- A **URL** is the common kind of URI used to locate a resource on the Web.

Examples:

```text
/todos
/todos/42
/todos/42/comments
```

A resource may also contain links to other resources.

The linked resource can even be located on another server.

## Operations on resources

Clients perform operations on resources through HTTP methods such as:

```http
GET
POST
PUT
DELETE
HEAD
OPTIONS
```

The available operations are deliberately restricted to the methods provided by HTTP.

A client can also request a particular form of a resource by using headers:

```http
Accept: text/html
```

```http
Accept: application/pdf
```

```http
Accept: application/json
```

The overall flow is:

```text
Client
  │
  ├── URI + HTTP operation
  ▼
Server resource

Server
  │
  ├── Representation of the resource
  ▼
Client
```

The lecture diagrams progressively show:

1. the resource on the server;
2. the browser navigating between resources;
3. the HTTP connection used to perform operations;
4. the representation returned to the client.

# 3. The Basic Idea of REST

REST applies ordinary Web principles to services.

Services and their data should be addressed like normal Web resources.

Instead of designing an operation-oriented address such as:

```text
/getTodo?id=42
```

the service treats the todo itself as a resource:

```text
/todos/42
```

The requested action is communicated separately using an HTTP method:

```http
GET /todos/42
```

This gives two separate pieces of information:

```text
/todos/42 → Which resource?
GET       → What should happen to it?
```

This separation is fundamental to REST.

A less REST-like design puts the operation in the URI:

```text
/deleteTodo/42
```

A REST-style design uses the resource URI and a standard method:

```http
DELETE /todos/42
```

==★ **URI = which resource; HTTP method = which operation.**==

# 4. The Five REST Principles

The lecture presents five principles:

1. Unique identification through URIs
2. Uniform and restricted interface
3. Representation diversity
4. Linking resources through hypermedia
5. Statelessness

A short memory map is:

```text
URI          → every resource has an address
Methods      → standard, restricted operations
Formats      → one resource can have several representations
Links        → the server shows possible next destinations
Stateless    → every request makes sense on its own
```

# 5. Unique Identification Through URIs

Every resource should be reachable through a unique URI.

The lecture uses a todo service.

```text
/todos
```

Identifies the collection of all todos.

```text
/todos/42
```

Identifies the todo with ID `42`.

```text
/todos/42/comments
```

Identifies the comments belonging to todo `42`.

```text
/todos/42/comments/7
```

Could identify comment `7` belonging to todo `42`.

## URI pattern

A URI normally describes a resource or a collection of resources.

It usually uses nouns:

```text
/todos
/todos/42
/todos/42/comments
```

The HTTP method describes the action:

```http
GET /todos/42
PUT /todos/42
DELETE /todos/42
```

The same URI can therefore support multiple operations.

## Resource does not necessarily mean database row

A resource is the conceptual thing exposed by the API.

It can represent:

- one database entity;
- a collection;
- a calculated result;
- a nested relationship;
- an abstract server-side capability.

Examples:

```text
/todos
```

represents a collection resource.

```text
/todos/42
```

represents one specific todo resource.

# 6. Uniform and Restricted Interface

A REST service does not invent a completely new operation for every use case.

Instead, it uses a uniform set of operations.

When REST is implemented with HTTP, these operations are the HTTP methods.

## What does “uniform” mean?

Uniform means that the same method has the same general meaning across the service.

```http
GET /todos/42
```

means retrieve todo `42`.

```http
GET /todos/99
```

means retrieve todo `99`.

The meaning of `GET` remains consistent.

## What does “restricted” mean?

Restricted means that developers do not invent unlimited methods such as:

```text
FIND-TODO
COMPLETE-TODO
SHOW-COMMENTS
REMOVE-TODO
```

Instead, they use the methods provided by HTTP and organize the API around resources.

This produces a predictable interface.

A developer who understands the meaning of `GET`, `POST`, `PUT`, and `DELETE` can understand many REST-style APIs more quickly.

# 7. Safe and Idempotent HTTP Methods

The HTTP specification distinguishes two important properties:

- safe;
- idempotent.

## What does safe mean?

A method is safe when executing it does not change the state of the requested resource.

Example:

```http
GET /todos/42
```

This should retrieve todo `42`.

It should not modify or delete the todo.

Technical side effects such as logging the request are still allowed.

The important point is that the requested resource state is not changed.

## What does idempotent mean?

A method is idempotent when sending the same request several times has the same overall side effect as sending it once.

Example:

```http
DELETE /todos/42
```

After the first successful request, todo `42` no longer exists.

Sending the same delete request again does not make it “more deleted.”

The final server state remains the same.

Idempotent does **not** mean every response must be identical.

The first request may return success, while a later request may report that the resource no longer exists.

The relevant point is the resulting side effect.

## HTTP method overview

| Method | Meaning in the lecture | Safe? | Idempotent? |
|---|---|---:|---:|
| `GET` | Requests a representation of a resource | Yes | Yes |
| `PUT` | Changes a resource or creates it if it does not exist | No | Yes |
| `DELETE` | Deletes a resource | No | Yes |
| `POST` | Adds something to an existing resource or collection | No | No |
| `HEAD` | Like GET, but returns only status and headers | Yes | Yes |
| `OPTIONS` | Requests information about supported operations | Yes | Yes |

## Why is POST not idempotent?

Suppose this request adds a new comment:

```http
POST /todos/42/comments
```

Sending it once may create comment `1`.

Sending the identical request again may create comment `2`.

Repeating the request can create additional side effects.

## Why is PUT idempotent?

Suppose this request sets the complete state of todo `42`:

```http
PUT /todos/42
Content-Type: application/json
```

```json
{
  "title": "Learn JavaScript"
}
```

Sending it several times continues setting the title to the same value.

The resulting resource state is the same as after sending it once.

==★ **Safe concerns whether the resource changes. Idempotent concerns whether repetition creates additional side effects.**==

# 8. Resource Versus Representation

This is one of the most important distinctions in the lecture.

## Resource

A resource is the conceptual thing managed or exposed by the server.

Example:

```text
Todo number 12
```

## Representation

A representation is a concrete description of the resource sent between client and server.

The same todo could be represented as JSON:

```json
{
  "id": 12,
  "title": "Learn JavaScript",
  "text": "I should not keep putting it off."
}
```

or XML:

```xml
<todo>
  <id>12</id>
  <title>Learn JavaScript</title>
  <text>I should not keep putting it off.</text>
</todo>
```

or HTML:

```html
<h1>Learn JavaScript</h1>
<p>Todo ID: 12</p>
```

The resource remains the same, but its representation changes.

```text
Resource       = Todo 12
Representation = JSON, XML, or HTML describing Todo 12
```

The client interacts with the resource through representations.

The desired representation can be requested through HTTP headers.

Example:

```http
GET /todos/12
Accept: application/json
```

The name “Representational State Transfer” refers to transferring representations of resource state between client and server.

==★ **The resource is the thing; the representation is a description of that thing.**==

# 9. HATEOAS and Hypermedia Links

REST says that resources should be linked using hypermedia.

This principle is called:

```text
HATEOAS
Hypermedia as the Engine of Application State
```

The server does not only return data.

It can also return links describing what the client can do next.

Example:

```json
{
  "id": 12,
  "title": "Learn JavaScript",
  "links": [
    {
      "rel": "self",
      "href": "http://example.com/todos/12"
    },
    {
      "rel": "show-comments",
      "href": "http://example.com/todos/12/comments"
    }
  ]
}
```

The first link:

```json
{
  "rel": "self",
  "href": "http://example.com/todos/12"
}
```

points to the current todo resource.

The second link:

```json
{
  "rel": "show-comments",
  "href": "http://example.com/todos/12/comments"
}
```

tells the client where the comments are available.

Here:

- `rel` describes the meaning of the link;
- `href` gives the URI.

## Road-sign mental model

Imagine that you arrive at a library and see signs:

```text
Reading room →
Information desk →
Café →
```

You do not need to memorize every destination beforehand.

The signs tell you where you can go next.

In the same way, a REST response can guide the client by including related resources and possible actions.

==★ **HATEOAS means the server helps the client discover the next available resources or actions through links.**==

# 10. Statelessness

The lecture distinguishes two kinds of state:

- resource state;
- application state.

## Resource state

Resource state is managed by the server.

For a todo, this might include:

```text
ID: 12
Title: Learn JavaScript
Completed: false
```

This information belongs to the resource and is stored on the server.

## Application state

Application state is managed by the client.

Examples:

- which resource the client is currently viewing;
- which link it followed;
- which step of a workflow it has reached;
- what action it wants to perform next;
- which page is currently visible;
- previous navigation steps.

| Type of state | Stored by | Example |
|---|---|---|
| Todo title, ID, and completion status | Server | Resource state |
| Current page | Client | Application state |
| Link to follow next | Client | Application state |
| Previous navigation steps | Client | Application state |

The server should not rely on remembering the client’s journey.

Each request must contain the information needed to process that request.

Suppose the client first sends:

```http
GET /todos
```

and later sends:

```http
GET /todos/42
```

The second request must be understandable independently.

The server should not need to think:

```text
This client previously requested /todos,
so it probably now means Todo 42.
```

The request itself states what is needed:

```http
GET /todos/42
Authorization: Bearer abc123
Accept: application/json
```

It includes:

- the requested operation;
- the resource address;
- authentication information;
- the desired representation.

## Important clarification

Statelessness does not mean that the server stores no data.

The server can store:

```text
Todo 42
Title: Study REST
Done: false
```

What it should not need to store is the client’s conversational or navigational history:

```text
This client previously opened the todo list.
Then it opened Todo 42.
Now it probably wants the comments.
```

==★ **Statelessness means every request must make sense on its own.**==

# 11. All Five Principles in One Example

Consider this request:

```http
GET /todos/12
Accept: application/json
```

The server responds:

```json
{
  "id": 12,
  "title": "Learn JavaScript",
  "links": [
    {
      "rel": "self",
      "href": "/todos/12"
    },
    {
      "rel": "show-comments",
      "href": "/todos/12/comments"
    }
  ]
}
```

This single interaction contains the complete lecture map:

1. **Unique identification**  
   `/todos/12` identifies the resource.

2. **Uniform interface**  
   `GET` is the standard operation for retrieving it.

3. **Representation diversity**  
   The client requests JSON using `Accept: application/json`.

4. **Hypermedia**  
   The response links to the todo itself and to its comments.

5. **Statelessness**  
   The request can be processed without remembering previous client requests.

# 12. Complete Technical Mapping

Suppose the client wants to retrieve todo `42`.

It sends:

```http
GET /todos/42
Accept: application/json
```

The server responds:

```json
{
  "id": 42,
  "title": "Study REST",
  "done": false,
  "links": [
    {
      "rel": "self",
      "href": "/todos/42"
    },
    {
      "rel": "show-comments",
      "href": "/todos/42/comments"
    }
  ]
}
```

Map every part:

```text
GET
│
└── HTTP method: what should happen?

/todos/42
│
└── URI: which resource?

Todo 42
│
└── Resource: the conceptual thing on the server

JSON object
│
└── Representation of Todo 42

/todos/42/comments
│
└── Hypermedia link to a related resource

No previous request required
│
└── Stateless communication
```

A useful formula is:

```text
HTTP method + URI = requested operation on a resource
```

Examples:

```text
GET    + /todos/42 = retrieve Todo 42
PUT    + /todos/42 = update Todo 42
DELETE + /todos/42 = delete Todo 42
```

The easiest complete sentence is:

==★ **A resource is the thing, its URI is its address, an HTTP method says what to do with it, a representation describes it, a hypermedia link shows where to go next, and statelessness means every request must make sense on its own.**==

# 13. Website Versus Web Service

In this lecture, “service” means a web service or API.

It does not mean customer service.

The difference is mainly:

- who consumes the response;
- what the response is used for.

| Aspect | Website | Web service / API |
|---|---|---|
| Main consumer | A human using a browser | Another software application |
| Typical response | A visual HTML page | Structured data such as JSON or XML |
| Main purpose | Display information and provide a user interface | Provide data or functionality to programs |
| Example request | Open a todo page | Request todo data |
| Example response | A formatted page with buttons and text | A JSON object describing a todo |

## Website example

A user opens:

```http
GET /todos/42
```

The server may return HTML:

```html
<h1>Study REST</h1>
<p>Status: Open</p>
<button>Mark as completed</button>
```

The browser renders this as a page that a human can read and interact with.

## Web service example

A mobile application sends:

```http
GET /api/todos/42
```

The server returns JSON:

```json
{
  "id": 42,
  "title": "Study REST",
  "done": false
}
```

The JSON is not normally the final user interface.

The mobile application reads the data and decides how to display it.

```text
Website:
Human → Browser → Server → HTML page → Human

Web service:
Application → API server → JSON/XML data → Application
```

## Why does the lecture compare them?

Traditional Web pages already follow principles such as:

- each resource has an address;
- standard HTTP operations are used;
- pages can link to other resources;
- different representations can be transferred.

REST applies those successful ideas to software-accessible services.

For example:

```text
/articles/42
```

may identify a Web article.

```text
/todos/42
```

may identify a todo resource in a REST API.

Both use:

```text
address + standard HTTP communication + representations + links
```

The important difference is that a website commonly returns a presentation for a human, while a web service commonly returns data for another program.

==★ **A website is usually the human-facing interface; a web service is usually the software-facing interface.**==

# 14. What Exactly Is a Web Service?

A web service is a program on a server that other programs can communicate with over the Web.

Websites and web services use many of the same technical mechanisms:

- both run on servers;
- both can be reached using URLs;
- both use HTTP requests and responses;
- both may use methods such as GET and POST.

The main difference is what the server sends back and who is expected to use it.

## Restaurant analogy

Imagine a restaurant with two ways to interact.

### Website: the dining room

The restaurant provides:

- tables;
- menus;
- decorations;
- buttons or instructions;
- a presentation designed for humans.

This is like a website: a complete visual interface.

### Web service: the kitchen order window

Another system sends a structured order:

```text
Order:
- 2 pizzas
- 1 salad
```

The kitchen responds:

```text
Order accepted
Order number: 42
```

There is no decorated dining room.

The communication is designed so another system can process it.

That is like a web service.

## What does a web service serve?

A web service can provide data or perform operations.

```http
GET /todos/42
```

Return a todo.

```http
POST /todos
```

Create a todo.

```http
PUT /todos/42
```

Update todo `42`.

```http
DELETE /todos/42
```

Delete todo `42`.

The client calling the service might be:

- a website’s JavaScript;
- a mobile application;
- another company’s server;
- a desktop program;
- another part of the same application.

A web service is therefore a software-facing entrance to server functionality.

## Can a web service be opened in a browser?

Yes.

A browser can send HTTP requests.

Opening a web-service URL may display raw JSON:

```json
{
  "id": 42,
  "title": "Study REST"
}
```

This does not make it a normal website.

The browser is simply showing data that was primarily designed for software to process.

A normal website usually gives:

- page layout;
- headings;
- forms;
- navigation;
- buttons;
- styling.

A web service usually gives:

- JSON or XML data;
- status codes;
- headers;
- links to related resources.

# 15. How Websites and Web Services Work Together

A website and a web service are often part of the same system.

```text
Human
  ↓
Website in browser
  ↓
JavaScript calls web service
  ↓
Web service returns JSON
  ↓
Website displays the JSON as HTML
```

Example:

1. A user opens a todo website.
2. The website displays a loading state.
3. JavaScript calls:

```http
GET /api/todos
```

4. The web service returns:

```json
[
  {
    "id": 1,
    "title": "Study REST"
  },
  {
    "id": 2,
    "title": "Buy food"
  }
]
```

5. JavaScript turns the data into:

```text
My Todos

1. Study REST
2. Buy food
```

Here:

- the website is what the human sees;
- the web service supplies the data behind it.

At the communication level, websites and web services are not completely different.

Both use the Web and HTTP.

The difference is mainly at the response level:

```text
Website:
Request → server → ready-to-display interface

Web service:
Request → server → data or operation result
```

# 16. REST Versus HTTP

REST and HTTP are not the same.

REST is a set of design principles.

HTTP is a concrete communication protocol.

A useful analogy is:

```text
REST = building plan
HTTP = materials and tools
```

REST defines principles.

HTTP provides mechanisms commonly used to realize them.

| REST principle | Common HTTP implementation |
|---|---|
| Resource has a unique identifier | URI such as `/todos/42` |
| Uniform operations | `GET`, `POST`, `PUT`, `DELETE` |
| Resource representations | JSON, XML, or HTML bodies |
| Representation choice | `Accept` and `Content-Type` headers |
| Resources link to other resources | Links inside JSON or HTML |
| Stateless communication | Each request contains the required information |

Example:

```http
GET /todos/42
Accept: application/json
```

Here:

- REST says: identify a resource and request its representation.
- HTTP supplies:
  - `GET` as the operation;
  - `/todos/42` as the URI;
  - `Accept` as the way to request JSON.

In simple words:

```text
REST describes how a service should be designed.
HTTP is the technology commonly used to build and communicate with it.
```

```text
REST ≠ HTTP
```

but in many real systems:

```text
REST principles + HTTP mechanisms = RESTful web service
```

# 17. What Does It Mean That REST Abstracts Away from HTTP?

To abstract means to focus on the general idea and ignore the concrete technical details.

REST says:

- every resource should be identifiable;
- use a uniform and restricted interface;
- transfer representations;
- link resources;
- keep communication stateless.

REST does not fundamentally say:

```text
You must always use HTTP GET.
You must always use HTTP headers.
You must always use JSON.
```

Those are common choices when implementing REST with HTTP.

Theoretically, another technology could follow REST principles if it provided:

- identifiers for resources;
- a small standard set of operations;
- representations;
- links;
- stateless messages.

## Why is HTTP used in practice?

HTTP already fits REST very well.

It provides:

- URIs;
- standard methods;
- request and response messages;
- headers;
- status codes;
- content types;
- links.

Developers therefore normally use HTTP instead of inventing another technology.

## Address analogy

Consider this principle:

```text
Every house must have a unique address.
```

The principle is independent of whether the address appears:

- on a metal sign;
- on a wooden sign;
- in a digital map.

Similarly:

```text
REST principle:
Every resource has a unique identifier.

HTTP implementation:
https://example.com/todos/42
```

The principle and the implementation are related but not identical.

# 18. Why Is REST Needed If HTTP Already Exists?

## Formal question

**If HTTP already provides the mechanisms used by REST, why is REST needed as a separate architectural style?**

HTTP provides capabilities, but it does not force developers to use them in a RESTful way.

HTTP tells us how messages can be exchanged.

REST tells us how a service should be designed using those messages.

## HTTP is a toolbox

HTTP provides:

- URIs;
- methods such as GET, POST, PUT, and DELETE;
- request and response bodies;
- headers;
- status codes.

But HTTP does not decide:

- what the URIs should represent;
- which method should be used for each operation;
- whether communication should be stateless;
- whether resources should contain links;
- whether the interface should be uniform.

Developers can use HTTP in many different styles.

## Example: HTTP without REST

A service could use one endpoint:

```http
POST /service
Content-Type: application/json
```

The requested operation appears in the body:

```json
{
  "operation": "deleteTodo",
  "todoId": 42
}
```

Another request might use the same endpoint:

```http
POST /service
Content-Type: application/json
```

```json
{
  "operation": "getTodo",
  "todoId": 42
}
```

This uses HTTP, but it does not follow REST very well because:

- resources do not have clear individual URIs;
- `POST` is used for every operation;
- the HTTP interface is not used uniformly;
- the operation is hidden inside the message body.

HTTP allows this design.

It does not prevent it.

## RESTful version

REST gives the todo its own URI:

```text
/todos/42
```

Then standard HTTP methods express the operation:

```http
GET /todos/42
```

Retrieve the todo.

```http
PUT /todos/42
```

Update the todo.

```http
DELETE /todos/42
```

Delete the todo.

Responsibilities are now clear:

```text
URI         → which resource?
HTTP method → what operation?
```

## Road-system analogy

HTTP is like a road system.

It provides:

- roads;
- traffic signals;
- signs;
- vehicles.

But having roads does not guarantee that a city is well designed.

Roads may be confusing, badly connected, or inconsistently labelled.

REST is like a city-planning approach that says:

- every location should have a clear address;
- standard traffic rules should be used;
- signs should point to related locations;
- checkpoints should not need to remember where every traveller came from.

```text
HTTP = communication infrastructure
REST = architectural rules for using that infrastructure
```

## Does HTTP already match REST well?

Yes.

| REST principle | HTTP mechanism |
|---|---|
| Unique identification | URIs |
| Uniform interface | Standard HTTP methods |
| Different representations | Bodies and content-type headers |
| Hypermedia links | Links in representations |
| Stateless communication | Independent request messages |

HTTP offers these mechanisms.

REST tells developers to use them consistently.

## Why does REST exist?

REST exists because services need more than a way to send messages.

They also need a consistent structure.

Without REST, HTTP services might use:

```text
/getTodo?id=42
/removeTodo?id=42
/changeTodo?id=42
```

or:

```text
/runOperation
```

With REST, a resource-oriented pattern is encouraged:

```http
GET /todos/42
PUT /todos/42
DELETE /todos/42
```

This makes the service easier to understand because developers already know the meaning of the standard HTTP operations.

==★ **HTTP makes Web communication possible. REST provides principles for organizing a service that communicates over the Web.**==

# 19. Final Exam-Ready Questions

## What is REST?

REST is an architectural style for designing web services according to principles inspired by the World Wide Web.

## What does REST stand for?

```text
Representational State Transfer
```

## Is REST a programming language, framework, or protocol?

No.

REST is an architectural style.

## Is REST the same as HTTP?

No.

REST is a design style.

HTTP is a concrete communication protocol commonly used to implement it.

## Why was REST developed?

It was motivated by the success of the Web and applies Web principles to software-accessible services.

## What are the five REST principles?

1. Unique identification through URIs
2. Uniform and restricted interface
3. Representation diversity
4. Hypermedia links
5. Statelessness

## What is a resource?

A resource is the conceptual entity exposed by the service.

Examples include a todo, a collection of todos, or comments belonging to a todo.

## What is a URI?

A URI uniquely identifies a resource.

## What is the relationship between a URI and an HTTP method?

The URI identifies the resource.

The method identifies the operation to perform on it.

## What does uniform interface mean?

Standard methods have consistent meanings throughout the service.

## What does restricted interface mean?

The service uses a limited standard set of operations instead of inventing a new method for each use case.

## What does safe mean?

A safe operation does not change the state of the requested resource.

## What does idempotent mean?

Repeating the same request has the same overall side effect as sending it once.

## Does idempotent mean every response is identical?

No.

Responses may differ, but the final side effect remains the same.

## Why is POST usually not idempotent?

Repeating a POST request can create additional resources or side effects.

## Why is PUT idempotent?

Repeating the same PUT request continues setting the resource to the same state.

## What is the difference between a resource and a representation?

A resource is the conceptual entity.

A representation is JSON, XML, HTML, or another concrete description of it.

## Is a resource the same as JSON?

No.

JSON is only one possible representation.

## What is HATEOAS?

HATEOAS means Hypermedia as the Engine of Application State.

It allows the server to include links describing related resources or possible next actions.

## What does `rel` mean in a hypermedia link?

It describes the relationship or meaning of the link.

## What does `href` mean?

It gives the URI of the linked resource.

## What does statelessness mean?

Every request contains the information needed to process it without relying on the server remembering previous client requests.

## Does statelessness mean the server stores no data?

No.

The server stores resource state.

The client manages application and navigation state.

## Where is resource state stored?

On the server.

## Where is application state stored?

On the client.

## What is a web service?

A web service is server-side functionality designed mainly for other programs to call over the Web.

## How is a website different from a web service?

A website usually returns a human-facing interface.

A web service usually returns data or an operation result for software.

## Can a web service be opened in a browser?

Yes.

The browser may display raw JSON or XML, but the response is still mainly designed for software.

## Why can REST be described independently of HTTP?

REST defines general architectural principles.

HTTP is one concrete technology used to implement them.

## Why is HTTP commonly used for REST?

HTTP already provides URIs, methods, headers, status codes, representations, links, and stateless messages.

## If HTTP already exists, why is REST needed?

HTTP provides communication tools.

REST provides consistent architectural rules for organizing those tools.

# 20. Final Memory Maps

## REST overview

```text
REST
│
├── Comes from principles of the WWW
├── Treats service data as resources
└── Five principles
    ├── URI          → every resource has an address
    ├── Methods      → standard, restricted operations
    ├── Formats      → one resource, several representations
    ├── Links        → server shows possible next actions
    └── Stateless    → client remembers its journey
```

## One complete interaction

```text
Client sends:
GET /todos/42
Accept: application/json
        ↓
GET
└── HTTP method: retrieve

/todos/42
└── URI: Todo 42

Todo 42
└── Resource on the server
        ↓
Server returns JSON
└── Representation

Response contains /todos/42/comments
└── Hypermedia link

No previous request is required
└── Stateless communication
```

## REST and HTTP

```text
REST
└── Architectural principles

HTTP
└── Communication mechanisms

Together in practice
└── RESTful web service
```

# Final Sentence to Remember

==★ **A resource is the thing, its URI is its address, an HTTP method says what to do with it, a representation describes it, a hypermedia link shows where to go next, and statelessness means every request must make sense on its own.**==
