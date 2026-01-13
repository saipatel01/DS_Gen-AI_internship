# S1 - Import flask
from flask import Flask, request

# S2 - Initialize Flask object
app = Flask(__name__)

# S3 - create end point or route + logic
@app.route('/')
def sai():
    name = request.args.get('name')

    if name:
        return f"""
        <h1>Hello, {name.upper()} </h1>
        <p>Your name in uppercase is: <b>{name.upper()}</b></p>
        """
    else:
        return """
        <h1>Welcome to the Flask App </h1>
        <p>Please provide your name in the URL.</p>
        <p>Example: <code>?name=saipatel</code></p>
        """
@app.route('/length')
def name_length():
    name = request.args.get('name')
    if name:
        return f"<h1>Length of your name: {len(name)}</h1>"
    return "<h1>Please provide a name</h1>"

# S4 - run the applicatiopn
if __name__ == '__main__':
    app.run(debug=True)
