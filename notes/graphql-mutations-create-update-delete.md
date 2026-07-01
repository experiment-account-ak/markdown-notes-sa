# GraphQL Mutations: Create, Update, and Delete

## Objective

Understand how GraphQL mutations are used to change data stored in a database.

The three fundamental mutation operations are:

```text
Create → add a new item
Update → modify an existing item
Delete → remove an existing item
```

These operations, together with queries for reading data, form the common CRUD pattern:

| CRUD operation | GraphQL operation |
|---|---|
| Create | Mutation |
| Read | Query |
| Update | Mutation |
| Delete | Mutation |

## Mental model: a warehouse

Imagine an application as a warehouse containing products.

- The database is the warehouse.
- A product’s ID is its shelf number.
- The schema is the official request form describing what actions are allowed.
- A resolver is the warehouse employee who carries out the request.
- The mutation sent through GraphiQL is the customer’s instruction.

For example:

```text
createProduct
      ↓
Put a new product into the warehouse.

updateProduct
      ↓
Find a product by shelf number and change it.

deleteProduct
      ↓
Find a product by shelf number and remove it.
```

The general process is:

```text
Client sends mutation
          ↓
GraphQL checks the schema
          ↓
GraphQL calls the matching resolver
          ↓
Resolver communicates with the database
          ↓
Database performs the change
          ↓
Resolver returns a result
          ↓
GraphQL sends the result to the client
```

# 1. Where Does Each Part Belong?

A simple GraphQL project may contain:

```text
project/
├── index.js
├── data/
│   ├── schema.js
│   └── resolvers.js
└── models/
    └── Product.js
```

| File | Responsibility |
|---|---|
| `schema.js` | Declares which mutations exist and their input/output types |
| `resolvers.js` | Contains functions that perform the database operations |
| `Product.js` | Defines how products are represented in the database |
| `index.js` | Connects Express, GraphQL, the schema, and resolvers |

# 2. Simplified Product Model

To make the mutation process easier to understand, assume that a product has only:

- an ID;
- a name;
- a price.

## `models/Product.js`

A simplified Mongoose model could look like this:

```js
import mongoose from "mongoose";

const productSchema = new mongoose.Schema({
  name: String,
  price: Number
});

const Product = mongoose.model("Product", productSchema);

export default Product;
```

This tells MongoDB that a product contains:

```text
name → text
price → number
```

MongoDB automatically creates an `_id` for every stored product.

# 3. GraphQL Schema

## `data/schema.js`

```js
import { buildSchema } from "graphql";

const schema = buildSchema(`
  type Product {
    id: ID
    name: String
    price: Float
  }

  input CreateProductInput {
    name: String!
    price: Float!
  }

  input UpdateProductInput {
    id: ID!
    name: String
    price: Float
  }

  type Query {
    getProduct(id: ID!): Product
  }

  type Mutation {
    createProduct(input: CreateProductInput!): Product
    updateProduct(input: UpdateProductInput!): Product
    deleteProduct(id: ID!): String
  }
`);

export default schema;
```

The schema declares three mutations.

## `createProduct`

```graphql
createProduct(input: CreateProductInput!): Product
```

Creates a product and returns the created product.

## `updateProduct`

```graphql
updateProduct(input: UpdateProductInput!): Product
```

Updates a product and returns the updated product.

## `deleteProduct`

```graphql
deleteProduct(id: ID!): String
```

Deletes a product and returns a confirmation message.

## Why are there separate create and update inputs?

When creating a product, the client does not yet have an ID:

```graphql
input CreateProductInput {
  name: String!
  price: Float!
}
```

When updating a product, the ID is necessary to identify which product should be changed:

```graphql
input UpdateProductInput {
  id: ID!
  name: String
  price: Float
}
```

The update fields are optional because the client may want to change only one property.

For example:

```graphql
{
  id: "123"
  price: 50.99
}
```

This means:

```text
Find product 123 and change only its price.
```

# 4. Why Are Database Resolvers Asynchronous?

Database operations take time.

The application may need to wait for MongoDB to:

- insert a document;
- locate and update a document;
- delete a document.

Resolvers are therefore written with `async`:

```js
async ({ input }) => {
  // database work
}
```

The `await` keyword waits for the database operation to finish:

```js
const product = await Product.create(input);
```

Without `await`, the resolver might return before the database has completed the operation.

# 5. Create a Product

## Schema declaration

```graphql
createProduct(input: CreateProductInput!): Product
```

In plain language:

```text
createProduct requires a product input and returns the newly created product.
```

## Create resolver

## `data/resolvers.js`

```js
import Product from "../models/Product";

const resolvers = {
  createProduct: async ({ input }) => {
    try {
      const newProduct = new Product({
        name: input.name,
        price: input.price
      });

      const savedProduct = await newProduct.save();

      return {
        id: savedProduct._id.toString(),
        name: savedProduct.name,
        price: savedProduct.price
      };
    } catch (error) {
      throw new Error(error.message);
    }
  }
};

export default resolvers;
```

## Step-by-step explanation

### Create a JavaScript/Mongoose object

```js
const newProduct = new Product({
  name: input.name,
  price: input.price
});
```

At this point, the product exists in application memory, but it has not necessarily been stored in MongoDB yet.

### Save it to MongoDB

```js
const savedProduct = await newProduct.save();
```

The resolver waits until MongoDB saves the product.

MongoDB generates an `_id`, for example:

```text
6654b3e8215a17d2c9a00112
```

### Return the created product

```js
return {
  id: savedProduct._id.toString(),
  name: savedProduct.name,
  price: savedProduct.price
};
```

GraphQL then returns the fields requested by the client.

## Try the create mutation in GraphiQL

```graphql
mutation {
  createProduct(
    input: {
      name: "Shovel"
      price: 14.99
    }
  ) {
    id
    name
    price
  }
}
```

Possible response:

```json
{
  "data": {
    "createProduct": {
      "id": "6654b3e8215a17d2c9a00112",
      "name": "Shovel",
      "price": 14.99
    }
  }
}
```

## Create execution flow

```text
createProduct mutation
          ↓
Schema validates name and price
          ↓
createProduct resolver runs
          ↓
new Product(...) creates an object
          ↓
.save() inserts it into MongoDB
          ↓
MongoDB generates an ID
          ↓
Resolver returns the created product
```

# 6. Update a Product

An update requires the ID of an existing product.

## Schema declaration

```graphql
updateProduct(input: UpdateProductInput!): Product
```

The input may contain:

```graphql
{
  id: "product-id"
  price: 50.99
}
```

This means:

```text
Find this product and change its price.
```

## Update resolver

Add the following resolver:

```js
updateProduct: async ({ input }) => {
  try {
    const { id, ...changes } = input;

    const updatedProduct = await Product.findByIdAndUpdate(
      id,
      changes,
      {
        new: true,
        runValidators: true
      }
    );

    if (!updatedProduct) {
      throw new Error("Product not found");
    }

    return {
      id: updatedProduct._id.toString(),
      name: updatedProduct.name,
      price: updatedProduct.price
    };
  } catch (error) {
    throw new Error(error.message);
  }
}
```

## Understanding the update resolver

### Separate the ID from the changed values

```js
const { id, ...changes } = input;
```

Suppose the input is:

```js
{
  id: "123",
  price: 50.99
}
```

After destructuring:

```js
id = "123";
```

and:

```js
changes = {
  price: 50.99
};
```

The ID identifies the product.

The `changes` object contains the values to update.

### Find and update the product

```js
const updatedProduct = await Product.findByIdAndUpdate(
  id,
  changes,
  {
    new: true,
    runValidators: true
  }
);
```

This means:

```text
Find the product with this ID
          ↓
Apply the supplied changes
          ↓
Return the updated product
```

## Important meaning of `new: true`

```js
{
  new: true
}
```

means:

```text
Return the product after it has been updated.
```

Without it, Mongoose may return the old version of the document.

It does not mean “create a product if it does not exist.”

To create a product when none is found, Mongoose uses:

```js
{
  upsert: true
}
```

These options have different meanings:

| Option | Meaning |
|---|---|
| `new: true` | Return the updated document |
| `upsert: true` | Create a new document if none matches |

## Try the update mutation

First copy the ID returned by `createProduct`.

Then run:

```graphql
mutation {
  updateProduct(
    input: {
      id: "6654b3e8215a17d2c9a00112"
      price: 50.99
    }
  ) {
    id
    name
    price
  }
}
```

Possible response:

```json
{
  "data": {
    "updateProduct": {
      "id": "6654b3e8215a17d2c9a00112",
      "name": "Shovel",
      "price": 50.99
    }
  }
}
```

The name remains unchanged because only the price was supplied.

## Update execution flow

```text
updateProduct mutation
          ↓
Schema checks that an ID is supplied
          ↓
Resolver extracts ID and changes
          ↓
MongoDB finds the product by ID
          ↓
MongoDB applies the changes
          ↓
Updated product is returned
```

# 7. Delete a Product

Deleting usually requires only the product ID.

## Schema declaration

```graphql
deleteProduct(id: ID!): String
```

In plain language:

```text
deleteProduct requires an ID and returns a message.
```

The `!` means that the ID cannot be omitted or `null`.

## Delete resolver

```js
deleteProduct: async ({ id }) => {
  try {
    const result = await Product.deleteOne({
      _id: id
    });

    if (result.deletedCount === 0) {
      throw new Error("Product not found");
    }

    return "Successfully deleted product";
  } catch (error) {
    throw new Error(error.message);
  }
}
```

## Understanding the delete resolver

### Find the product by MongoDB ID

```js
{
  _id: id
}
```

MongoDB stores its identifier in `_id`.

### Delete one matching document

```js
await Product.deleteOne({
  _id: id
});
```

This asks MongoDB to delete the product whose `_id` matches the supplied ID.

### Check whether anything was deleted

```js
if (result.deletedCount === 0) {
  throw new Error("Product not found");
}
```

If `deletedCount` is zero, no product had that ID.

### Return confirmation

```js
return "Successfully deleted product";
```

Because the product no longer exists, the mutation returns a message instead of the deleted product.

## Try the delete mutation

```graphql
mutation {
  deleteProduct(
    id: "6654b3e8215a17d2c9a00112"
  )
}
```

Possible response:

```json
{
  "data": {
    "deleteProduct": "Successfully deleted product"
  }
}
```

## Delete execution flow

```text
deleteProduct mutation
          ↓
Schema checks that ID is present
          ↓
deleteProduct resolver runs
          ↓
MongoDB finds the product by _id
          ↓
deleteOne removes the product
          ↓
Resolver returns a confirmation message
```

# 8. Complete Simplified Resolvers File

```js
import Product from "../models/Product";

const resolvers = {
  createProduct: async ({ input }) => {
    try {
      const newProduct = new Product({
        name: input.name,
        price: input.price
      });

      const savedProduct = await newProduct.save();

      return {
        id: savedProduct._id.toString(),
        name: savedProduct.name,
        price: savedProduct.price
      };
    } catch (error) {
      throw new Error(error.message);
    }
  },

  updateProduct: async ({ input }) => {
    try {
      const { id, ...changes } = input;

      const updatedProduct = await Product.findByIdAndUpdate(
        id,
        changes,
        {
          new: true,
          runValidators: true
        }
      );

      if (!updatedProduct) {
        throw new Error("Product not found");
      }

      return {
        id: updatedProduct._id.toString(),
        name: updatedProduct.name,
        price: updatedProduct.price
      };
    } catch (error) {
      throw new Error(error.message);
    }
  },

  deleteProduct: async ({ id }) => {
    try {
      const result = await Product.deleteOne({
        _id: id
      });

      if (result.deletedCount === 0) {
        throw new Error("Product not found");
      }

      return "Successfully deleted product";
    } catch (error) {
      throw new Error(error.message);
    }
  }
};

export default resolvers;
```

# 9. Connecting the Schema and Resolvers

## `index.js`

```js
import express from "express";
import { graphqlHTTP } from "express-graphql";

import schema from "./data/schema";
import resolvers from "./data/resolvers";

const app = express();

app.use(
  "/graphql",
  graphqlHTTP({
    schema: schema,
    rootValue: resolvers,
    graphiql: true
  })
);

app.listen(8080, () => {
  console.log(
    "GraphQL server running on localhost:8080/graphql"
  );
});
```

The important connection is:

```js
rootValue: resolvers
```

GraphQL matches schema fields to resolver functions by name:

```text
Schema mutation       Resolver function
----------------------------------------
createProduct     →   createProduct
updateProduct     →   updateProduct
deleteProduct     →   deleteProduct
```

A spelling difference prevents GraphQL from finding the correct resolver.

# 10. Why Use `try`, `catch`, and `throw`?

Database operations can fail because:

- the database is unavailable;
- the ID is invalid;
- validation fails;
- the item does not exist;
- a required field is missing.

The resolver therefore uses:

```js
try {
  // perform database operation
} catch (error) {
  throw new Error(error.message);
}
```

`try` contains the operation that may fail.

`catch` receives the error.

`throw new Error(...)` passes the error back to GraphQL.

GraphQL then returns an error response instead of pretending that the mutation succeeded.

# 11. Full CRUD Lifecycle

A common test sequence is:

## Step 1: Create

```graphql
mutation {
  createProduct(
    input: {
      name: "Shovel"
      price: 14.99
    }
  ) {
    id
    name
    price
  }
}
```

Copy the returned ID.

## Step 2: Update

```graphql
mutation {
  updateProduct(
    input: {
      id: "COPIED_ID"
      price: 50.99
    }
  ) {
    id
    name
    price
  }
}
```

## Step 3: Read

```graphql
query {
  getProduct(id: "COPIED_ID") {
    id
    name
    price
  }
}
```

## Step 4: Delete

```graphql
mutation {
  deleteProduct(id: "COPIED_ID")
}
```

The complete lifecycle is:

```text
Create
  ↓
Product receives an ID
  ↓
Update using that ID
  ↓
Query using that ID
  ↓
Delete using that ID
```

# Glossary

| Term | Meaning | Example |
|---|---|---|
| Mutation | GraphQL operation that changes data | `createProduct` |
| Create | Add a new database item | `newProduct.save()` |
| Update | Modify an existing item | `findByIdAndUpdate()` |
| Delete | Remove an existing item | `deleteOne()` |
| Resolver | Function that performs a GraphQL operation | `createProduct: async ...` |
| Database model | JavaScript representation of a database collection | `Product` |
| Document | One stored MongoDB object | One product |
| `_id` | MongoDB’s internal document identifier | `"6654..."` |
| `async` | Marks a function that performs asynchronous work | `async ({ input })` |
| `await` | Waits for an asynchronous operation to finish | `await newProduct.save()` |
| `try/catch` | Handles errors during an operation | Database failure handling |
| `new: true` | Returns the updated document | Mongoose update option |
| `upsert: true` | Creates a document if none exists | Optional Mongoose update behavior |
| `deletedCount` | Number of documents deleted | `1` or `0` |
| CRUD | Create, Read, Update, Delete | Basic data operations |

# Key Points to Remember

==★ **Schema declares which mutations are available.**==

==★ **Resolver performs the actual database operation.**==

==★ **Database model provides methods such as save, update, and delete.**==

==★ **ID identifies which item should be updated or deleted.**==

The three mutations follow the same basic pattern:

```text
Create:
receive data
    ↓
create object
    ↓
save
    ↓
return object
```

```text
Update:
receive ID and changes
    ↓
find object
    ↓
update
    ↓
return object
```

```text
Delete:
receive ID
    ↓
find object
    ↓
delete
    ↓
return confirmation
```
