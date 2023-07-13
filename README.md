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

## Reference
[Authlib reference for OIDC Flask](https://docs.authlib.org/en/latest/client/flask.html)