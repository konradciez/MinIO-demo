# Instalacja

https://github.com/minio/minio#install-from-source

## Zmiana domyślnych Root Credentials

```
$env:MINIO_ROOT_USER="admin"
$env:MINIO_ROOT_PASSWORD="supersecretpassword"
```

## Uruchomienie serwera we wskazanym folderze lokalnym.
Flaga --console-address ":9001" wymusiłaby uruchomienie interfejsu graficznego na konkretnym innym porcie.

`minio server C:\folder_na_minio`

