from anillo.app import application
from anillo.middlewares.json import wrap_json
from anillo.http import Ok

#
# You can test this example with the curl line:
#
# curl -X POST -d '{"echo": "Hello World"}' localhost:5000 -H "Content-Type: application/json"
#

def index(request):
    return Ok({"echo-response": request.body["echo"]}, headers={"Content-Type": "application/json"})


app = application(wrap_json(index))


if __name__ == '__main__':
    from anillo import serving
    serving.run_simple(app, port=5000)
