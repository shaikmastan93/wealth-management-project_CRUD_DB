from flask import Flask

app = Flask(__name__)

# This is the simple GET method
@app.route('/', methods=['GET'])
def home():
    return "I am Tejashwini, writing this message!"

if __name__ == '__main__':
    app.run()