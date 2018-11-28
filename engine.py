from models import Condition


def diagnose(symptoms):
    possible_conditions = []
    for condition in Condition.query.all():
        possible_conditions.append({'name': condition.name, 'probability': get_probability(condition, symptoms)})
    return possible_conditions


def get_probability(condition, symptoms, previous_probability=None):
    return 0
