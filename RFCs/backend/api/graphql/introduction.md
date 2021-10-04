# Introduction

This folder contains APIs in [GraphQL](https://graphql.org) specs. To edit the documents, you need to follow the guidelines below. 

## Types

The type system of GraphQL is defined [here](https://graphql.org/learn/schema/#type-system). All the types should have its own subheading and a table of the composition of types. 

The table should have three columns. The first one holds the field name; the second indicates the type of each field; the third describes what this field is for. 

For example: 

### Comm Type (Type Example)

| Field        | Type              | description                                                  |
| ------------ | ----------------- | ------------------------------------------------------------ |
| `initiator`  | `String`          | The name of the initiator of the communiaciton               |
| `receivor`   | `String`          | The name of the receiver                                     |
| `attachment` | `[package.File]!` | A list of files, where file is a custom type defined somewhere esle |

## Query

The query system is described [here](https://graphql.org/learn/queries/). All the types should also have its own subheading and a table of 

## Mutations