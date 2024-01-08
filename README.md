## Description

This code is intended to enable the front-end to directly upload files to S3 without relying on the backend. This approach significantly alleviates the CPU load on the remote server.

The mechanism involves the front-end sending a file upload request to the backend. Subsequently, the backend requests a temporary URL from S3 and returns it to the front-end. Upon receiving the URL, the front-end can then proceed to directly upload the file to the remote S3 storage.

## Folder Structure

```
S3_Presigned_URL/
├── templates/
│   └── index.html
├── .gitignore
├── backend.py
├── config.dist.py
├── README.md
```

## Step

1. Ensure that all dependencies are installed in your Python environment. For detailed instructions, refer to: "https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html".
2. Create a `config.py` file based on `config.dist.py` and fill in your own API key and bucket information.
3. Configure your S3 settings by navigating to your S3 console, selecting your bucket, navigating to Permissions, and then configuring CORS as follows:

```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT"
        ],
        "AllowedOrigins": [
            "http://127.0.0.1:5000"
        ],
        "ExposeHeaders": []
    }
]
```

4. Run the command `python <YOUR BACKENT.PY FULL ROUTE>`
5. Open the corresponding link, such as `http://127.0.0.1:5000/` to explore the application.
6. You can test the functionality by adjusting the `ExpiresIn` value on Line 20 in `backend.py` using Postman.
