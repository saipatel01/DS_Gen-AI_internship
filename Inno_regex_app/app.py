from flask import Flask, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    error = ""

    if request.method == "POST":
        text = request.form["text"]
        pattern = request.form["pattern"]

        try:
            matches = re.findall(pattern, text)
            result = ", ".join(matches)
        except re.error:
            error = "Invalid regex pattern"

    return f"""
    <html>
    <body style="font-family: Arial; text-align: center; padding-top: 40px;">

        <h2>Regex Matcher</h2>

        <form method="POST">
            <textarea name="text" rows="4" cols="50"
                placeholder="Enter test string"></textarea><br><br>

            <input type="text" name="pattern"
                placeholder="Enter regex pattern"><br><br>

            <button type="submit">Submit</button>
        </form>

        <p><b>Matches:</b> {result}</p>
        <p style="color:red;">{error}</p>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
