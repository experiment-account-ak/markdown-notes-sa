# Complete GraphQL Example

## Master Example for Lectures E04–E06

Use this as the complete example connecting all three lectures:

```text
E04: Why GraphQL?
Client requests exactly the required data
        ↓
E05: Schema
Server defines what data and operations exist
        ↓
E06: Requests
Client sends queries, mutations, or introspection requests
```

GraphQL treats data as a graph of connected objects.

In this example:

```text
Todo
└── Comment
```

A `Todo` can have several `Comment` objects.

The client selects only the required part of that graph.

# Part 1: The GraphQL Schema on the Server

```graphql
# Defines which types act as the API's entry points
schema {
  query: MyQueryType
  mutation: MyMutationType
}

# Root type for read operations
type MyQueryType {
  # Returns a non-null list containing non-null Todo objects
  todos: [Todo!]!

  # Returns one Todo identified by its mandatory ID
  todo(id: ID!): Todo
}

# Root type for write operations
type MyMutationType {
  # Creates a Todo
  # title is mandatory
  # text is optional
  # the returned Todo must not be null
  createTodo(
    title: String!
    text: String
  ): Todo!
}

# An object type representing a Todo
type Todo {
  # ID is a scalar type representing a unique identifier
  # ! means that the value must not be null
  id: ID!

  # A mandatory String
  title: String!

  # An optional String
  text: String

  # A value restricted to the TodoStatus enum
  status: TodoStatus!

  # A list of Comment objects
  # last is an optional argument used to limit the result
  comments(last: Int): [Comment]
}

# An object type representing a Comment
type Comment {
  id: ID!
  text: String!
}

# A fixed set of permitted values
enum TodoStatus {
  OPEN
  PENDING
  DONE
}
```

The schema is the server-side contract.

It defines:

- types;
- fields;
- relationships;
- query operations;
- mutation operations.

==★ **The schema defines what is possible.**==

# Part 2: Important Schema Syntax

## 1. `type`

```graphql
type Todo {
  title: String
}
```

The keyword `type` defines an object type.

Here:

- `Todo` is the type name.
- `title` is a field.
- `String` is the field’s type.

General syntax:

```graphql
type TypeName {
  fieldName: FieldType
}
```

## 2. Field syntax: `name: Type`

```graphql
title: String
```

Read this as:

```text
The field named title has the type String.
```

The colon separates the field name from its type:

```text
field name : field type
title      : String
```

## 3. `!` means non-null

```graphql
title: String!
```

The exclamation mark means that the value may not be `null`.

Allowed:

```json
{
  "title": "Learn GraphQL"
}
```

Not allowed:

```json
{
  "title": null
}
```

Compare this with:

```graphql
text: String
```

Because `text` has no `!`, it is optional and may be `null`.

## 4. Square brackets `[]` mean list

```graphql
comments: [Comment]
```

This means that `comments` returns a list of `Comment` objects.

Possible result:

```json
{
  "comments": [
    {
      "id": "1",
      "text": "First comment"
    },
    {
      "id": "2",
      "text": "Second comment"
    }
  ]
}
```

## 5. Understanding `[Todo!]!`

```graphql
todos: [Todo!]!
```

Read it from the inside outward:

```text
Todo
  ↓
One Todo object

Todo!
  ↓
An individual Todo may not be null

[Todo!]
  ↓
A list of non-null Todo objects

[Todo!]!
  ↓
The list itself may also not be null
```

Therefore:

```graphql
todos: [Todo!]!
```

means:

```text
Always return a list,
and none of its Todo elements may be null.
```

An empty list is still possible:

```json
{
  "todos": []
}
```

## 6. Field arguments

```graphql
comments(last: Int): [Comment]
```

This field accepts an argument.

```text
Argument name: last
Argument type: Int
Return type: [Comment]
```

General syntax:

```graphql
fieldName(argumentName: ArgumentType): ReturnType
```

A client can provide the argument like this:

```graphql
comments(last: 5) {
  text
}
```

Meaning:

```text
Return the last five comments
and select their text field.
```

GraphQL fields can behave more like functions than simple attributes.

## 7. `enum`

```graphql
enum TodoStatus {
  OPEN
  PENDING
  DONE
}
```

An enum defines a fixed range of permitted values.

A field using this enum:

```graphql
status: TodoStatus!
```

may contain:

```text
OPEN
PENDING
DONE
```

but not:

```text
FINISHED
```

unless that value is declared in the enum.

## 8. Root operation types

```graphql
schema {
  query: MyQueryType
  mutation: MyMutationType
}
```

This establishes the API entry points:

```text
MyQueryType    → read operations
MyMutationType → write operations
```

Every GraphQL request starts from a field of one of these root types.

A query type is required.

Mutation and subscription types are optional.

# Part 3: A Complete GraphQL Query

Suppose the client needs:

- each todo’s ID;
- title;
- status;
- the text of its last five comments.

```graphql
# Operation type: query
# Operation name: ListOfTodos
query ListOfTodos {
  # Root field from MyQueryType
  todos {
    # Scalar fields selected from Todo
    id
    title
    status

    # Nested object field with an argument
    comments(last: 5) {
      # Scalar field selected from Comment
      text
    }
  }
}
```

# Part 4: Query Syntax Explained

Complete structure:

```graphql
query ListOfTodos {
  todos {
    id
    title
    status
    comments(last: 5) {
      text
    }
  }
}
```

The structure can be separated into these parts:

```text
query
  ↓
operation type

ListOfTodos
  ↓
optional operation name

todos
  ↓
root field

{ id title status }
  ↓
selection set

comments(last: 5)
  ↓
field with an argument

{ text }
  ↓
nested selection set
```

## 1. Operation type

```graphql
query
```

GraphQL supports:

```graphql
query
mutation
subscription
```

Their meanings are:

```text
query        → read data
mutation     → change data
subscription → subscribe to changes
```

For a simple query, `query` can be omitted.

These requests are equivalent:

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

When the operation type is omitted, GraphQL uses `query` as the default.

## 2. Operation name

```graphql
ListOfTodos
```

In:

```graphql
query ListOfTodos {
```

`ListOfTodos` is the operation’s name.

It is optional, but useful for:

- debugging;
- logs;
- identifying requests;
- distinguishing different operations.

It is not a schema type or field.

It is a client-chosen name for the request.

## 3. Root field

```graphql
todos
```

This comes from the schema:

```graphql
type MyQueryType {
  todos: [Todo!]!
}
```

The relationship is:

```text
Schema                  Request
------                  -------
todos: [Todo!]!    →    todos { ... }
```

The request must begin with a field available through the relevant root type.

## 4. Selection set

```graphql
{
  id
  title
  status
}
```

A selection set specifies exactly which fields the client wants.

The client does not request:

```graphql
text
```

Therefore, the todo’s `text` field does not need to appear in the result.

```text
Requested fields   → returned
Unrequested fields → omitted
```

## 5. Nested selection

```graphql
comments(last: 5) {
  text
}
```

`comments` returns `Comment` objects rather than a final scalar value.

Therefore, another selection set is required:

```graphql
{
  text
}
```

Mental rule:

```text
Scalar field → selection ends
Object field → another selection set is required
```

For example:

```graphql
title
```

is enough because `title` is a `String`.

But this is incomplete:

```graphql
comments
```

The client must specify fields of the returned objects:

```graphql
comments {
  text
}
```

# Part 5: Expected Query Response

The runtime executes the query and commonly returns JSON:

```json
{
  "data": {
    "todos": [
      {
        "id": "42",
        "title": "Learn JavaScript",
        "status": "PENDING",
        "comments": [
          {
            "text": "Did nothing today."
          },
          {
            "text": "Good source: book by K. Simpson."
          }
        ]
      },
      {
        "id": "23",
        "title": "Learn GraphQL",
        "status": "OPEN",
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

The result is wrapped inside:

```json
{
  "data": {
  }
}
```

The structure reflects the query:

```text
QUERY       RESPONSE
-----       --------
todos   →   "todos"
id      →   "id"
title   →   "title"
status  →   "status"
comments→   "comments"
text    →   "text"
```

==★ **The response structure reflects the request structure.**==

# Part 6: Querying One Todo Using an Argument

The schema contains:

```graphql
type MyQueryType {
  todo(id: ID!): Todo
}
```

The client can supply the required `id` argument:

```graphql
query FindTodo {
  todo(id: "42") {
    id
    title
    text
    status
  }
}
```

Breakdown:

```text
query
  ↓
read operation

FindTodo
  ↓
operation name

todo
  ↓
root field

id: "42"
  ↓
argument name and supplied value

id, title, text, status
  ↓
selected return fields
```

Possible response:

```json
{
  "data": {
    "todo": {
      "id": "42",
      "title": "Learn JavaScript",
      "text": "I cannot ignore it any longer.",
      "status": "PENDING"
    }
  }
}
```

# Part 7: A Complete Mutation

A mutation performs a write operation.

The schema defines:

```graphql
type MyMutationType {
  createTodo(
    title: String!
    text: String
  ): Todo!
}
```

The client can create a todo using:

```graphql
# Operation type: mutation
# Operation name: AddTodo
mutation AddTodo {
  # Mutation root field
  createTodo(
    title: "Convert REST API to GraphQL"
    text: "Review lectures E04 to E06"
  ) {
    # Fields that should be returned after creation
    id
    title
    text
    status
  }
}
```

# Part 8: Mutation Syntax Explained

Complete mutation:

```graphql
mutation AddTodo {
  createTodo(
    title: "Convert REST API to GraphQL"
    text: "Review lectures E04 to E06"
  ) {
    id
    title
    text
    status
  }
}
```

## Operation type

```graphql
mutation
```

This tells the server that the request intends to change data.

Unlike a query, `mutation` should not be omitted because the default operation type is `query`.

## Operation name

```graphql
AddTodo
```

This optional name identifies the mutation.

## Mutation field

```graphql
createTodo
```

This field is declared in the mutation root:

```graphql
type MyMutationType {
  createTodo(...): Todo!
}
```

## Input arguments

```graphql
title: "Convert REST API to GraphQL"
text: "Review lectures E04 to E06"
```

The schema defines the expected argument types:

```graphql
title: String!
text: String
```

Therefore:

- `title` must be supplied because it is non-null.
- `text` may be omitted because it is nullable.

This is also valid:

```graphql
mutation {
  createTodo(title: "Learn GraphQL") {
    id
    title
  }
}
```

## Mutation return selection

```graphql
{
  id
  title
  text
  status
}
```

This does not describe the input.

It specifies which fields of the newly created todo should be returned.

The mutation means:

```text
Create a todo using these argument values
          +
Return these fields of the created object
```

GraphQL mutations can perform an operation and return client-selected data.

# Part 9: Expected Mutation Response

```json
{
  "data": {
    "createTodo": {
      "id": "123",
      "title": "Convert REST API to GraphQL",
      "text": "Review lectures E04 to E06",
      "status": "OPEN"
    }
  }
}
```

The server may generate fields that the client did not provide, such as:

```json
"id": "123"
```

The client receives it because `id` was included in the mutation’s return selection.

# Part 10: Introspection Example

GraphQL allows a client to inspect the schema itself.

## Inspect the `Todo` type

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

Syntax:

```text
__type
  ↓
special introspection meta-field

name: "Todo"
  ↓
argument identifying the type

name
  ↓
request the type's name

description
  ↓
request its description

fields { name }
  ↓
request the names of its fields
```

Possible response:

```json
{
  "data": {
    "__type": {
      "name": "Todo",
      "description": "A type representing a todo.",
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
          "name": "status"
        },
        {
          "name": "comments"
        }
      ]
    }
  }
}
```

Introspection is comparable to reflection in Java.

It enables tools such as:

- documentation explorers;
- schema browsers;
- editors with code completion.

# Part 11: Inspect All Available Type Names

```graphql
{
  __schema {
    types {
      name
    }
  }
}
```

Read it as:

```text
__schema
  ↓
Access the complete schema

types
  ↓
Access its types

name
  ↓
Return the name of every type
```

Possible partial result:

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
        },
        {
          "name": "TodoStatus"
        }
      ]
    }
  }
}
```

# Part 12: Complete Request Through `/graphql`

The lecture presents GraphQL requests as being sent to an endpoint such as:

```http
POST /graphql
Content-Type: application/json
```

The request body can contain the GraphQL operation:

```json
{
  "query": "query ListOfTodos { todos { id title } }"
}
```

The important concept is:

```text
The endpoint remains /graphql
        ↓
The GraphQL request determines
which operation and data are required
```

# Final Syntax Map

## Request syntax

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

| Syntax | Meaning |
|---|---|
| `query` | Read operation |
| `ListOfTodos` | Optional operation name |
| `{ ... }` | Selection set |
| `todos` | Root field |
| `id`, `title` | Scalar fields |
| `comments` | Object/list field |
| `(last: 5)` | Argument with a supplied value |
| `comments { text }` | Nested selection |
| `# comment` | GraphQL line comment |

## Schema syntax

| Syntax | Meaning |
|---|---|
| `type Todo` | Defines an object type |
| `title: String` | Field named `title` of type `String` |
| `String!` | Non-null string |
| `[Comment]` | List of comments |
| `[Comment!]!` | Non-null list of non-null comments |
| `enum` | Fixed set of values |
| `schema` | Connects root operation types |
| `query: MyQueryType` | Defines the query entry point |
| `mutation: MyMutationType` | Defines the mutation entry point |

# One Complete Flow to Remember

```text
Schema:
todos: [Todo!]!
        ↓
Client query:
todos {
  title
  comments {
    text
  }
}
        ↓
Runtime validates and executes it
        ↓
Response:
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

# Key Points to Remember

==★ **The schema defines what is possible.**==

==★ **The request selects what is currently needed.**==

==★ **The runtime validates and executes the request.**==

==★ **The response mirrors the client’s selection.**==
