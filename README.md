# OAuth and Google Calender

## How to run

1. Install dependencies, migrations

    ```
    pip install -r requirements.txt
    
    python manage.py migrate
    ```
2. Add .env file.

3. Collect static folder

    `python manage.py collectstatic`

3. Add _client_id.json_ file generated from Google Console Credentials to _secrets/client_id.json_.

2. Run the developement server

    `python manage.py runsslserver`
    
    __Note__: OAuth2 needs server to be https enabled so use `runsslserver`.
    
 ## .env file format
 
 The file needs to be at same level as manage.py named exactly as ".env".
 Following parameters are to be added in there:
 
1. SECRET_KEY
  
    This is the Django secret key.
      
      
  ### Optional parameters
  STATIC_ROOT
  
  STATIC_URL
  
  MEDIA_ROOT
  
  MEDIA_URL
