from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from stories import Story

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# create a Story object with the example story
story = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}."""
)

# create a homepage with a form to prompt the user for all the words in the story
@app.route('/')
def home():
    prompts = story.prompts
    return render_template('home.html', prompts=prompts)

# create a route to show the resulting story for those answers
@app.route('/story', methods=['POST'])
def show_story():
    answers = {}
    for prompt in story.prompts:
        answers[prompt] = request.form[prompt]
    result = story.generate(answers)
    return render_template('story.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)