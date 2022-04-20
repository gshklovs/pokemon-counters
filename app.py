# app.py
import pokemon
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=["POST"])
def register():
    pokemon_name = request.form.get("pokemon_name")
    list_len = request.form.get("list_len")
    if not pokemon_name or not list_len.isdigit():
        return 'failure, no input provided'
    my_result = pokemon.run(pokemon_name, int(list_len))
    return render_template('results.html', my_result=my_result, pokemon_name=pokemon_name)



if __name__ == '__main__':
    app.run(debug=True)


