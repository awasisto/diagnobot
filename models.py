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

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Condition(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    probability = db.Column(db.Float, nullable=False)
    symptom_probabilities = db.relationship('SymptomProbability')


class Symptom(db.Model):
    __tablename__ = 'symptoms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    probability = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class SymptomProbability(db.Model):
    __tablename__ = 'symptom_probabilities'
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), nullable=False)
    condition = db.relationship('Condition')
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id'), nullable=False)
    symptom = db.relationship('Symptom')
    probability = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('condition_id', 'symptom_id'),
    )
