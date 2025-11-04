# Standard Libraries
import ast

# Non-Standard Libraries


# Custom Modules


def convert_to_json(response):
    '''Extract JSON content and return valid python dictionary'''
    return ast.literal_eval(response.strip().strip('```json').strip('```').strip())