# Simple Web Framework

## Example

```python
from nirvana import App
from nirvana import HttpResponse


app = App('localhost', 80)

def hello(request):
  data = bytes('Hello world!', 'utf-8')

  response = HttpResponse()
  response.setStatus('200 OK')
  response.setHeaders({
    'Content-Encoding': "utf-8",
    'Content-Type': 'text/plain',
    'Content-Length': str(len(data))
  })
  response.setBody(data)

  return data
```

app.get('/', hello)

app.run()
