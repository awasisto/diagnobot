# Copyright 2018 Adityawarman Fanaro, Andika Wasisto
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, jsonify, render_template, request

import engine
from models import db, Symptom

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)


@app.route('/api/v1/symptoms')
def get_all_symptoms():
    all_symptoms = []
    for query_result_item in Symptom.query.all():
        all_symptoms.append(query_result_item.to_dict())
    return jsonify(all_symptoms)


@app.route('/api/v1/symptoms/<symptom_id>')
def get_symptom_by_id(symptom_id):
    return jsonify(Symptom.query.get(symptom_id).to_dict())


@app.route('/api/v1/diagnosis', methods=['POST'])
def diagnosis():
    return jsonify(engine.get_possible_conditions(request.json['symptoms']))


@app.route("/")
def hello():
    return render_template('diagnosis.html')


if __name__ == '__main__':
    app.run()
