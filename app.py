import os
from flask import Flask, render_template, request, redirect
from supabase import create_client
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# Page 1: Enter Name & Age
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        if name and age:
            try:
                supabase.table("users").insert({"name": name, "age": int(age)}).execute()
                return redirect("/registered")
            except Exception as e:
                return f"Error inserting data: {e}"
    return render_template("index.html")

# Page 2: Show Registered Users
@app.route("/registered")
def registered():
    try:
        response = supabase.table("users").select("*").execute()
        users = response.data  # <-- must use .data
    except Exception as e:
        return f"Error fetching data: {e}"
    return render_template("registered.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
