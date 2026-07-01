# Lecture E06: GraphQL Requests

## Objective

Once the schema and runtime are available, clients can send requests to the API.

The GraphQL request language uses a brace-based, JSON-like structure.

The server-side runtime commonly returns the result as JSON.

# 1. Relationship Between Schema and Request

The schema defines what is possible:

```graphql
type MyQueryType {
  todos: [Todo!]!
}

type Todo {
  id: ID!
  title: String!
  text: String
  comments(last: Int): [Comment]
}
```

The request selects from those possibilities:

```graphql
{
  todos {
    id
    title
  }
}
```

A useful distinction is:

```text
Schema:
The server's complete available vocabulary

Request:
The client's sentence written using that vocabulary
```

A request cannot correctly select fields that do not exist in the schema.

For example, this would fail if `price` is not a field of `Todo`:

```graphql
{
  todos {
    price
  }
}
```

# 2. Basic Structure of a GraphQL Request

Complete basic example:

```graphql
query ListOfTodos {
  todos {
    id
    title
  }
}
```

This contains four important elements:

1. operation type;
2. operation name;
3. root field;
4. selection set.

# 3. Operation Type

```graphql
query
```

The permitted operation types are:

| Operation | Purpose |
|---|---|
| `query` | Read data |
| `mutation` | Change data |
| `subscription` | Subscribe to events or changes |

In:

```graphql
query ListOfTodos {
```

the operation type is `query`, so the request reads data.

## Can `query` be omitted?

Yes.

When no operation type is written, GraphQL treats the request as a query.

These are equivalent for a simple single query:

```graphql
query {
  todos {
    id
    title
  }
}
```

```graphql
{
  todos {
    id
    title
  }
}
```

The default operation type is `query`.

# 4. Operation Name

```graphql
ListOfTodos
```

The complete opening is:

```graphql
query ListOfTodos {
```

`ListOfTodos` is the name of the request.

It is optional:

```graphql
query {
  todos {
    id
    title
  }
}
```

The name does not refer to a field in the schema.

It identifies this client operation.

It is useful for:

- debugging;
- logging;
- identifying requests in developer tools;
- distinguishing several operations.

A named operation communicates more clearly when examining logs.

# 5. Root Field

```graphql
todos
```

The root field is the entry point into the request.

In the schema:

```graphql
type MyQueryType {
  todos: [Todo!]!
}
```

the query root type provides the field:

```graphql
todos
```

Therefore, the client can begin with:

```graphql
query ListOfTodos {
  todos {
    ...
  }
}
```

The connection is:

```text
Schema root field     Client request
-----------------     --------------
todos: [Todo!]!   →   todos { ... }
```

# 6. Selection Set

```graphql
{
  id
  title
}
```

A selection set defines which fields should be returned.

In:

```graphql
query ListOfTodos {
  todos {
    id
    title
  }
}
```

the client requests exactly two fields for each todo:

```text
id
title
```

It does not request:

```text
text
comments
```

Therefore, those fields do not appear in the result.

This mechanism allows GraphQL clients to avoid receiving unneeded fields.

# 7. Complete Basic Query Explained

```graphql
query ListOfTodos {
  todos {
    id
    title
  }
}
```

Read it as:

```text
query
  ↓
Perform a read operation.

ListOfTodos
  ↓
Name this client operation "ListOfTodos".

todos
  ↓
Begin with the todos field of the query root type.

id
title
  ↓
Return only these fields for every Todo.
```

# 8. Hierarchical and Nested Requests

GraphQL requests can follow relationships between object types.

```graphql
query ListOfTodos {
  todos {
    id
    title
    comments {
      text
    }
  }
}
```

The structure is hierarchical:

```text
todos
├── id
├── title
└── comments
    └── text
```

The request moves:

1. from the query root;
2. to `todos`;
3. from each todo to its comments;
4. from each comment to its text.

This nesting must follow the relationships defined in the schema.

For example:

```graphql
type Todo {
  comments: [Comment]
}

type Comment {
  text: String
}
```

allows:

```graphql
todos {
  comments {
    text
  }
}
```

# 9. Why Do Object Fields Need Nested Selections?

Consider:

```graphql
comments: [Comment]
```

`comments` returns objects, not a final scalar value.

Therefore, the client must specify which fields of each `Comment` it needs:

```graphql
comments {
  text
}
```

By contrast, `title` is already a scalar:

```graphql
title: String
```

So the client writes only:

```graphql
title
```

not:

```graphql
title {
  ...
}
```

Mental rule:

```text
Scalar field → selection ends
Object field → open another selection set
```

# 10. Arguments in Requests

Arguments defined in the schema can be supplied by the client.

Schema:

```graphql
type Todo {
  comments(last: Int): [Comment]
}
```

Request:

```graphql
query ListOfTodos {
  todos {
    id
    title
    comments(last: 5) {
      text
    }
  }
}
```

The argument is:

```graphql
last: 5
```

This asks the server to return only the last five comments.

```text
Schema definition:
comments(last: Int): [Comment]

Client value:
comments(last: 5)
```

The schema declares the argument’s name and type.

The request supplies its concrete value.

# 11. Query with Optional Elements Omitted

Request:

```graphql
{
  todos {
    id
    title
  }
}
```

This is still a query because `query` is the default operation type.

Result:

```json
{
  "data": {
    "todos": [
      {
        "id": "42",
        "title": "Learn JavaScript"
      },
      {
        "id": "23",
        "title": "Look at GraphQL"
      }
    ]
  }
}
```

The lecture sometimes uses an ellipsis such as:

```text
{ ... }
```

That ellipsis is explanatory and is not literal valid JSON.

# 12. Why Is the Result Wrapped in `data`?

Requested fields are returned inside:

```json
{
  "data": {
    "todos": []
  }
}
```

Inside `data`, the response follows the selection structure:

```text
Request       Result
-------       ------
todos     →   "todos"
id        →   "id"
title     →   "title"
```

The response does not include unrequested fields.

# 13. The Result Reflects the Request Structure

Request:

```graphql
{
  todos {
    id
    title
  }
}
```

Result shape:

```json
{
  "data": {
    "todos": [
      {
        "id": "...",
        "title": "..."
      }
    ]
  }
}
```

The schema tells us that `todos` returns a list, so the result contains a JSON array:

```json
"todos": []
```

The fields inside each todo correspond to the selection set.

# 14. Clients Can Change Their Selection

The next request changes both fields and order:

```graphql
{
  todos {
    text
    title
    id
  }
}
```

Result:

```json
{
  "data": {
    "todos": [
      {
        "text": "Lorem ipsum...",
        "title": "Learn JavaScript",
        "id": "42"
      },
      {
        "text": "Dolor sit amet...",
        "title": "Look at GraphQL",
        "id": "23"
      }
    ]
  }
}
```

The client now requests:

```text
text
title
id
```

Therefore, each returned todo contains those three fields.

==★ **The client can adapt the response by changing its selection without requiring a new REST-style endpoint.**==

Different clients can use the same GraphQL API:

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
  todos {
    text
    title
    id
  }
}
```

# 15. Nested Query Example

Request:

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

Result:

```json
{
  "data": {
    "todos": [
      {
        "title": "Learn JavaScript",
        "comments": [
          {
            "text": "Done nothing today."
          },
          {
            "text": "Good source: book by K. Simpson."
          }
        ]
      },
      {
        "title": "Look at GraphQL",
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

The nesting corresponds directly:

```text
Request       Result
-------       ------
todos     →   "todos"
title     →   "title"
comments  →   "comments"
text      →   "text"
```

The client obtains connected todo and comment data in one request.

# 16. Query Versus Mutation

A query reads existing information:

```graphql
{
  todos {
    id
    title
  }
}
```

A mutation changes data:

```graphql
mutation {
  createTodo(
    title: "Convert REST-API to GraphQL"
    text: "Lorem ipsum..."
  ) {
    id
    title
    text
  }
}
```

The operation type must be written for the mutation:

```graphql
mutation
```

Without it, the default would be a query.

# 17. Complete Mutation Example

Request:

```graphql
mutation {
  createTodo(
    title: "Convert REST-API to GraphQL"
    text: "Lorem ipsum..."
  ) {
    id
    title
    text
  }
}
```

Result:

```json
{
  "data": {
    "createTodo": {
      "id": "123",
      "title": "Convert REST-API to GraphQL",
      "text": "Lorem ipsum..."
    }
  }
}
```

## What does `createTodo` do?

The schema defines:

```graphql
createTodo(title: String!, text: String): Todo!
```

The mutation supplies:

```graphql
title: "Convert REST-API to GraphQL"
text: "Lorem ipsum..."
```

The server creates a todo using those values.

Because `title` is:

```graphql
String!
```

it is mandatory.

Because `text` is:

```graphql
String
```

it is optional.

## What is the selection set after the mutation?

```graphql
{
  id
  title
  text
}
```

A mutation does not merely tell the server what to change.

It can also specify which fields of the changed object should be returned.

This mutation means:

```text
Create a todo with this title and text,
then return its id, title, and text.
```

The server might generate the ID:

```json
"id": "123"
```

The client did not provide this ID, but requested it in the result.

The client could request fewer return fields:

```graphql
mutation {
  createTodo(title: "Learn GraphQL") {
    id
  }
}
```

Conceptually, the server would then return only the new todo’s ID.

# 18. Further Request-Language Possibilities

The lecture mentions additional GraphQL features without explaining them in detail.

## Fragments

Fragments allow repeated selections to be reused.

```text
Define a common set of Todo fields once
and use it in multiple places.
```

## Variables

Variables allow dynamic, parameterized requests.

```text
Write one mutation structure
and supply different title values at runtime.
```

## Directives

Directives can conditionally affect field selection or execution.

```text
Include this field only when a condition is true.
```

# 19. Introspection

Introspection allows clients to ask the GraphQL API about its own schema.

It is comparable to reflection in Java.

With introspection, a client can discover:

- which types exist;
- which fields a type contains;
- descriptions of types;
- available operations;
- argument information.

It makes dynamic tools possible, such as:

- request editors with code completion;
- automatically generated documentation;
- schema explorers;
- tools that validate queries while they are written.

# 20. Introspection Meta-Fields

Two important meta-fields are:

```graphql
__schema
```

and:

```graphql
__type(name: String!)
```

They begin with two underscores:

```text
__
```

These are special fields used to inspect the schema.

## `__schema`

```graphql
__schema
```

provides access to the overall schema.

It can be used to inspect all available types and other schema information.

## `__type`

```graphql
__type(name: String!)
```

provides information about one named type.

The argument:

```graphql
name: String!
```

is required.

For example:

```graphql
__type(name: "Todo")
```

asks for information about the `Todo` type.

# 21. Introspection Example 1: List All Type Names

Request:

```graphql
{
  __schema {
    types {
      name
    }
  }
}
```

Read this as:

```text
Access the schema
        ↓
Access all types
        ↓
Return the name of every type
```

Result:

```json
{
  "data": {
    "__schema": {
      "types": [
        {
          "name": "Boolean"
        },
        {
          "name": "Comment"
        },
        {
          "name": "ID"
        },
        {
          "name": "MyMutationType"
        },
        {
          "name": "MyQueryType"
        },
        {
          "name": "String"
        },
        {
          "name": "Todo"
        }
      ]
    }
  }
}
```

This includes:

- user-defined types such as `Todo` and `Comment`;
- root types such as `MyQueryType`;
- standard scalar types such as `Boolean`, `ID`, and `String`;
- potentially additional standard or meta-types.

# 22. Introspection Example 2: Inspect `Todo`

Request:

```graphql
{
  __type(name: "Todo") {
    name
    description
    fields {
      name
    }
  }
}
```

This asks for:

- the type’s name;
- its description;
- all its fields;
- the name of every field.

Result:

```json
{
  "data": {
    "__type": {
      "name": "Todo",
      "description": "A type for ToDos.",
      "fields": [
        {
          "name": "id"
        },
        {
          "name": "title"
        },
        {
          "name": "text"
        },
        {
          "name": "comments"
        }
      ]
    }
  }
}
```

The result tells the client that the `Todo` type contains:

```text
id
title
text
comments
```

This information can be used by a development tool to suggest valid fields.

# 23. Public Example APIs Mentioned

The lecture mentions public GraphQL APIs for experimentation:

- BahnQL for Deutsche Bahn-related services;
- the official GitHub GraphQL API;
- a GraphQL wrapper for the Star Wars API;
- the Rick and Morty API.

They are examples only; their internal details are outside the lecture’s scope.

# E06 Lecture Map

```text
Schema and runtime already exist
          ↓
Client writes a request
          ↓
Operation type says query, mutation, or subscription
          ↓
Optional operation name identifies the request
          ↓
Root field selects an API entry point
          ↓
Selection set chooses exact fields
          ↓
Nested selections follow object relationships
          ↓
Arguments refine fields
          ↓
Runtime executes the request
          ↓
JSON response reflects the request structure
```

# Combined Example: Schema to Request to Response

## Step 1: Server schema

```graphql
schema {
  query: MyQueryType
  mutation: MyMutationType
}

type MyQueryType {
  todos: [Todo!]!
}

type MyMutationType {
  createTodo(title: String!, text: String): Todo!
}

type Todo {
  id: ID!
  title: String!
  text: String
  comments(last: Int): [Comment]
}

type Comment {
  text: String
}
```

This describes what the server permits.

## Step 2: Client read request

```graphql
query ListOfTodos {
  todos {
    id
    title
    comments(last: 5) {
      text
    }
  }
}
```

This follows the schema:

```text
MyQueryType.todos
        ↓
Todo.id
Todo.title
Todo.comments(last: Int)
        ↓
Comment.text
```

## Step 3: Returned JSON

```json
{
  "data": {
    "todos": [
      {
        "id": "42",
        "title": "Learn GraphQL",
        "comments": [
          {
            "text": "Read the schema chapter."
          }
        ]
      }
    ]
  }
}
```

## Step 4: Client write request

```graphql
mutation {
  createTodo(
    title: "Prepare for exam"
    text: "Review GraphQL requests"
  ) {
    id
    title
    text
  }
}
```

This follows:

```graphql
createTodo(title: String!, text: String): Todo!
```

# Most Important Distinction Between E05 and E06

| E05: Schema | E06: Request |
|---|---|
| Written for the server/API contract | Written by the client |
| Defines everything that is possible | Selects what is needed now |
| Defines field names and types | Supplies fields and argument values |
| Defines query and mutation entry points | Starts from those entry points |
| Used to validate requests | Must conform to the schema |
| Describes the complete graph | Selects a subgraph |

The shortest useful mental model is:

```text
Schema  = available possibilities
Request = one selection from those possibilities
```

# Exam-Ready Questions

## 12. What are the basic parts of a GraphQL request?

- operation type;
- optional operation name;
- root field;
- selection set.

## 13. What is the default operation type?

```text
query
```

## 14. What is a selection set?

The set of fields that the client wants returned.

## 15. How are relationships requested?

By nesting selections.

```graphql
todos {
  comments {
    text
  }
}
```

## 16. What is the difference between a query and a mutation?

A query reads data.

A mutation changes data and can return selected fields of the changed object.

## 17. Why does a mutation also have a selection set?

It allows the client to specify which fields of the created or changed object should be returned.

## 18. What is introspection?

It is the ability to query the GraphQL schema itself, comparable to reflection in Java.

## 19. Which meta-fields are introduced for introspection?

```graphql
__schema
```

and:

```graphql
__type(name: String!)
```

## 20. What is the relationship between a request and its result?

The hierarchical structure of the result generally reflects the hierarchical structure of the request.

# Final Takeaway

==★ **The schema is the server’s typed contract describing the available graph and operations.**==

==★ **A request follows that contract to select or modify specific data.**==

==★ **The runtime returns a JSON response whose structure reflects the client’s selection.**==
