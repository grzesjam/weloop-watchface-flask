# weloop-watchface-flask

Another rewrite of one of my projects. 

This time weloop-watchface-serverlike, this time in Flask (don't ask why).

It was done in 1h so it's not perfect but it works... it reuses UI from old project.

## Usage

### Prerequisites

```
Docker
```

### Running

Just run docker-compose

```bash
docker compose up -d
```

App will be available on port 5000

> **Note:** If you want to use it on different port, change it in docker-compose.yml


## Preparing modified version of app

1. Unpacking app using [Apktool](https://ibotpeaches.github.io/Apktool/) 
```
java -jar apktool d [name of apk]
```
2. Modifying in app address of server  
```
on Chronos app (in weloop probably in similar place) in 
[name of apk]\smali\com\yf\weloop\activities\SendDialActivity$13.smali in 107 line
to "http://[domain]/watch" or "https://[domain]/watch"
```
* Packing app 
```
java -jar apktool b [name of folder]
```
* signing apk
```
Find on google how (sorry)
```

## Uses

[Bootstrap 3.4.1](https://getbootstrap.com/) (yes, for real :p)

## Authors

* **Grzegorz M** - *Creator* - [weloop-watchface-flask](https://github.com/grzesjam/weloop-watchface-flask)

See also the list of [contributors](https://github.com/grzesjam/weloop-watchface-flask /graphs/contributors) who participated in this project.

## License

This project is licensed under the **MIT License**
- see the [LICENSE](LICENSE) file for details