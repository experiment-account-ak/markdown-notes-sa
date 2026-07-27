# API Migration

Yes - this is a very likely exam style. They may give you **GraphQL schema/request code** and ask you to convert it to REST-style thinking.

The key idea:

> **In REST, endpoints are based on resources. In GraphQL, the whole API is usually accessed through one endpoint such as `/graphql`, and the operation is written inside the request body.**

The lecture explicitly shows GraphQL using `HTTP POST /graphql` and notes that the entire API is available through a single endpoint. REST, in contrast, identifies resources using URIs like `/todos`, `/todos/42`, and `/todos/42/comments`. `E-apis-complete.pdf`
## 1. Main rule: REST vs GraphQL endpoints

## REST

REST uses **different endpoints for different resources**.

Example from lecture:

```http
GET /todos
GET /todos/42
GET /todos/42/comments
```

So in REST, endpoints are based on nouns/resources:

```text
todos
one todo
comments of one todo
```
## GraphQL

GraphQL normally uses **one endpoint**:

```http
POST /graphql
```

The actual operation is inside the request body:

```graphql
{
  todo(id: "42") {
    title
    comments {
      text
    }
  }
}
```

So in GraphQL:

```text
Endpoint: /graphql
Operation: written inside the GraphQL query/mutation body
```
## 2. Why does GraphQL usually have only one endpoint?

Because GraphQL does not use the URL to say **which resource and fields** are needed.

Instead, the client writes a request like:

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

This request itself tells the server:

```text
Start from todos
return title
go into comments
return text
```

So the endpoint stays the same:

```http
POST /graphql
```

but the body changes.

This is different from REST, where the URL changes:

```http
GET /todos
GET /todos/42
GET /todos/42/comments
```
## 3. If GraphQL code is given, how to answer “number of endpoints”?

## Example GraphQL schema

```graphql
type Query {
  todos: [Todo!]!
  todo(id: ID!): Todo
}

type Mutation {
  createTodo(title: String!, text: String): Todo!
}

type Todo {
  id: ID!
  title: String!
  text: String
  comments: [Comment]
}

type Comment {
  id: ID!
  text: String!
}
```

## GraphQL number of endpoints

```text
Number of endpoints: 1
Endpoint name: /graphql
```

## Why?

Because GraphQL exposes the API through one endpoint, and the client specifies the operation in the request body.

Possible operations:

```graphql
{
  todos {
    id
    title
  }
}
```

```graphql
{
  todo(id: "42") {
    title
  }
}
```

```graphql
mutation {
  createTodo(title: "Learn APIs", text: "Practice REST and GraphQL") {
    id
    title
  }
}
```

All of these go to:

```http
POST /graphql
```
## 4. How many REST endpoints would be needed?

If migrating the GraphQL schema above to REST, you would usually create endpoints based on resources.

Possible REST endpoints:

```http
GET /todos
GET /todos/{id}
GET /todos/{id}/comments
POST /todos
```

So number of REST endpoints here could be:

```text
4 endpoints
```

Depending on how much functionality is included.
## 5. Mapping GraphQL operations to REST

## Given GraphQL operation 1

```graphql
{
  todos {
    id
    title
  }
}
```

### REST migration

```http
GET /todos
```

### HTTP method

```text
GET
```

### Type of HTTP method

```text
Safe: yes
Idempotent: yes
```

Because GET only reads data.

### Number of REST endpoints needed

```text
1 endpoint
```

### Endpoint name

```http
/todos
```

### Possible JSON result

```json
[
  {
    "id": "42",
    "title": "Learn JavaScript"
  },
  {
    "id": "23",
    "title": "Look at GraphQL"
  }
]
```

### GraphQL endpoint count

```text
GraphQL: 1 endpoint → /graphql
REST: 1 endpoint → /todos
```
## 6. Given GraphQL operation 2

```graphql
{
  todo(id: "42") {
    id
    title
    text
  }
}
```

### REST migration

```http
GET /todos/42
```

### HTTP method

```text
GET
```

### Type of HTTP method

```text
Safe: yes
Idempotent: yes
```

### Endpoint name

```http
/todos/{id}
```

or specifically:

```http
/todos/42
```

### Number of REST endpoints

```text
1 endpoint
```

### Possible JSON result

```json
{
  "id": "42",
  "title": "Learn JavaScript",
  "text": "I cannot ignore it any longer."
}
```

### GraphQL version

```http
POST /graphql
```

with body:

```graphql
{
  todo(id: "42") {
    id
    title
    text
  }
}
```

So:

```text
GraphQL endpoint count: 1
REST endpoint count for this operation: 1
```
## 7. Given GraphQL operation 3: nested data

```graphql
{
  todo(id: "42") {
    title
    comments {
      text
    }
  }
}
```

This is more interesting.

## GraphQL

### Endpoint

```http
POST /graphql
```

### Number of GraphQL endpoints

```text
1 endpoint
```

### Why?

Because GraphQL can request nested connected data in one request body.

### Possible JSON result

```json
{
  "data": {
    "todo": {
      "title": "Learn JavaScript",
      "comments": [
        {
          "text": "Did nothing today."
        },
        {
          "text": "Good source: book by K. Simpson."
        }
      ]
    }
  }
}
```
## REST migration option A: aggregated endpoint

```http
GET /todos/42
```

This endpoint returns Todo together with comments.

### Number of REST endpoints

```text
1 endpoint
```

### Problem

If the client does not always need comments, this may cause **overfetching**.
## REST migration option B: separate endpoints

```http
GET /todos/42
GET /todos/42/comments
```

### Number of REST endpoints

```text
2 endpoints
```

### Problem

If the client needs both Todo and comments, this may cause **underfetching**, because one request is not enough.

The lecture describes exactly this trade-off: aggregated REST data can cause overfetching, while separate REST endpoints can cause underfetching. `E-apis-complete.pdf`
## 8. Given GraphQL operation 4: mutation

```graphql
mutation {
  createTodo(title: "Convert REST API to GraphQL", text: "Lorem ipsum...") {
    id
    title
    text
  }
}
```

## REST migration

```http
POST /todos
```

### HTTP method

```text
POST
```

### Type of HTTP method

```text
Safe: no
Idempotent: no
```

Because POST creates/adds something. In the lecture’s HTTP method table, POST is not safe and not idempotent. `E-apis-complete.pdf`

### Endpoint name

```http
/todos
```

### Number of REST endpoints

```text
1 endpoint
```

### Request body in REST

```json
{
  "title": "Convert REST API to GraphQL",
  "text": "Lorem ipsum..."
}
```

### Possible JSON result

```json
{
  "id": "123",
  "title": "Convert REST API to GraphQL",
  "text": "Lorem ipsum..."
}
```

### GraphQL endpoint count

```text
1 endpoint: /graphql
```

Even though it creates a Todo, the GraphQL endpoint is still the same. The difference is that the body contains a `mutation`.
## 9. Type of HTTP method: exam table

Use this table in the exam:

| HTTP method | Meaning | Safe? | Idempotent? |
|---|---|---:|---:|
| `GET` | Read resource | Yes | Yes |
| `POST` | Add/create something | No | No |
| `PUT` | Replace/create resource | No | Yes |
| `DELETE` | Delete resource | No | Yes |
| `HEAD` | Like GET but no body | Yes | Yes |
| `OPTIONS` | Ask supported operations | Yes | Yes |
## 10. Full exam-style example

## Given GraphQL code

```graphql
type Query {
  todos: [Todo!]!
  todo(id: ID!): Todo
}

type Mutation {
  createTodo(title: String!, text: String): Todo!
}

type Todo {
  id: ID!
  title: String!
  text: String
  comments: [Comment]
}

type Comment {
  id: ID!
  text: String!
}
```

And request:

```graphql
{
  todo(id: "42") {
    title
    comments {
      text
    }
  }
}
```
## 1. GraphQL to REST migration

Possible REST design:

```http
GET /todos/42
GET /todos/42/comments
```

or aggregated:

```http
GET /todos/42
```

where `/todos/42` returns both todo and comments.

Better answer in exam:

```text
If REST does not aggregate relationships:
GET /todos/42
GET /todos/42/comments

If REST aggregates the relationship:
GET /todos/42
```
## 2. Which HTTP method?

```text
GET
```

Because the operation reads data.
## 3. Name of endpoints

Separate REST version:

```http
/todos/42
/todos/42/comments
```

Generic endpoint names:

```http
/todos/{id}
/todos/{id}/comments
```
## 4. Number of endpoints

For REST:

```text
2 endpoints if comments are separate.
1 endpoint if todo and comments are aggregated.
```

For GraphQL:

```text
1 endpoint: /graphql
```
## 5. Result of operation JSON

GraphQL result:

```json
{
  "data": {
    "todo": {
      "title": "Learn JavaScript",
      "comments": [
        {
          "text": "Did nothing today."
        },
        {
          "text": "Good source: book by K. Simpson."
        }
      ]
    }
  }
}
```

REST result if aggregated:

```json
{
  "title": "Learn JavaScript",
  "comments": [
    {
      "text": "Did nothing today."
    },
    {
      "text": "Good source: book by K. Simpson."
    }
  ]
}
```

REST result if separate:

First request:

```json
{
  "id": "42",
  "title": "Learn JavaScript",
  "text": "I cannot ignore it any longer."
}
```

Second request:

```json
[
  {
    "text": "Did nothing today."
  },
  {
    "text": "Good source: book by K. Simpson."
  }
]
```
## 6. Type of HTTP method

```text
GET is safe and idempotent.
```

Because reading does not change resource state, and sending the same GET multiple times has the same intended effect.
## 11. Very important: GraphQL number of endpoints

For GraphQL, the answer is usually:

```text
Number of endpoints: 1
Endpoint: /graphql
```

## Why?

Because GraphQL does not create one URL per resource.

It uses one API endpoint:

```http
POST /graphql
```

Then the query body decides what is requested:

```graphql
{
  todos {
    id
    title
  }
}
```

or:

```graphql
{
  todo(id: "42") {
    comments {
      text
    }
  }
}
```

or:

```graphql
mutation {
  createTodo(title: "Learn APIs", text: "Practice") {
    id
  }
}
```

All go to:

```http
POST /graphql
```

So the exam answer:

```text
GraphQL has one endpoint because the request body specifies the operation and selected data, while REST uses different resource URIs.
```
## 12. Quick conversion cheat sheet

| GraphQL | REST migration | HTTP method | Safe? | Idempotent? |
|---|---|---|---:|---:|
| `todos { ... }` | `/todos` | `GET` | Yes | Yes |
| `todo(id: "42") { ... }` | `/todos/42` | `GET` | Yes | Yes |
| `todo(id:"42") { comments { ... } }` | `/todos/42/comments` or aggregated `/todos/42` | `GET` | Yes | Yes |
| `createTodo(...) { ... }` | `/todos` | `POST` | No | No |
| update/replace Todo | `/todos/42` | `PUT` | No | Yes |
| delete Todo | `/todos/42` | `DELETE` | No | Yes |
## 13. Final mental model

```text
REST:
URL tells what resource.
HTTP method tells what action.

GraphQL:
Endpoint is usually /graphql.
Request body tells what operation and fields.
```

So when asked:

> “In GraphQL, number of endpoints and why?”

Answer:

```text
GraphQL usually has one endpoint, commonly /graphql, because the client sends the operation and field selection inside the GraphQL request body. The endpoint does not change for todos, comments, queries, or mutations.
```

## Prompt

give one more similar question with different code with solution

Here is **one more similar exam-style question** with a different GraphQL code and full solution.
## Exam-style question

## Given GraphQL schema

```graphql
type Query {
  books: [Book!]!
  book(isbn: ID!): Book
}

type Mutation {
  createBook(
    title: String!
    author: String!
    year: Int
  ): Book!
}

type Book {
  isbn: ID!
  title: String!
  author: String!
  year: Int
  reviews(last: Int): [Review]
}

type Review {
  id: ID!
  rating: Int!
  text: String
}
```

## Given GraphQL request

```graphql
{
  book(isbn: "978-123") {
    title
    author
    reviews(last: 2) {
      rating
      text
    }
  }
}
```

Answer the following:

```text
1. Convert this GraphQL request to REST.
2. Which HTTP method is used?
3. What are the endpoint names?
4. How many endpoints are needed in REST?
5. What is the possible JSON result?
6. What type of HTTP method is used?
7. In GraphQL, how many endpoints are used and why?
```
## Solution

## 1. GraphQL to REST migration

The GraphQL request asks for:

```text
One book by ISBN
+
its last 2 reviews
```

In REST, there are two possible designs.

### REST option A: separate endpoints

```http
GET /books/978-123
GET /books/978-123/reviews?last=2
```

This follows a resource-based REST style:

```text
/books/978-123              → one book
/books/978-123/reviews      → reviews of that book
```
### REST option B: aggregated endpoint

```http
GET /books/978-123
```

In this version, the `/books/978-123` endpoint returns the book together with reviews.

But this may cause **overfetching** if some clients need only book data and not reviews.
## 2. Which HTTP method is used?

```text
GET
```

Because the operation only reads data.

It does not create, update, or delete anything.
## 3. Name of endpoints

If using separate REST endpoints:

```http
/books/{isbn}
/books/{isbn}/reviews
```

Concrete example:

```http
/books/978-123
/books/978-123/reviews?last=2
```

The `last=2` part can be represented as a query parameter because it restricts the number of reviews.
## 4. Number of endpoints in REST

If relationships are separate:

```text
2 endpoints
```

They are:

```http
GET /books/978-123
GET /books/978-123/reviews?last=2
```

If using an aggregated REST endpoint:

```text
1 endpoint
```

It would be:

```http
GET /books/978-123
```

But then the endpoint must include reviews in the book response.
## 5. Possible JSON result

## GraphQL result

Because the GraphQL request selected:

```graphql
title
author
reviews {
  rating
  text
}
```

the response contains only those fields:

```json
{
  "data": {
    "book": {
      "title": "Learning Web APIs",
      "author": "A. Meyer",
      "reviews": [
        {
          "rating": 5,
          "text": "Very helpful for exam preparation."
        },
        {
          "rating": 4,
          "text": "Good explanations of REST and GraphQL."
        }
      ]
    }
  }
}
```

Notice that `isbn` and `year` are not returned because they were not requested.
## REST result with separate endpoints

First request:

```http
GET /books/978-123
```

Possible response:

```json
{
  "isbn": "978-123",
  "title": "Learning Web APIs",
  "author": "A. Meyer",
  "year": 2024
}
```

Second request:

```http
GET /books/978-123/reviews?last=2
```

Possible response:

```json
[
  {
    "id": "r8",
    "rating": 5,
    "text": "Very helpful for exam preparation."
  },
  {
    "id": "r9",
    "rating": 4,
    "text": "Good explanations of REST and GraphQL."
  }
]
```
## REST result with aggregated endpoint

```http
GET /books/978-123
```

Possible response:

```json
{
  "isbn": "978-123",
  "title": "Learning Web APIs",
  "author": "A. Meyer",
  "year": 2024,
  "reviews": [
    {
      "id": "r8",
      "rating": 5,
      "text": "Very helpful for exam preparation."
    },
    {
      "id": "r9",
      "rating": 4,
      "text": "Good explanations of REST and GraphQL."
    }
  ]
}
```

This returns more than the GraphQL request asked for, so it may cause overfetching.
## 6. Type of HTTP method

The HTTP method is:

```text
GET
```

Type:

```text
Safe: yes
Idempotent: yes
```

Why?

```text
Safe → GET does not change server resource state.
Idempotent → sending the same GET many times has the same effect as sending it once.
```
## 7. In GraphQL, how many endpoints are used and why?

```text
Number of GraphQL endpoints: 1
Endpoint: /graphql
```

The GraphQL request would be sent to:

```http
POST /graphql
```

with this body:

```graphql
{
  book(isbn: "978-123") {
    title
    author
    reviews(last: 2) {
      rating
      text
    }
  }
}
```

Why only one endpoint?

Because in GraphQL, the endpoint does not represent each resource separately. The request body specifies:

```text
which operation to execute
which object to access
which fields to return
which nested data to include
```

So these would all use the same endpoint:

```graphql
{
  books {
    title
  }
}
```

```graphql
{
  book(isbn: "978-123") {
    title
  }
}
```

```graphql
mutation {
  createBook(title: "API Design", author: "L. Smith") {
    isbn
    title
  }
}
```

All go to:

```http
POST /graphql
```
## Final exam answer in compact form

```text
GraphQL operation:
book(isbn: "978-123") with nested reviews(last: 2)

REST migration:
GET /books/978-123
GET /books/978-123/reviews?last=2

HTTP method:
GET

Endpoint names:
/books/{isbn}
/books/{isbn}/reviews

Number of REST endpoints:
2 if reviews are separate
1 if book response is aggregated with reviews

JSON result:
Book title + author + last 2 reviews

Type of HTTP method:
GET is safe and idempotent

GraphQL endpoints:
1 endpoint, usually /graphql, because the query body describes the operation and selected fields.
```

## Prompt

can there be an opposite questions

Yes. The **opposite question** can definitely come.

Instead of giving **GraphQL code and asking you to migrate to REST**, the exam can give you a **REST API design** and ask you to express it as **GraphQL schema + GraphQL query/mutation**.
## Opposite question type

## Given REST endpoints

```http
GET /books
GET /books/978-123
GET /books/978-123/reviews
POST /books
```

They may ask:

```text
1. Convert this REST API to GraphQL.
2. Write the GraphQL schema.
3. Write the GraphQL query for getting one book with reviews.
4. Write the GraphQL mutation for creating a book.
5. How many GraphQL endpoints are needed?
6. What JSON result will be returned?
```
## Example opposite exam question

## Question

A REST API exposes the following endpoints:

```http
GET /products
GET /products/{id}
GET /products/{id}/reviews
POST /products
```

A product has:

```text
id
name
price
description
reviews
```

A review has:

```text
id
rating
text
```

Convert this REST design into GraphQL.
## Solution

## 1. GraphQL schema

```graphql
type Query {
  products: [Product!]!
  product(id: ID!): Product
}

type Mutation {
  createProduct(
    name: String!
    price: Float!
    description: String
  ): Product!
}

type Product {
  id: ID!
  name: String!
  price: Float!
  description: String
  reviews: [Review]
}

type Review {
  id: ID!
  rating: Int!
  text: String
}
```
## 2. GraphQL query for all products

REST version:

```http
GET /products
```

GraphQL version:

```graphql
{
  products {
    id
    name
    price
  }
}
```

Possible result:

```json
{
  "data": {
    "products": [
      {
        "id": "1",
        "name": "Laptop",
        "price": 999.99
      },
      {
        "id": "2",
        "name": "Mouse",
        "price": 29.99
      }
    ]
  }
}
```
## 3. GraphQL query for one product

REST version:

```http
GET /products/1
```

GraphQL version:

```graphql
{
  product(id: "1") {
    id
    name
    price
    description
  }
}
```
## 4. GraphQL query for product with reviews

REST version may need:

```http
GET /products/1
GET /products/1/reviews
```

GraphQL version:

```graphql
{
  product(id: "1") {
    name
    price
    reviews {
      rating
      text
    }
  }
}
```

Here GraphQL can get the connected data in one request body.
## 5. GraphQL mutation for creating a product

REST version:

```http
POST /products
```

GraphQL version:

```graphql
mutation {
  createProduct(
    name: "Keyboard"
    price: 79.99
    description: "Mechanical keyboard"
  ) {
    id
    name
    price
  }
}
```

Possible result:

```json
{
  "data": {
    "createProduct": {
      "id": "3",
      "name": "Keyboard",
      "price": 79.99
    }
  }
}
```
## 6. Number of GraphQL endpoints

```text
Number of GraphQL endpoints: 1
Endpoint: /graphql
```

Why?

Because GraphQL does not create a separate endpoint for:

```text
/products
/products/{id}
/products/{id}/reviews
```

Instead, all requests go to:

```http
POST /graphql
```

and the request body decides what data is needed.
## How to recognize opposite questions

## GraphQL → REST question

They give:

```graphql
{
  product(id: "1") {
    name
    reviews {
      text
    }
  }
}
```

You answer with:

```http
GET /products/1
GET /products/1/reviews
```
## REST → GraphQL question

They give:

```http
GET /products/1/reviews
```

You answer with:

```graphql
{
  product(id: "1") {
    reviews {
      text
    }
  }
}
```
## Final exam memory

```text
REST → GraphQL:
Endpoints become fields and nested selections.

GraphQL → REST:
Fields and nested selections become resource endpoints.
```

Example:

```text
REST:
/products/1/reviews

GraphQL:
product(id: "1") {
  reviews {
    text
  }
}
```
