from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = "secret123"

# 🔌 اتصال PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname="todo_app",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    return conn


# 🧱 إنشاء الجداول
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        is_done BOOLEAN DEFAULT FALSE,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()


# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# 🔑 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/todos')
        else:
            return "Wrong login ❌"

    return render_template('login.html')


# 📋 Todo
@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        cur.execute(
            "INSERT INTO todos (title, description, user_id) VALUES (%s, %s, %s)",
            (title, description, session['user_id'])
        )
        conn.commit()

    cur.execute(
        "SELECT * FROM todos WHERE user_id=%s",
        (session['user_id'],)
    )
    todos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('todo_list.html', todos=todos)


# ✅ Done
@app.route('/done/<int:id>')
def done(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE todos SET is_done = NOT is_done WHERE id=%s",
        (id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/todos')


# ✏️ Edit
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        cur.execute(
            "UPDATE todos SET title=%s, description=%s WHERE id=%s",
            (title, description, id)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/todos')

    cur.execute("SELECT * FROM todos WHERE id=%s", (id,))
    todo = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('edit.html', todo=todo)


# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)