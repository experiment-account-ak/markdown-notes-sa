# Lecture E05: GraphQL Schema

## Combined Mental Model

Continue the restaurant analogy:

- The **schema** is the restaurant’s menu.
- **Types and fields** are the available dishes and their properties.
- A **query** asks to read information.
- A **mutation** asks the kitchen to create or change something.
- A **subscription** asks to be informed when something changes.
- The **runtime environment** is the kitchen that validates and prepares the order.
- A **request** is the customer’s order slip.
- A **response** is the returned food, structured as requested.
- **Introspection** asks the restaurant to describe its menu.

The complete flow is:

```text
Server defines a schema
          ↓
Schema describes types, fields, relationships, and operations
          ↓
Client sends a request that follows the schema
          ↓
Runtime validates and executes the request
          ↓
Server returns a JSON result shaped like the request
```

## Objective

A GraphQL server cannot understand arbitrary requests.

It first needs a formal description of:

- which data exists;
- how that data is structured;
- how objects relate to one another;
- which operations clients are allowed to perform.

That formal description is the **GraphQL schema**.

GraphQL provides an **Interface Definition Language**, or **IDL**, for writing the schema.

# 1. Where Does the Schema Belong?

The schema belongs primarily to the server side.

```text
Client                         Server
------                         ------
Writes requests        →       Schema defines what is valid
                               Runtime executes valid requests
```

For example, a client might send:

```graphql
{
  todos {
    title
  }
}
```

Before the server can execute this, it must know:

- Is there a root field called `todos`?
- Does `todos` return `Todo` objects?
- Does a `Todo` have a field called `title`?
- What type of value is `title`?

The schema answers these questions.

# 2. What Does a GraphQL Schema Define?

A schema defines:

1. Supported data types
2. The structure of those types
3. Relationships between types
4. Supported operations

GraphQL separates operations into three categories:

| Operation | Purpose |
|---|---|
| Query | Read data |
| Mutation | Create, update, or delete data |
| Subscription | Subscribe to changes or events |

A simple interpretation is:

```text
Query         → "Give me data."
Mutation      → "Change data."
Subscription  → "Inform me when data changes."
```

# 3. The GraphQL Type System

GraphQL provides a type system for describing the API.

The lecture lists:

- scalar types;
- object types;
- enumerations;
- query types;
- mutation types;
- subscription types;
- interfaces;
- union types;
- directives.

The lecture mainly focuses on:

```text
Scalar types
Object types
Enumerations
Query, mutation, and subscription types
```

Interfaces, union types, and directives are mentioned but not explained in detail.

# 4. Scalar Types

A scalar is a basic value that cannot be divided into further GraphQL fields.

GraphQL provides these standard scalar types:

| Scalar | Meaning |
|---|---|
| `Int` | Signed 32-bit integer |
| `Float` | 64-bit double-precision floating-point number |
| `String` | Sequence of UTF-8 characters |
| `Boolean` | `true` or `false` |
| `ID` | Unique identifier, represented similarly to a string |

Examples:

```graphql
id: ID
title: String
numberOfComments: Int
estimatedHours: Float
done: Boolean
```

Possible values:

```text
id               → "42"
title            → "Learn GraphQL"
numberOfComments → 3
estimatedHours   → 2.5
done             → false
```

## Why Are Scalars Called the Leaves of the Graph?

Objects can lead to other objects, but scalar values are normally the final values selected by a request.

```text
Todo
├── title → String
└── comments
    └── Comment
        └── text → String
```

`Todo` and `Comment` are objects through which the query can continue.

`title` and `text` are scalar values. The selection ends there.

==★ **Objects form the structure of the graph; scalar values form its leaves.**==

# 5. Object Types

An object type is defined using the keyword `type`.

General structure:

```graphql
type Name {
  fieldName: FieldType
}
```

Example:

```graphql
type Todo {
  title: String
}
```

This defines:

- an object type named `Todo`;
- a field called `title`;
- a value of type `String`.

# 6. Complete `Todo` Object Type

```graphql
type Todo {
  # Field with name 'id' and type 'ID', must not be null
  id: ID!

  title: String!

  text: String

  # Field with name 'comments' as list of Comment objects
  comments: [Comment]
}
```

## `type Todo`

```graphql
type Todo {
```

This defines an object type named `Todo`.

A returned todo could conceptually look like:

```json
{
  "id": "42",
  "title": "Learn GraphQL",
  "text": "Study the schema",
  "comments": []
}
```

## Schema comments

```graphql
# Field with name 'id' and type 'ID', must not be null
```

A line beginning with `#` is a comment.

Comments are ignored during execution and are used to explain the schema.

## Non-null ID

```graphql
id: ID!
```

This field has:

- name: `id`;
- type: `ID`;
- `!`: the field may not be `null`.

Valid:

```json
{
  "id": "42"
}
```

Invalid according to this schema:

```json
{
  "id": null
}
```

The `!` means the value is non-nullable.

## Non-null title

```graphql
title: String!
```

Every `Todo` must have a non-null title.

Valid:

```json
{
  "title": "Learn GraphQL"
}
```

Not permitted:

```json
{
  "title": null
}
```

## Nullable text

```graphql
text: String
```

There is no `!`, so the field may contain a string or `null`.

Both are valid:

```json
{
  "text": "Read the GraphQL documentation"
}
```

```json
{
  "text": null
}
```

This can represent an optional description.

## List of comments

```graphql
comments: [Comment]
```

Square brackets indicate a list.

This means that `comments` contains a list of `Comment` objects.

Example:

```json
{
  "comments": [
    {
      "text": "First comment"
    },
    {
      "text": "Second comment"
    }
  ]
}
```

Because neither the list nor its elements are marked with `!`, this definition is comparatively permissive.

It can potentially allow:

```graphql
comments: null
```

and possibly nullable elements inside the list.

# 7. Understanding Lists and `!`

The placement of `!` is important.

## Nullable list with nullable elements

```graphql
comments: [Comment]
```

Possible:

```text
null
[]
[Comment, Comment]
[Comment, null]
```

## Nullable list with non-null elements

```graphql
comments: [Comment!]
```

Possible:

```text
null
[]
[Comment, Comment]
```

Not possible:

```text
[Comment, null]
```

## Non-null list with nullable elements

```graphql
comments: [Comment]!
```

Possible:

```text
[]
[Comment, Comment]
[Comment, null]
```

Not possible:

```text
null
```

## Non-null list with non-null elements

```graphql
comments: [Comment!]!
```

Possible:

```text
[]
[Comment, Comment]
```

Not possible:

```text
null
[Comment, null]
```

## Important technical detail

The lecture later uses:

```graphql
todos: [Todo!]!
```

This guarantees:

- the list itself is not `null`;
- no `Todo` inside the list is `null`.

It does **not** guarantee that the list contains at least one todo.

An empty list is still possible:

```json
{
  "todos": []
}
```

# 8. Fields Can Have Arguments

A field does not always behave like a simple Java attribute.

It can accept arguments that influence the returned value.

General syntax:

```graphql
fieldName(
  argumentName1: ArgumentType1
  argumentName2: ArgumentType2
): FieldType
```

Several arguments may optionally be separated using commas:

```graphql
field(first: Int, offset: Int): SomeType
```

Arguments can filter, limit, or otherwise refine returned data.

# 9. Field Argument Example

```graphql
type Todo {
  comments(last: Int): [Comment]
}
```

The field is:

```graphql
comments
```

Its optional argument is:

```graphql
last: Int
```

Its return type is:

```graphql
[Comment]
```

A client could request:

```graphql
comments(last: 5) {
  text
}
```

Meaning:

```text
Return only the last five comments,
and return the text field of each comment.
```

Because `last` is defined as:

```graphql
last: Int
```

and not:

```graphql
last: Int!
```

the argument is optional.

Both requests may therefore be permitted:

```graphql
comments {
  text
}
```

```graphql
comments(last: 5) {
  text
}
```

# 10. Enumeration Types

An enumeration, or enum, defines a fixed set of allowed values.

```graphql
enum TodoStatus {
  OPEN
  PENDING
  DONE
}
```

A field using this type could be defined as:

```graphql
status: TodoStatus
```

The field can then use one of the predefined values:

```text
OPEN
PENDING
DONE
```

A value outside this set is invalid:

```text
CANCELLED
```

unless it is added to the enum.

Enums are useful when a value must belong to a controlled set rather than accepting any arbitrary string.

Using:

```graphql
status: String
```

could allow spelling variations:

```text
"done"
"Done"
"finished"
"complete"
```

Using:

```graphql
status: TodoStatus
```

restricts the value to the declared alternatives.

# 11. Root Operation Types

Query, mutation, and subscription types are special object types that serve as entry points into the GraphQL API.

Every request starts from one of these root types.

```text
Query         → starting point for reading
Mutation      → starting point for writing
Subscription  → starting point for subscriptions
```

A GraphQL schema:

- must define a query type;
- may define a mutation type;
- may define a subscription type.

A read-only API might have only a query type.

An API supporting reads and writes might have query and mutation types.

# 12. Complete Root Type Example

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
```

## Schema declaration

```graphql
schema {
  query: MyQueryType
  mutation: MyMutationType
}
```

This states:

- read requests begin at `MyQueryType`;
- write requests begin at `MyMutationType`;
- no subscription root type is declared.

```text
Read entrance   → MyQueryType
Write entrance  → MyMutationType
```

## Query root type

```graphql
type MyQueryType {
  todos: [Todo!]!
}
```

This defines a root field named:

```graphql
todos
```

Its return type is:

```graphql
[Todo!]!
```

Meaning:

- the returned list is non-null;
- every `Todo` inside it is non-null;
- the list may still be empty.

A client can start a read request with:

```graphql
{
  todos {
    id
    title
  }
}
```

## Mutation root type

```graphql
type MyMutationType {
  createTodo(title: String!, text: String): Todo!
}
```

This defines a write operation called:

```graphql
createTodo
```

It has two arguments:

```graphql
title: String!
text: String
```

Meaning:

- `title` is required;
- `text` is optional.

Its return type is:

```graphql
Todo!
```

A valid operation could be:

```graphql
mutation {
  createTodo(
    title: "Learn GraphQL"
    text: "Read the schema lecture"
  ) {
    id
    title
    text
  }
}
```

# 13. Standard Root Type Names

The explicit schema declaration can be omitted when the standard names are used:

```text
Query
Mutation
Subscription
```

Instead of:

```graphql
schema {
  query: MyQueryType
  mutation: MyMutationType
}
```

the schema could use:

```graphql
type Query {
  todos: [Todo!]!
}

type Mutation {
  createTodo(title: String!, text: String): Todo!
}
```

GraphQL recognizes `Query` and `Mutation` as standard root type names.

# 14. Schema Versus Runtime Environment

The schema is a description or contract.

It says:

```text
A Todo has these fields.
This query is available.
This mutation accepts these arguments.
This operation returns this type.
```

But the schema alone does not fetch data or create objects.

A runtime environment is required to:

1. receive a request;
2. validate it against the schema;
3. execute it;
4. obtain the data;
5. return the result.

```text
Schema   → "What is allowed?"
Runtime  → "How is it executed?"
```

The schema itself is independent of a particular programming language.

A runtime could be implemented using Java, JavaScript, or another supported language while exposing the same conceptual schema.

# E05 Lecture Map

```text
GraphQL server needs to understand client requests
          ↓
The server exposes a schema
          ↓
Schema defines types, fields, and relationships
          ↓
Scalar types form final values
          ↓
Object types connect values and other objects
          ↓
Enums restrict values to a predefined set
          ↓
Root types define possible operations
          ↓
Runtime validates and executes operations
```

# Exam-Ready Questions

## 1. Why does a GraphQL server need a schema?

The runtime needs to know the structure and relationships of the data and which operations are supported so that it can validate and execute client requests.

## 2. What does the schema define?

It defines data types, fields, relationships, and the available query, mutation, and subscription operations.

## 3. What are GraphQL’s standard scalar types?

```text
Int
Float
String
Boolean
ID
```

## 4. Why are scalar types the leaves of the GraphQL graph?

They are final values such as strings and numbers and do not contain further selectable GraphQL fields.

## 5. What does `!` mean?

It marks a value as non-nullable.

```graphql
title: String!
```

means `title` may not be `null`.

## 6. What do square brackets mean?

They represent a list.

```graphql
comments: [Comment]
```

means a list of `Comment` objects.

## 7. What does `[Todo!]!` mean?

The list may not be `null`, and its elements may not be `null`. It can still be empty.

## 8. What are field arguments used for?

They refine or parameterize the value returned by a field.

```graphql
comments(last: 5)
```

requests the last five comments.

## 9. What is an enum?

A type with a fixed set of allowed values.

```graphql
enum TodoStatus {
  OPEN
  PENDING
  DONE
}
```

## 10. What are root operation types?

They are the starting points for requests:

```text
query        → reads
mutation     → writes
subscription → event-based updates
```

## 11. Which root type is mandatory?

A query root type is mandatory.

Mutation and subscription types are optional.

# Key Points to Remember

==★ **The schema is the server’s typed contract.**==

==★ **Scalar types are final values, while object types connect the graph.**==

==★ **Root operation types define where requests begin.**==

==★ **The schema says what is allowed; the runtime executes it.**==
