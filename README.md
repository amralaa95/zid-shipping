# zid-shipping




## Run tests

Change the database's credentials to your local database's credentials in .env file
```bash
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
python manage.py test
```

## Building

we use Docker compose, this will install Mysql and then launch the app

```bash
docker-compose up --build
```

## Swagger


```bash
http://localhost:9000/openapi/
```

## Simple Workflow

```bash
- Enter to swager openapi
- Use first API to create a shippment it will create a shippment in courier and then save it on our system
- You can retrive this shippment by tracking id with second API and this like create waybill from our system
- Third API is used like a webhook and can be used in couriers to update shippment status in our system
- Create a shipment
- Schedule it
- Fourth API used for print waybill label
- Fifth API used for get status for tracking id from courier itself
- Sixth API for cancel a shippment and this feature can nott be used for all couriers
```
