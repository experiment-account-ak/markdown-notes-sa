# GraphQL Types: Scalars, Enums, Lists, and Non-Null

## Objective

Understand four important GraphQL type concepts:

1. **Scalar types** represent basic individual values.
2. **Enumeration types** restrict a field to a predefined set of values.
3. **List types** allow a field to contain multiple values or objects.
4. The exclamation mark `!` makes a value **non-null**.

## Mental model

A GraphQL schema can be viewed as a structured form:

- A scalar type determines the kind of value allowed in one field.
- An enum type provides a fixed list of permitted choices.
- A list type allows multiple entries in one field.
- `!` determines whether a value may be `null`.

For example, a product may contain:

```text
Name: text
Price: decimal number
Inventory: whole number
Status: ONSALE or SOLDOUT
Stores: multiple store objects
```

# 1. Scalar Types

A scalar type represents a single basic value.

GraphQL provides several built-in scalar types, so they do not need to be defined manually.

The correct term is **scalar type**, not “Scala type.” Scala is a separate programming language.

## Built-in GraphQL scalar types

| Scalar type | Meaning | Example |
|---|---|---|
| `Int` | A whole number | `10` |
| `Float` | A number that may include a decimal part | `52.99` |
| `String` | Text or a sequence of characters | `"Widget 54"` |
| `Boolean` | A logical value | `true` or `false` |
| `ID` | A unique identifier | `"a92bc31"` |

## Scalar fields in an object type

```graphql
type Product {
  id: ID
  name: String
  description: String
  price: Float
  inventory: Int
}
```

This definition states that:

- `id` contains an identifier.
- `name` contains text.
- `description` contains text.
- `price` contains a number that may contain decimals.
- `inventory` contains a whole number.

A matching JavaScript object could be:

```js
{
  id: "abc123",
  name: "Widget 54",
  description: "A useful garden widget",
  price: 52.99,
  inventory: 10
}
```

## Adding an inventory field

The number of available products can be represented using an integer:

```graphql
inventory: Int
```

The field should be added to the output type:

```graphql
type Product {
  id: ID
  name: String
  description: String
  price: Float
  inventory: Int
}
```

It should also be added to the input type when clients are allowed to submit it:

```graphql
input ProductInput {
  name: String
  description: String
  price: Float
  inventory: Int
}
```

The JavaScript class or object must also store the value:

```js
class Product {
  constructor(id, { name, description, price, inventory }) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.price = price;
    this.inventory = inventory;
  }
}
```

## Example mutation using scalar types

```graphql
mutation {
  createProduct(
    input: {
      name: "Widget 54"
      description: "A useful garden widget"
      price: 52.99
      inventory: 10
    }
  ) {
    id
    name
    price
    inventory
  }
}
```

Possible response:

```json
{
  "data": {
    "createProduct": {
      "id": "abc123",
      "name": "Widget 54",
      "price": 52.99,
      "inventory": 10
    }
  }
}
```

GraphQL checks that each submitted value matches its declared type.

For example, this is valid:

```graphql
inventory: 10
```

This is invalid:

```graphql
inventory: "ten"
```

The value `"ten"` is a `String`, while the schema expects an `Int`.

# 2. Enumeration Types

An enumeration type, commonly called an **enum**, restricts a field to a fixed collection of named values.

## Defining an enum

```graphql
enum Soldout {
  SOLDOUT
  ONSALE
}
```

The field may now contain only:

```text
SOLDOUT
ONSALE
```

The enum can be used in both output and input types:

```graphql
type Product {
  soldout: Soldout
}

input ProductInput {
  soldout: Soldout
}
```

## Boolean versus enum

A Boolean field could be defined as:

```graphql
soldout: Boolean
```

It accepts:

```text
true
false
```

An enum field could instead be defined as:

```graphql
soldout: Soldout
```

It accepts:

```text
SOLDOUT
ONSALE
```

The enum values communicate their meaning more clearly.

| Boolean representation | Enum representation |
|---|---|
| `true` | `SOLDOUT` |
| `false` | `ONSALE` |

## Valid and invalid enum input

Valid:

```graphql
soldout: ONSALE
```

Invalid:

```graphql
soldout: false
```

The second value is invalid because `false` is a Boolean, not a member of the `Soldout` enum.

Enum values are normally written without quotation marks:

```graphql
soldout: SOLDOUT
```

They are not written as strings:

```graphql
soldout: "SOLDOUT"
```

## Example mutation using an enum

```graphql
mutation {
  createProduct(
    input: {
      name: "Widget 99"
      description: "Another garden widget"
      price: 12.99
      inventory: 5
      soldout: ONSALE
    }
  ) {
    name
    price
    inventory
    soldout
  }
}
```

Possible response:

```json
{
  "data": {
    "createProduct": {
      "name": "Widget 99",
      "price": 12.99,
      "inventory": 5,
      "soldout": "ONSALE"
    }
  }
}
```

Although enum values are written without quotes in a GraphQL operation, they normally appear as strings in the JSON response.

## Why are enums useful?

Enums prevent clients from submitting arbitrary values.

Without an enum:

```graphql
status: String
```

Clients could submit inconsistent values:

```text
"available"
"Available"
"on sale"
"in-stock"
```

With an enum:

```graphql
enum ProductStatus {
  ONSALE
  SOLDOUT
  DISCONTINUED
  COMING_SOON
}
```

Only the defined values are accepted:

```graphql
status: ONSALE
```

Enums therefore improve:

- consistency;
- validation;
- readability;
- documentation;
- communication between client and server.

# 3. List Types

A list type represents multiple values of another type.

Lists are declared using square brackets:

```graphql
[Store]
```

This means:

```text
A list containing zero or more Store values.
```

## Defining the contained type

Before using a list of stores, the structure of one store must be defined:

```graphql
type Store {
  store: String
}
```

This means that each `Store` object contains a field called `store`.

A JavaScript store object might be:

```js
{
  store: "Pasadena"
}
```

## Adding a list to Product

```graphql
type Product {
  name: String
  stores: [Store]
}
```

A matching JavaScript object could be:

```js
{
  name: "Widget",
  stores: [
    { store: "Pasadena" },
    { store: "Los Angeles" }
  ]
}
```

The `stores` field contains an array of objects, and each object follows the `Store` type.

## Input lists

Output object types cannot be used directly as input object types.

A separate input type must be defined:

```graphql
input StoreInput {
  store: String
}
```

The product input can then contain a list of `StoreInput` objects:

```graphql
input ProductInput {
  name: String
  stores: [StoreInput]
}
```

A matching mutation input is:

```graphql
stores: [
  { store: "Pasadena" }
  { store: "Los Angeles" }
]
```

## Querying a list of objects

Because `stores` contains objects, a query must specify which fields are required from each object:

```graphql
query {
  getProduct(id: "abc123") {
    name
    stores {
      store
    }
  }
}
```

The nested selection:

```graphql
stores {
  store
}
```

means:

```text
For every object in the stores list, return its store field.
```

Possible response:

```json
{
  "data": {
    "getProduct": {
      "name": "Widget",
      "stores": [
        {
          "store": "Pasadena"
        },
        {
          "store": "Los Angeles"
        }
      ]
    }
  }
}
```

## Scalar list versus object list

A list may contain scalar values:

```graphql
tags: [String]
```

Matching data:

```js
tags: ["garden", "tools", "outdoor"]
```

A list may also contain objects:

```graphql
stores: [Store]
```

Matching data:

```js
stores: [
  { store: "Pasadena" },
  { store: "Los Angeles" }
]
```

When querying a scalar list, no nested selection is required:

```graphql
tags
```

When querying an object list, a nested selection is required:

```graphql
stores {
  store
}
```

# 4. Understanding the Exclamation Mark

In GraphQL, `!` means **non-null**.

It does not mean that a list must contain at least one item.

## List nullability

| Syntax | Meaning |
|---|---|
| `[Store]` | The list may be `null`, and individual items may be `null` |
| `[Store]!` | The list cannot be `null`, but individual items may be `null` |
| `[Store!]` | The list may be `null`, but its items cannot be `null` |
| `[Store!]!` | Neither the list nor its items can be `null` |

## Example: `[Store]!`

```graphql
stores: [Store]!
```

This is valid:

```graphql
stores: []
```

An empty list is still a list.

This is invalid:

```graphql
stores: null
```

The field is not permitted to be `null`.

However, the following may still be accepted because individual items are nullable:

```graphql
stores: [
  { store: "Pasadena" }
  null
]
```

## Example: `[Store!]!`

```graphql
stores: [Store!]!
```

This requires:

- the list itself to exist;
- every item inside the list to be non-null.

This is valid:

```graphql
stores: []
```

This is also valid:

```graphql
stores: [
  { store: "Pasadena" }
]
```

This is invalid:

```graphql
stores: null
```

This is also invalid:

```graphql
stores: [
  { store: "Pasadena" }
  null
]
```

GraphQL does not provide standard syntax for requiring at least one item in a list.

That rule must be implemented through additional validation in the resolver or business logic.

# 5. Combined Schema Example

```js
import { buildSchema } from "graphql";

const schema = buildSchema(`
  enum Soldout {
    SOLDOUT
    ONSALE
  }

  type Store {
    store: String
  }

  type Product {
    id: ID
    name: String
    description: String
    price: Float
    inventory: Int
    soldout: Soldout
    stores: [Store!]!
  }

  input StoreInput {
    store: String
  }

  input ProductInput {
    name: String
    description: String
    price: Float
    inventory: Int
    soldout: Soldout
    stores: [StoreInput!]!
  }

  type Query {
    getProduct(id: ID!): Product
  }

  type Mutation {
    createProduct(input: ProductInput!): Product
  }
`);

export default schema;
```

# 6. Updating the JavaScript Product Class

The JavaScript class must include all values that should be returned:

```js
class Product {
  constructor(
    id,
    {
      name,
      description,
      price,
      inventory,
      soldout,
      stores
    }
  ) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.price = price;
    this.inventory = inventory;
    this.soldout = soldout;
    this.stores = stores;
  }
}
```

The schema describes the API structure, while the JavaScript class creates the actual runtime object.

```text
GraphQL Product type
        ↓
describes the returned product
        ↓
JavaScript Product class
        ↓
constructs the actual product object
```

# 7. Complete Mutation Example

```graphql
mutation {
  createProduct(
    input: {
      name: "Widget 54"
      description: "A useful garden widget"
      price: 52.99
      inventory: 10
      soldout: ONSALE
      stores: [
        { store: "Orlando" }
        { store: "Miami" }
      ]
    }
  ) {
    id
    name
    description
    price
    inventory
    soldout
    stores {
      store
    }
  }
}
```

The input uses:

| Field | Type | Submitted value |
|---|---|---|
| `name` | `String` | `"Widget 54"` |
| `description` | `String` | `"A useful garden widget"` |
| `price` | `Float` | `52.99` |
| `inventory` | `Int` | `10` |
| `soldout` | `Soldout` enum | `ONSALE` |
| `stores` | List of `StoreInput` | Orlando and Miami |

Possible response:

```json
{
  "data": {
    "createProduct": {
      "id": "abc123",
      "name": "Widget 54",
      "description": "A useful garden widget",
      "price": 52.99,
      "inventory": 10,
      "soldout": "ONSALE",
      "stores": [
        {
          "store": "Orlando"
        },
        {
          "store": "Miami"
        }
      ]
    }
  }
}
```

# 8. Retrieving the Product

```graphql
query {
  getProduct(id: "abc123") {
    name
    price
    inventory
    soldout
    stores {
      store
    }
  }
}
```

Possible response:

```json
{
  "data": {
    "getProduct": {
      "name": "Widget 54",
      "price": 52.99,
      "inventory": 10,
      "soldout": "ONSALE",
      "stores": [
        {
          "store": "Orlando"
        },
        {
          "store": "Miami"
        }
      ]
    }
  }
}
```

# Glossary

| Term | Meaning | Example |
|---|---|---|
| Scalar | A basic individual value | `String`, `Int`, `Float` |
| `Int` | Whole-number scalar | `inventory: 10` |
| `Float` | Numeric scalar supporting decimals | `price: 52.99` |
| `String` | Text scalar | `name: "Widget"` |
| `Boolean` | True-or-false scalar | `soldout: false` |
| `ID` | Identifier scalar | `id: "abc123"` |
| Enum | Type restricted to named values | `ONSALE`, `SOLDOUT` |
| List | Multiple values of another type | `[Store]` |
| Object list | List containing structured objects | `[Store]` |
| Scalar list | List containing basic values | `[String]` |
| Non-null | Value that cannot be `null` | `String!` |
| Nested selection | Selection of fields inside an object | `stores { store }` |
| Input type | Structure accepted from the client | `StoreInput` |
| Output type | Structure returned to the client | `Store` |

# Key Points to Remember

==★ **Scalar type = one basic value.**==

==★ **Enum type = one value from a predefined set.**==

==★ **List type = multiple values of another type.**==

Examples:

```graphql
inventory: Int
```

One whole-number value.

```graphql
soldout: Soldout
```

One value selected from `ONSALE` or `SOLDOUT`.

```graphql
stores: [Store!]!
```

A non-null list containing non-null `Store` objects.

==★ **The schema specifies the permitted structure and types, while the resolver provides the actual data.**==
