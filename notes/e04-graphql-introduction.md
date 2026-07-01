# Lecture E04: GraphQL Introduction

## Mental Model: Fixed Menus Versus a Custom Order

Imagine that a server is a restaurant and an application is a customer.

- With a typical REST API, the restaurant offers several fixed meals. Each endpoint determines what is included.
- With GraphQL, the customer writes down exactly which items they want.
- The server processes that request and returns only those items.

Different clients may need very different data:

- A desktop application may need a todo together with all its comments.
- A mobile overview may need only the todo title.
- Another client may need titles and comment texts, but not IDs.

==★ **The client specifies the exact structure of the required data, and the server returns data in approximately the same structure.**==

# 1. Where Does GraphQL Fit?

GraphQL is presented as an alternative to REST for implementing APIs.

According to the lecture:

- Development began at Facebook in 2012.
- GraphQL was publicly released in 2015.
- It was transferred to the GraphQL Foundation in 2018.
- Its behavior is formally described in the GraphQL specification.

This lecture is an introduction.

Its focus is:

1. why GraphQL was created;
2. which REST-related problems motivate it;
3. how a basic GraphQL request and response are structured.

# 2. Essential Vocabulary

| Term | Meaning in this lecture |
|---|---|
| Client | The application using the API, such as a browser, mobile app, or frontend |
| Server | The system that receives requests and supplies data |
| Resource | An object exposed through an API, such as a todo |
| Endpoint | An address through which an API operation is accessed, such as `/todos/42` |
| Aggregation | Returning one object together with related objects |
| Schema | A description of which data types, fields, and relationships are available |
| Graph | Data represented as objects connected through relationships |
| Subgraph | A selected portion of that graph |

For example, a `Todo` object and its associated `Comment` objects form a small graph:

```text
Todo
├── Comment 1
├── Comment 2
└── Comment 3
```

The todo and comments are the objects.

The association between them is the relationship.

# 3. Why Can REST APIs Be Challenging for Different Clients?

The structure of a REST API often reflects assumptions made by the API designer.

For example, when designing the response for:

```http
GET /todos/42
```

the API designer must decide:

- Should the response contain only the todo?
- Should it also contain all comments?
- Should comments be retrieved through another endpoint?
- Which fields should always be returned?

The server chooses a response structure before knowing the exact requirements of every future client.

That can create two opposite problems:

1. **Overfetching** — the server returns more data than the client needs.
2. **Underfetching** — one response does not contain enough data, so the client must make further requests.

# 4. REST Scenario 1: Aggregated Data

In the first scenario, the REST API returns a todo together with all of its comments.

## Request

```http
GET /todos/42
```

## Response

```json
{
  "id": 42,
  "title": "Learn JavaScript",
  "text": "I can't ignore it any longer.",
  "comments": [
    {
      "id": 1,
      "text": "Did nothing today."
    },
    {
      "id": 2,
      "text": "Good source: Book by Kyle Simpson."
    }
  ]
}
```

The response contains:

- the todo ID;
- the todo title;
- the todo text;
- all comments associated with the todo.

This is called **aggregated data**, because the main object and its related objects are combined into one response.

## When Is This Approach Useful?

This is suitable for clients that need to display or process the todo and its comments together.

For example, a todo detail page may show:

```text
Learn JavaScript
I can't ignore it any longer.

Comments:
- Did nothing today.
- Good source: Book by Kyle Simpson.
```

Only one HTTP request is needed to obtain all the information.

## What Is Overfetching?

Overfetching means that the server returns more data than the client actually needs.

Suppose a mobile overview screen displays only:

```text
Learn JavaScript
```

The client only needs the title, but the REST response also contains:

- `id`;
- `text`;
- all comment IDs;
- all comment texts.

The response structure is fixed by the API, so the client receives unnecessary data.

Possible consequences:

- Bandwidth is wasted.
- Performance may become worse.
- The client must parse and possibly filter unnecessary data.
- The API transfers data that is not required.
- Large related collections make the problem more significant.

```text
Client needs:
title

Server sends:
id + title + text + every comment

Result:
overfetching
```

# 5. REST Scenario 2: Separate Endpoints

The second REST design does not aggregate the related objects.

The todo and its comments are available through separate endpoints.

## First request: obtain the todo

```http
GET /todos/42
```

## First response

```json
{
  "id": 42,
  "title": "Learn JavaScript",
  "text": "I can't ignore it any longer."
}
```

This response does not contain comments.

## Second request: obtain the comments

```http
GET /todos/42/comments
```

## Second response

```json
[
  {
    "id": 1,
    "text": "Did nothing today."
  },
  {
    "id": 2,
    "text": "Good source: Book by Kyle Simpson."
  }
]
```

## When Is This Approach Useful?

It is suitable for clients that do not require comments.

For example, a todo overview can request only:

```http
GET /todos/42
```

It does not need to receive comments.

## What Is Underfetching?

Underfetching means that one response does not contain enough data for the client’s task.

Suppose a client needs both:

- the todo;
- its comments.

The first request gives only the todo.

The client must send a second request for the comments.

```text
Request 1 → todo
Request 2 → comments
```

One request did not provide enough information, so additional requests were required.

Possible consequences:

- More network traffic is produced.
- Every request and response adds latency.
- Application performance may become worse.
- Time to Interactive may increase.

## What Is Time to Interactive?

Time to Interactive, or **TTI**, indicates when a website is ready to react properly to user input.

A page may already be visible but not yet usable because it is still waiting for comment data.

# 6. The Basic Trade-Off in the REST Examples

| REST design | Advantage | Potential disadvantage |
|---|---|---|
| Return todo and comments together | One request provides everything | Overfetching when comments are not needed |
| Return todo and comments separately | Clients can avoid requesting comments | Underfetching when both are needed |

The API designer cannot always choose one fixed response structure that is ideal for every client.

```text
Aggregated endpoint
        ↓
Good for clients needing everything
        ↓
Bad for clients needing only a few fields
```

```text
Separate endpoints
        ↓
Good for clients needing only the todo
        ↓
Bad for clients needing todo + comments
```

This design tension is the motivation for GraphQL in the lecture.

# 7. What Is the Basic Idea of GraphQL?

GraphQL allows clients to formulate specific requests that state exactly which data should be returned.

Instead of the server deciding one fixed representation for every client, the client selects the required fields.

Examples:

- A list view can request only todo titles.
- A detail view can request the title, text, and comments.
- Another view can request only titles and comment texts.

The API remains the same, but the request can differ according to the client’s needs.

==★ **GraphQL addresses overfetching and underfetching by allowing the client to request exactly the fields and relationships it needs.**==

# 8. The Two Components of GraphQL

The lecture describes GraphQL as supporting APIs through two components.

## 1. A Language

GraphQL provides a language for:

- querying data;
- manipulating data;
- defining a schema.

The client uses this language to describe what it needs.

## 2. A Server-Side Runtime Environment

The GraphQL server needs a runtime that:

- receives a GraphQL request;
- evaluates the query;
- obtains the requested data;
- builds the response.

```text
GraphQL language
        ↓
Describes the required data

GraphQL runtime
        ↓
Obtains and returns that data
```

# 9. Why Is It Called “GraphQL”?

GraphQL understands application data as a graph structure.

Example:

```text
Todos
├── Todo: Learn JavaScript
│   ├── Comment: Did nothing today.
│   └── Comment: Good source: Book by Kyle Simpson.
└── Todo: Learn GraphQL
    └── Comment: Is it better than REST?
```

Possible nodes include:

- todo objects;
- comment objects.

Possible relationships include:

- a todo has comments.

A query selects a part of this graph: a **subgraph**.

For example:

```text
Todo title
└── Comment text
```

Fields such as the todo’s own text and the comment ID are not selected, so they do not need to appear in the result.

# 10. GraphQL Uses One API Endpoint in the Lecture

The structure illustrated in the lecture uses:

```http
POST /graphql
```

The entire GraphQL API is made available through this single endpoint.

This differs from the REST examples:

```http
GET /todos/42
```

and:

```http
GET /todos/42/comments
```

With GraphQL, the endpoint remains:

```http
POST /graphql
```

What changes is the GraphQL query sent in the request.

==★ **A single endpoint does not mean that every client receives the same data. The query inside the request specifies the required data.**==

# 11. The Complete GraphQL Query

The client sends the following query to:

```http
POST /graphql
```

```graphql
# Select all todos along with their "title" attribute
# plus associated comments and their attribute
# "text"
{
  todos {
    title
    comments {
      text
    }
  }
}
```

## Comments

```graphql
# Select all todos along with their "title" attribute
# plus associated comments and their attribute
# "text"
```

Lines beginning with `#` are comments.

They explain the purpose of the query.

## Outer braces

```graphql
{
  ...
}
```

The braces contain the client’s requested selection.

## Select todos

```graphql
todos {
  ...
}
```

This asks for the available todo objects.

## Select only the todo title

```graphql
title
```

For each todo, return its title.

The client does not request:

```text
id
text
```

Therefore, those fields do not appear in the result.

## Follow the relationship to comments

```graphql
comments {
  ...
}
```

For each todo, follow the relationship to its associated comments.

## Select only comment text

```graphql
text
```

For every comment, return only the comment’s text.

The comment ID is not requested.

# 12. The Query Selects a Subgraph

The complete query:

```graphql
{
  todos {
    title
    comments {
      text
    }
  }
}
```

can be read as a tree:

```text
todos
├── title
└── comments
    └── text
```

The data may contain many more fields:

```text
Todo:
- id
- title
- text
- creationDate
- done
- comments

Comment:
- id
- text
- author
- date
```

But the query selects only:

```text
Todo.title
Todo.comments.text
```

That selected structure is the requested subgraph.

# 13. What Happens on the Server?

After receiving the request, the GraphQL runtime evaluates it on the server.

The simplified flow is:

```text
1. Client sends POST /graphql
2. Request contains a GraphQL query
3. Server evaluates the query
4. Server obtains the requested todo data
5. Server constructs a response matching the query
6. Response is returned to the client
```

GraphQL is not simply a different JSON response format.

The server must understand and execute the GraphQL query.

# 14. The Complete Response

The server returns a response resembling:

```json
{
  "data": {
    "todos": [
      {
        "title": "Learn JavaScript",
        "comments": [
          {
            "text": "Did nothing today."
          },
          {
            "text": "Good source: Book by Kyle Simpson."
          }
        ]
      },
      {
        "title": "Learn GraphQL",
        "comments": [
          {
            "text": "Is it better than REST?"
          }
        ]
      }
    ]
  }
}
```

## `data`

```json
"data": {
  ...
}
```

The requested result is placed inside the `data` property.

## `todos`

```json
"todos": [
  ...
]
```

This corresponds to the `todos` field requested in the query.

## `title`

```json
"title": "Learn JavaScript"
```

This appears because the query explicitly selected:

```graphql
title
```

## `comments`

```json
"comments": [
  ...
]
```

This appears because the query followed the `comments` relationship.

## Comment text

```json
{
  "text": "Did nothing today."
}
```

Only `text` appears because that is the only comment field selected by the query.

Comment IDs are not returned.

# 15. The Request Structure Resembles the Response Structure

## Request

```graphql
{
  todos {
    title
    comments {
      text
    }
  }
}
```

## Corresponding response structure

```json
{
  "data": {
    "todos": [
      {
        "title": "...",
        "comments": [
          {
            "text": "..."
          }
        ]
      }
    ]
  }
}
```

The correspondence is:

```text
Query field    Response field
-----------    --------------
todos      →   "todos"
title      →   "title"
comments   →   "comments"
text       →   "text"
```

==★ **The shape of the response resembles the shape of the query.**==

The query tells the server:

- which data is required;
- how that data should be nested.

# 16. How the GraphQL Example Reduces the Two REST Problems

The GraphQL query requests:

```graphql
{
  todos {
    title
    comments {
      text
    }
  }
}
```

It does not request:

- todo IDs;
- todo descriptions;
- comment IDs.

Compared with an aggregated REST response, it avoids transferring unnecessary fields.

At the same time, todos and comments are obtained through one GraphQL request.

The client does not need one request for todos and another for comments.

```text
REST aggregated response:
One request, possibly too much data
        ↓
Overfetching
```

```text
REST separate responses:
Exact resource separation, possibly several requests
        ↓
Underfetching
```

```text
GraphQL request:
One request containing the exact field selection
        ↓
Request only the required connected data
```

This is the central motivation of the lecture.

It is not a claim that every REST API always suffers from these problems.

The point is that fixed REST response structures can make varying client requirements difficult to satisfy.

# 17. REST and GraphQL in This Lecture

| Aspect | REST examples | GraphQL example |
|---|---|---|
| API access | Multiple resource-oriented endpoints | A single `/graphql` endpoint |
| Data selection | Primarily determined by the endpoint | Determined by the client’s query |
| Relationships | Embedded or obtained separately | Selected as nested fields |
| Response structure | Fixed by the endpoint’s design | Resembles the query structure |
| Possible problem | Overfetching or underfetching | Client requests the required fields |
| Server responsibility | Implement each endpoint’s response | Evaluate the GraphQL query |

# 18. Complete Lecture Map

```text
Different clients need different data
        ↓
A REST response often assumes what clients need
        ↓
Scenario 1: include related data
        ↓
Clients not needing it experience overfetching
        ↓
Scenario 2: separate related data
        ↓
Clients needing everything experience underfetching
        ↓
GraphQL lets clients specify exact fields
        ↓
Data is viewed as a graph
        ↓
The query selects a subgraph
        ↓
The server evaluates the query
        ↓
The response resembles the query's structure
```

# Exam-Ready Questions

## 1. What is GraphQL?

GraphQL is an alternative approach to REST for implementing APIs.

It provides:

1. a language for querying and manipulating data and defining a schema;
2. a server-side runtime for executing queries.

## 2. What is overfetching?

Overfetching occurs when an API response contains more data than the client requires.

## 3. What is underfetching?

Underfetching occurs when one API response does not contain enough data, requiring the client to send additional requests.

## 4. How does GraphQL address varying client requirements?

The client specifies exactly which fields and relationships should be returned.

## 5. Why is the data understood as a graph?

Objects are treated as nodes and their relationships as connections.

A query can select a connected portion, or subgraph, of the available data.

## 6. What are the two main components supported by GraphQL?

1. A language for querying and manipulating data and defining a schema.
2. A runtime for executing the query on the server.

## 7. What is significant about the GraphQL response structure?

The response resembles the content and nested structure of the client’s query.

## 8. Which endpoint is used in the lecture’s GraphQL example?

```http
POST /graphql
```

## 9. What exactly does the lecture’s query request?

For every todo:

- its title;
- its associated comments;
- the text of each comment.

It does not request:

- todo IDs;
- todo descriptions;
- comment IDs.

# Key Points to Remember

==★ **REST endpoints commonly provide server-defined data packages.**==

==★ **GraphQL allows the client to describe the exact connected data it needs.**==

==★ **A GraphQL query selects a subgraph of the available data.**==

==★ **The server returns a response whose structure resembles the query.**==

# One-Sentence Takeaway

==★ **REST endpoints commonly provide server-defined data packages, whereas GraphQL allows the client to describe the exact connected data it needs and returns a correspondingly structured response.**==
