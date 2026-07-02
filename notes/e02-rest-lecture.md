# Lecture E02: REST

## Beginner-Friendly Mental Model

Think of a REST service as a city containing identifiable places.

| REST concept | City analogy | Technical meaning |
|---|---|---|
| Resource | A place, such as a library | An entity or piece of information exposed by the server |
| URI | The address of that place | The unique identifier of a resource |
| HTTP method | A standard action performed there | The operation requested by the client |
| Representation | A map, photo, or description | JSON, XML, HTML, or another concrete format |
| Hypermedia link | A sign showing where to go next | A link to another resource or possible action |
| Statelessness | The traveller remembers the journey | Every request contains the information needed to process it |

==★ **REST identifies resources with URIs, manipulates them through standard operations, exchanges representations, connects them through links, and keeps application state on the client.**==

# 1. What Is REST?

REST stands for:

```text
Representational State Transfer
```

REST is an **architectural style** for designing web services. It was described by Roy Fielding in his PhD thesis.

REST is:

- not a programming language;
- not a framework or library;
- not identical to HTTP;
- not a concrete implementation.

REST was inspired by the success of the World Wide Web. The idea is that services can benefit from the same principles used by the Web: identifiable resources, standard operations, representations, links, and stateless communication.

# 2. How Does Web Communication Work?

Communication involves:

- a client, such as a browser or mobile app;
- a server;
- resources exposed by the server;
- HTTP requests and responses.

A resource can be an HTML page, image, document, todo, comment, or collection.

A **URI** identifies a resource. A URL is a common kind of URI used on the Web.

Examples:

```text
/todos
/todos/42
/todos/42/comments
```

Clients perform operations through HTTP methods:

```http
GET
POST
PUT
DELETE
HEAD
OPTIONS
```

A client may request a particular representation:

```http
GET /todos/42
Accept: application/json
```

The basic flow is:

```text
Client sends URI + HTTP operation
                ↓
Server processes the resource
                ↓
Server returns a representation
```

# 3. What Is the Basic Idea of REST?

REST treats service data as resources.

Less REST-like:

```text
/getTodo?id=42
```

Resource-oriented REST style:

```http
GET /todos/42
```

The two parts have separate meanings:

```text
/todos/42 → Which resource?
GET       → What should happen to it?
```

==★ **The URI identifies the resource; the HTTP method identifies the operation.**==

# 4. The Five REST Principles

The lecture presents five principles:

1. Unique identification through URIs
2. Uniform and restricted interface
3. Representation diversity
4. Hypermedia links
5. Statelessness

# 5. Unique Identification Through URIs

Every resource should have a unique URI.

```text
/todos
```

Represents the collection of todos.

```text
/todos/42
```

Represents todo `42`.

```text
/todos/42/comments
```

Represents the comments of todo `42`.

REST-style URIs normally contain nouns representing resources.

The action is expressed through the method:

```http
GET /todos/42
PUT /todos/42
DELETE /todos/42
```

The URI stays the same because the resource is the same. Only the requested action changes.

# 6. Uniform and Restricted Interface

A REST service uses a standard set of operations instead of inventing a new operation for every use case.

“Uniform” means that a method keeps the same general meaning:

```http
GET /todos/42
GET /todos/99
```

Both retrieve a resource.

“Restricted” means developers do not invent methods such as:

```text
FIND-TODO
COMPLETE-TODO
SHOW-COMMENTS
```

They use the standard HTTP methods and design the resources around them.

# 7. Safe and Idempotent Methods

## Safe

A method is safe when it does not change the requested resource state.

```http
GET /todos/42
```

should retrieve the todo without modifying it.

Logging is still allowed. The key point is that the resource itself is not changed.

## Idempotent

A method is idempotent when repeating the same request has the same overall side effect as sending it once.

```http
DELETE /todos/42
```

After the first successful deletion, repeating it does not make the resource “more deleted.”

The responses may differ, but the final server state remains the same.

| Method | Meaning | Safe? | Idempotent? |
|---|---|---:|---:|
| `GET` | Retrieve a representation | Yes | Yes |
| `PUT` | Replace or create a resource | No | Yes |
| `DELETE` | Delete a resource | No | Yes |
| `POST` | Add something to a resource or collection | No | No |
| `HEAD` | Like GET, without a response body | Yes | Yes |
| `OPTIONS` | Ask which operations are supported | Yes | Yes |

## Why is POST not idempotent?

```http
POST /todos/42/comments
```

Sending the same request twice may create two comments.

## Why is PUT idempotent?

```http
PUT /todos/42
Content-Type: application/json
```

```json
{
  "title": "Learn JavaScript"
}
```

Repeating it continues setting the resource to the same state.

# 8. Resource Versus Representation

A **resource** is the conceptual thing exposed by the server.

Example:

```text
Todo 12
```

A **representation** is a concrete description of that resource.

JSON:

```json
{
  "id": 12,
  "title": "Learn JavaScript",
  "text": "I should not keep putting it off."
}
```

XML:

```xml
<todo>
  <id>12</id>
  <title>Learn JavaScript</title>
  <text>I should not keep putting it off.</text>
</todo>
```

HTML:

```html
<h1>Learn JavaScript</h1>
<p>Todo ID: 12</p>
```

The resource remains the same, but the representation changes.

==★ **The resource is the thing; JSON, XML, or HTML is only a representation of it.**==

# 9. What Is HATEOAS?

HATEOAS means:

```text
Hypermedia as the Engine of Application State
```

The server can include links that tell the client what it can do next.

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

Here:

- `rel` describes the meaning of the link;
- `href` gives the URI.

Mental model:

```text
You are at Todo 12.
A road sign tells you where its comments are.
```

The client discovers related resources from the response.

# 10. What Does Statelessness Mean?

REST distinguishes between resource state and application state.

| State | Managed by | Example |
|---|---|---|
| Resource state | Server | Todo title and completion status |
| Application state | Client | Which page or resource the client is viewing |

Each request must contain the information needed to process it:

```http
GET /todos/42
Authorization: Bearer abc123
Accept: application/json
```

The server does not need to remember that the client previously requested `/todos`.

Statelessness does **not** mean that the server stores no data. It can store todos, users, and other resource state. It should not need to store the client’s navigation history.

==★ **Statelessness means every request must make sense on its own.**==

# 11. All Five Principles in One Example

Request:

```http
GET /todos/12
Accept: application/json
```

Response:

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

This demonstrates:

1. `/todos/12` uniquely identifies the resource.
2. `GET` is the standard retrieval operation.
3. The client requests a JSON representation.
4. The response links to related resources.
5. The request can be processed independently.

# 12. Complete Technical Mapping

```text
GET
└── HTTP method: what should happen?

/todos/42
└── URI: which resource?

Todo 42
└── Resource: the conceptual thing on the server

JSON object
└── Representation of Todo 42

/todos/42/comments
└── Hypermedia link to a related resource

No previous request required
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

# 13. Website Versus Web Service

In this lecture, “service” means a web service or API.

| Aspect | Website | Web service / API |
|---|---|---|
| Main consumer | Human | Software application |
| Typical response | HTML page | JSON or XML |
| Main purpose | Present a user interface | Provide data or functionality |
| Example | Page with buttons and text | Todo object as JSON |

Website response:

```html
<h1>Study REST</h1>
<p>Status: Open</p>
<button>Mark as completed</button>
```

Web service response:

```json
{
  "id": 42,
  "title": "Study REST",
  "done": false
}
```

A website is mainly human-facing. A web service is mainly software-facing.

A browser can display a web service response, but it may only show raw JSON because the response is designed for software rather than as a complete interface.

# 14. How Websites and Web Services Work Together

Modern applications often use both:

```text
Human
  ↓
Website or mobile application
  ↓
JavaScript calls a web service
  ↓
Web service returns JSON
  ↓
Application displays the data
```

Example:

```http
GET /api/todos
```

Response:

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

JavaScript can turn this data into a visible todo list.

# 15. Is REST the Same as HTTP?

No.

REST is an architectural style. HTTP is a communication protocol commonly used to implement it.

```text
REST = design principles
HTTP = concrete communication mechanisms
```

| REST idea | Common HTTP implementation |
|---|---|
| Unique resource identifier | URI such as `/todos/42` |
| Uniform operations | GET, POST, PUT, DELETE |
| Representations | JSON, XML, HTML bodies |
| Representation choice | Accept and Content-Type headers |
| Hypermedia | Links inside representations |
| Stateless communication | Independent request messages |

REST can theoretically be implemented using another technology, but HTTP is used in practice because it already provides suitable mechanisms.

# 16. Why Is REST Needed If HTTP Already Exists?

HTTP provides tools, but it does not force developers to use them in a RESTful way.

HTTP provides:

- URIs;
- methods;
- headers;
- request and response bodies;
- status codes.

But HTTP does not decide:

- what a URI should represent;
- which method should be used;
- whether the service should be stateless;
- whether links should be included;
- whether the interface is uniform.

## HTTP without a strong REST design

```http
POST /service
Content-Type: application/json
```

```json
{
  "operation": "deleteTodo",
  "todoId": 42
}
```

The same endpoint might also be used for retrieval:

```json
{
  "operation": "getTodo",
  "todoId": 42
}
```

This uses HTTP, but:

- the resource has no clear individual URI;
- POST is used for every operation;
- the operation is hidden in the body;
- the HTTP interface is not used uniformly.

## RESTful version

```http
GET /todos/42
PUT /todos/42
DELETE /todos/42
```

Now the responsibilities are clear:

```text
URI         → which resource?
HTTP method → what operation?
```

==★ **HTTP makes Web communication possible; REST provides principles for organizing a service that communicates over the Web.**==

# Exam-Ready Questions

## What is REST?

REST is an architectural style for designing web services according to principles inspired by the World Wide Web.

## What are the five REST principles?

1. Unique identification through URIs
2. Uniform and restricted interface
3. Representation diversity
4. Hypermedia links
5. Statelessness

## Is REST the same as HTTP?

No. REST is an architectural style; HTTP is a protocol commonly used to implement it.

## What is the difference between a resource and a representation?

A resource is the conceptual entity. A representation is JSON, XML, HTML, or another format describing it.

## What does safe mean?

The operation does not change the requested resource state.

## What does idempotent mean?

Repeating the same request has the same overall side effect as sending it once.

## Why is POST not idempotent?

Repeating a POST request can create additional resources or side effects.

## What is HATEOAS?

It is the principle of including links in responses so clients can discover related resources or possible next actions.

## What does statelessness mean?

Every request contains the information needed to process it, without relying on the server remembering the client’s previous requests.

## What is a web service?

A web service is server-side functionality designed mainly for other software to call over the Web.

## Why is REST needed when HTTP already exists?

HTTP provides communication mechanisms. REST provides design principles for using those mechanisms consistently.

# Final Memory Map

```text
REST
│
├── Comes from principles of the Web
├── Treats service data as resources
└── Five principles
    ├── URI       → every resource has an address
    ├── Methods   → standard, restricted operations
    ├── Formats   → one resource, multiple representations
    ├── Links     → server shows possible next actions
    └── Stateless → client remembers its journey
```

# Final Sentence to Remember

==★ **A resource is the thing, its URI is its address, an HTTP method says what to do with it, a representation describes it, a hypermedia link shows where to go next, and statelessness means every request must make sense on its own.**==
