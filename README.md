# scratchweb
a scratch website to implement OIDC

## How start
Create virutal environment
```
virtualenv env
```

Install dependencies
```
pip install -r requirements.txt
```

Run app
```
flask --app oidc run --cert=adhoc --debug
```