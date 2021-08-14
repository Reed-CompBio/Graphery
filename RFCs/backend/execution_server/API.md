# API

## Introduction 

There are two sets of API, one for incoming requests and one for responses. 

## Request

The request object looks like the following. 

```typescript
interface request_object {
  code: string;
  graph: string | object;
  options?: request_options;
}

interface request_options {
    version: '1';
		rand_seed?: int;
}

let default_request_options: request_options = {
  version: '1';
  rand_seed: 0;
}
```

## Response

```typescript
interface response_object {
  execution_result: string | object; 
}
```

