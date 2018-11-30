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

from models import Condition, SymptomProbability, Symptom


def get_possible_conditions(symptoms):
    possible_conditions = []
    for condition in Condition.query.all():
        possible_conditions.append({'name': condition.name, 'probability': get_condition_probability_given_symptoms(
            condition, symptoms)})
    possible_conditions.sort(key=lambda possible_condition: possible_condition['probability'], reverse=True)
    return possible_conditions


def get_condition_probability_given_symptoms(condition, symptoms):
    symptoms = symptoms.copy()
    condition_probability = condition.probability
    while len(symptoms) > 0:
        first_symptom = symptoms.pop()
        if is_condition_has_symptom(condition, first_symptom):
            condition_probability = get_symptom_probability_given_condition(
                first_symptom, condition) * condition.probability / get_symptom_probability(first_symptom['id'])
            break
    if len(symptoms) > 0:
        for symptom in symptoms:
            if is_condition_has_symptom(condition, symptom):
                condition_probability = bayesian_update(condition, symptom, condition_probability)
    return condition_probability


def bayesian_update(condition, symptom, previous_probability):
    return previous_probability * get_symptom_probability_given_condition(symptom, condition) /\
           (previous_probability * get_symptom_probability_given_condition(symptom, condition) +
            (1 - get_symptom_probability_given_condition(symptom, condition)) * get_symptom_probability(symptom['id']))


def get_symptom_probability(symptom_id):
    return Symptom.query.get(symptom_id).probability


def get_symptom_probability_given_condition(symptom, condition):
    return SymptomProbability.query.filter_by(condition_id=condition.id, symptom_id=symptom['id']).first().probability


def is_condition_has_symptom(condition, symptom):
    return SymptomProbability.query.filter_by(condition_id=condition.id, symptom_id=symptom['id']).first() is not None
