# API

## Introduction 

There are two sets of API, one for incoming requests and one for responses. 


## 3.0 API

### Request

The request object looks like the following. 

```typescript
interface request_object {
  code: string;
  graph: string | object;
  options?: request_options;
}

interface request_options {
    version?: '3' | '2';
    rand_seed?: int;
    float_precision?: int;
    input_list?: string;
}

```

If any of the request options is undefined, we use the default options to make sure it doesn't have undefined fields.

```typescript
let default_request_options: request_options = {
  version: '3';
  rand_seed: 0;
  float_precision: 4;
  input_list: '';  // not decided yet 
}
```

### Response

```typescript
interface response_object {
  execution_result: string | object; 
}
```

where the `execution_result` follows the [`result JSON API `](/RFCs/backend/database/tutorial_related_tables/execution_result/result_json_api.md). 
