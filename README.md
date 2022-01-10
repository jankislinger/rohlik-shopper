API to do the shopping on rohlik.cz for you. Designed to be used together with Home Assistant

```shell
docker build -t rohlik-shopper .
docker run --rm \
  -p 8000:5000 \
  --name rohlik-shopper \
  -e ROHLIK_EMAIL=<email> \
  -e ROHLIK_PASSWORD=<password> \
  rohlik-shopper
```
