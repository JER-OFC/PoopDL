## API Documentation

### Get All File

URL
  - ```py
    https://poopdl-api.dapuntaratya.com/generate_file
    ```

Params
  - ```json
    {"url":url}
    ```

Response
  - ```json
    {"status":status, "message":message, "file":file}
    ```

### Get Link Download & Streaming

URL
  - ```py
    https://poopdl-api.dapuntaratya.com/generate_link
    ```

Params
  - ```json
    {"domain":domain, "id":id}
    ```

Response
  - ```json
    {"status":status, "message":message, "link":link}
    ```