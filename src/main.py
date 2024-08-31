from flask import Flask, request
from handle import Handle

# urls = (
#     '/wx', 'Handle'
# )
# app = web.application(urls, globals())
app = Flask("LNSFOCOLNS", static_folder="../static")
handle = Handle()

@app.route('/wx', methods=['GET'])
def wxGet():
    print(request)
    return handle.GET(request)

@app.route('/wx', methods=['POST'])
def wxPOST():
    print(request)
    return handle.POST(request)



if __name__ == "__main__":
    app.run(port=80, debug=True)

