<<<<<<< HEAD
# netR

netR is a customizable [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) framework for [python](https://www.python.org/). netR is designed for Python users who want more control and customization. netR is composed from the ground up to ensure speed efficiency.

netR is a new [python](https://www.python.org/) framework that need much more development and [feedback](https://github.com/Net-Dash/netR/issues). netR is currently not recommended for production use until version 1.0.0 is released.

# Installing

```shell
$ pip install netR
```

# Docs

- ## Creating a simple HTTP server
    -  ```python
       from netR import netR

       def handler(req, res):
         res.write("Hello World")
         res.end()

       server = netR.http_server()
       server.add(handler)
       server.listen(port=5000, ip="127.0.0.1")
       ```
=======
# netR

netR is a customizable [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) framework for [python](https://www.python.org/). netR is designed for Python users who want more control and customization. netR is composed from the ground up to ensure speed efficiency. 

netR is a new [python](https://www.python.org/) framework that need much more development and [feedback](https://github.com/Net-Dash/netR/issues). netR is currently not recommended for production use until version 1.0.0 is released.

### Installing

```shell
$ pip install netR
```

# Docs

- ### Creating a simple HTTP server
    -  ```
       d
       ```
>>>>>>> 67264d25a2f4c325b65060f63cac6d40b028e5a0
