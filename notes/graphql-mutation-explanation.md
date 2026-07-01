# GraphQL Mutation: Save and Read One Message

## Objective

Understand a GraphQL **mutation** as simply as possible: a mutation is a request that **changes data**.

A query reads data:

```text
Give me the current message.
```

A mutation changes data:

```text
Replace the current message with "Hello".
```

## Simplest mental model

Think of GraphQL like a reception desk:

- `schema.js` is the list of allowed requests.
- `resolvers.js` contains the workers who actually perform those requests.
- `index.js` connects everything to the server.
- GraphiQL is where you send the request.

## Example: save and read one message

We will store just one message:

```js
let savedMessage = "Nothing saved yet";
```

The mutation will change it.

## File structure

```text
project/
├── index.js
└── data/
    ├── schema.js
    └── resolvers.js
```

# 1. `schema.js`: Declare What Is Allowed

```js
import { buildSchema } from "graphql";

const schema = buildSchema(`
  type Query {
    getMessage: String
  }

  type Mutation {
    setMessage(message: String!): String
  }
`);

export default schema;
```

## What does this mean?

## Query

```graphql
getMessage: String
```

This means:

The client may ask for the saved message, and GraphQL will return a string.

## Mutation

```graphql
setMessage(message: String!): String
```

Read it like this:

- `setMessage` = name of the mutation
- `message` = the value the client must send
- `String!` = it must be text and cannot be missing
- `: String` = the mutation returns text

In plain language:

The client can send a new message, and the server will return the saved message.

The schema only describes the operation. It does not save anything itself.

# 2. `resolvers.js`: Perform the Actual Work

```js
let savedMessage = "Nothing saved yet";

const resolvers = {
  getMessage: () => {
    return savedMessage;
  },

  setMessage: ({ message }) => {
    savedMessage = message;
    return savedMessage;
  }
};

export default resolvers;
```

This file contains the real logic.

## Query resolver

```js
getMessage: () => {
  return savedMessage;
}
```

This only reads the message.

```text
getMessage
    ↓
return savedMessage
```

## Mutation resolver

```js
setMessage: ({ message }) => {
  savedMessage = message;
  return savedMessage;
}
```

This actually changes the data.

Suppose GraphQL sends:

```js
{
  message: "Hello GraphQL"
}
```

The resolver performs:

```js
savedMessage = "Hello GraphQL";
```

Then it returns the updated value.

```text
Receive new message
        ↓
Save it in savedMessage
        ↓
Return the new message
```

The most important line is:

```js
savedMessage = message;
```

That is the actual mutation.

GraphQL does not automatically change the data. The resolver changes it.

# 3. `index.js`: Connect GraphQL to Express

```js
import express from "express";
import { graphqlHTTP } from "express-graphql";

import schema from "./data/schema";
import resolvers from "./data/resolvers";

const PORT = 8080;
const app = express();

app.use(
  "/graphql",
  graphqlHTTP({
    schema: schema,
    rootValue: resolvers,
    graphiql: true
  })
);

app.listen(PORT, () => {
  console.log(`Server running on localhost:${PORT}/graphql`);
});
```

The important connection is:

```js
schema: schema
```

This gives GraphQL the list of allowed operations.

And:

```js
rootValue: resolvers
```

This gives GraphQL the functions that perform those operations.

GraphQL connects them by name:

```text
Schema name        Resolver name
---------------------------------
getMessage    →    getMessage
setMessage    →    setMessage
```

The names must match exactly.

# 4. Start the server

Run:

```bash
npm start
```

Then open:

```text
http://localhost:8080/graphql
```

# 5. First, Read the Original Message

In GraphiQL, run:

```graphql
query {
  getMessage
}
```

Expected result:

```json
{
  "data": {
    "getMessage": "Nothing saved yet"
  }
}
```

Execution:

```text
GraphQL sees getMessage
          ↓
Calls resolvers.getMessage()
          ↓
Resolver returns savedMessage
          ↓
GraphQL sends the result
```

# 6. Now Change the Message with a Mutation

Run:

```graphql
mutation {
  setMessage(message: "Hello GraphQL")
}
```

Expected result:

```json
{
  "data": {
    "setMessage": "Hello GraphQL"
  }
}
```

Execution:

```text
Client sends:
setMessage(message: "Hello GraphQL")
                ↓
GraphQL checks schema.js:
Is setMessage allowed?
Does it accept a String?
                ↓
GraphQL calls:
resolvers.setMessage({
  message: "Hello GraphQL"
})
                ↓
Resolver executes:
savedMessage = "Hello GraphQL"
                ↓
Resolver returns:
"Hello GraphQL"
                ↓
GraphQL sends the response
```

# 7. Read the Message Again

Run:

```graphql
query {
  getMessage
}
```

Now the result is:

```json
{
  "data": {
    "getMessage": "Hello GraphQL"
  }
}
```

This proves that the mutation changed the value.

# The Three Files in One Sentence Each

## `schema.js`

Declares what clients are allowed to do.

```text
You may call `setMessage` and send a `String`.
```

## `resolvers.js`

Contains the code that actually does it.

```text
Put the new value into `savedMessage`.
```

## `index.js`

Connects the schema and resolvers to the GraphQL server.

```text
Use this schema and these resolver functions.
```

## Final mental model

```text
Mutation written in GraphiQL
            ↓
Schema confirms that the mutation exists
            ↓
GraphQL finds the resolver with the same name
            ↓
Resolver changes the data
            ↓
Resolver returns the result
            ↓
GraphQL sends the result back
```

The key idea is:

==★ **Schema describes the mutation.**==

==★ **Resolver performs the mutation.**==
