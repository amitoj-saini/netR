# netR

netR is a customizable [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) framework for [python](https://www.python.org/). netR is designed for Python users who want more control and customization. netR is composed from the ground up to ensure speed efficiency.

netR is a new [python](https://www.python.org/) framework that need much more development and [feedback](https://github.com/Net-Dash/netR/issues). netR is currently not recommended for production use until version 1.0.0 is released.

# Installing

```shell
$ pip install netR
```

# Examples

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

- ## Create a HTTP server with virtual hosts
    -  ```python
       from netR import netR

       def localhost_handler(req, res):
         res.write("Hello World you are visiting localhost")
         res.end()

       def ip_handler(req, res):
         res.write("Hello World you are visiting 127.0.0.1")
         res.end()

       server = netR.http_server()
       server.add(localhost_handler, "localhost")
       server.add(localhost_handler, "127.0.0.1")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Create a HTTP server with function paths
    -  ```python
       from netR import netR

       def handler(req, res):
         res.write("This is the home page")
         res.end()

       server = netR.http_server()
       server.add(handler, "*", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Another example of virtual hosts and paths combined
    -  ```python
       from netR import netR

       def handler(req, res):
         res.write("This is the home page on localhost")
         res.end()

       server = netR.http_server()
       server.add(handler, "localhost", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Serving static
    -  ```python
       from netR import netR

       server = netR.http_server()

       handler = server.serve_static("./somelocalfolder")

       server.add(handler, "*", "/somestaticurlpath")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Serving a file
    -  ```python
       from netR import netR

       def handler(req, res):
         res.serve_file("meme.gif")
         res.end()

       server = netR.http_server()
       server.add(handler, "localhost", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Writing response code
    -  ```python
       from netR import netR

       def handler(req, res):
         # you have the choice of also writing headers!
         res.write_head(404, {"Content-Type": "text/plain"})
         res.write("Sorry, are you lost?")
         res.end()

       server = netR.http_server()
       server.add(handler, "localhost", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```


- ## Getting headers
    -  ```python
       from netR import netR

       def handler(req, res):
         print(req.get_header("referer"))
         res.write("We got your headers!")
         res.end()

       server = netR.http_server()
       server.add(handler, "localhost", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Writing headers
    -  ```python
       from netR import netR

       def handler(req, res):
         res.set_header("Content-Type", "text/plain")
         res.write("Did you get our headers???")
         res.end()

       server = netR.http_server()
       server.add(handler, "localhost", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Getting query
    -  ```python
       from netR import netR

       def handler(req, res):
         print(req.query)
         res.write("We got your query!")
         res.end()

       server = netR.http_server()
       server.add(handler, "localhost", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```

- ## Getting post content
    -  ```python
       from netR import netR

       def handler(req, res):
         if req.method == "POST":
           # req.body also provides uploaded files (accepts: xxx-url-encoded and form-data)
           print(req.body)
           res.set_header("Content-Type", "text/plain")
           res.write("We got the file or text you sent!")
           res.end()

       server = netR.http_server()
       server.add(handler, "localhost", "/home")
       server.listen(port=5000, ip="127.0.0.1")
       ```