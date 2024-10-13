import sqlite3
from flask import Flask, render_template, request, redirect, url_for

#  Define the DATABASE variable
DATABASE = 'poll.db'  # or your desired database filename

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS options (id INTEGER PRIMARY KEY, option TEXT UNIQUE, selected INTEGER DEFAULT 0)")
        c.execute("CREATE TABLE IF NOT EXISTS votes (id INTEGER PRIMARY KEY, voter_name TEXT UNIQUE, option_id INTEGER)")

        # Insert poll options if they don't exist
    options = [
    "Rise of the Internet and Social Media",
    "Mobile Revolution",
    "Digital Entertainment",
    "Open-Source Software and Community",
    "Cloud Computing and Data Centers",
    "Artificial Intelligence and Machine Learning",
    "Human Genome Project",
    "Advances in Medical Technology",
    "Personalized Medicine and Genomics",
    "Vaccines and Disease Control",
    "Rise of China and India",
    "Global Warming and Climate Change Initiatives",
    "Global Economic Crisis of 2008",
    "Reality Television and Pop Culture",
    "Environmental Awareness and Climate Change",
    "Shifting Demographics and Globalization",
    "Millennials and Generation Z",
    "Food Trends and Global Cuisine",
    "Social Media and Mental Health",
    "Urbanization and Megacities",
    "Economic Inequality and Social Justice",
    "Immigration and Global Migration",
    "Digital Divide and Technological Access",
    "Urban Sprawl and Infrastructure",
    "Work-Life Balance and Remote Work",
    "Consumerism and Materialism",
    "Digital Literacy and Education",
    "Stem Cell Research and Controversies",
    "Renewable Energy and Sustainability",
    "Global Sports Stars and Franchises",
    "Popular Music and Cultural Icons",
    "Film and Television Trends",
    "E-Sports and Gaming Culture",
    "Social Media Influencers and Celebrity Culture",
    "Sports Broadcasting and Streaming",
    "The Olympics in the 2000's"
    ]

        
    for option in options:
            c.execute("INSERT OR IGNORE INTO options (option) VALUES (?)", (option,))
        
    conn.commit()


# Load poll options from the database
def get_poll_options():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
        SELECT options.id, options.option, options.selected, votes.voter_name
        FROM options
        LEFT JOIN votes ON options.id = votes.option_id
    """)
    options = c.fetchall()
    conn.close()
    return options


# Mark an option as selected and record the voter name
def select_option(option_id, voter_name):
    conn = sqlite3.connect('poll.db')
    c = conn.cursor()
    c.execute("UPDATE options SET selected = 1, voter_name = ? WHERE id = ?", (voter_name, option_id))
    conn.commit()
    conn.close()

# Add a new option
def add_option(new_option):
    conn = sqlite3.connect('poll.db')
    c = conn.cursor()
    c.execute("INSERT INTO options (option) VALUES (?)", (new_option,))
    conn.commit()
    conn.close()

@app.route('/')
def poll():
    options = get_poll_options()
    return render_template('poll.html', options=options)

@app.route('/choose/<int:option_id>', methods=['GET', 'POST'])
def choose(option_id):
    if request.method == 'POST':
        voter_name = request.form['voter_name']
        
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            # Check if the voter has already voted
            c.execute("SELECT * FROM votes WHERE voter_name = ?", (voter_name,))
            if c.fetchone() is None:
                # If not voted, record their vote
                c.execute("INSERT INTO votes (voter_name, option_id) VALUES (?, ?)", (voter_name, option_id))
                # Mark the option as selected
                c.execute("UPDATE options SET selected = 1 WHERE id = ?", (option_id,))
                conn.commit()
                return redirect(url_for('poll'))
            else:
                # Voter has already voted
                return render_template('error.html', message="You have already voted.")

    return render_template('choose_option.html', option_id=option_id)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_option = request.form['new_option']
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO options (option) VALUES (?)", (new_option,))
            conn.commit()
        return redirect(url_for('poll'))

    return render_template('add_option.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
