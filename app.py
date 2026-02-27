from flask import Flask
from routes import api
import debugpy

debugpy.listen(("127.0.0.1", 5678))
print("Debugger listening on 127.0.0.1:5678")

app = Flask(__name__)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
