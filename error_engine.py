import re

def analyze_error(error_text):
    text = error_text.lower()
    
    # Pattern 1: TypeError - Concatenation
    if re.search(r'typeerror:.*concatenate|typeerror:.*must be str', text):
        return _build_response("TypeError", "High", 
            "You are trying to combine a string with a non-string type (like an integer).", 
            "Python doesn't automatically convert numbers to strings when using the '+' operator.", 
            "Convert the non-string value using the str() function.", 
            "print('Age: ' + 25)", "print('Age: ' + str(25))")
            
    # Pattern 2: Generic TypeError
    elif re.search(r'typeerror:', text):
        return _build_response("TypeError", "Medium", 
            "An operation was performed on an incorrect or unsupported data type.", 
            "A function or operator received a value of the wrong type.", 
            "Verify the types of variables involved using type().", 
            "'2' + 2", "int('2') + 2")

    # Pattern 3: IndexError - Out of bounds
    elif re.search(r'indexerror:.*out of range', text):
        return _build_response("IndexError", "High", 
            "You tried to access a list item using a position that doesn't exist.", 
            "The index provided is either negative or larger than the list length.", 
            "Ensure the index is between 0 and len(my_list) - 1.", 
            "my_list = [1, 2]\nval = my_list[2]", "my_list = [1, 2]\nval = my_list[1]")
            
    # Pattern 4: KeyError
    elif re.search(r'keyerror:', text):
        return _build_response("KeyError", "High", 
            "You tried to access a dictionary using a key that does not exist.", 
            "The key is missing from the dictionary keys structure.", 
            "Use the .get() method to safely access dictionary values.", 
            "val = my_dict['missing_key']", "val = my_dict.get('missing_key', 'default')")

    # Pattern 5: SyntaxError
    elif re.search(r'syntaxerror:.*invalid syntax', text):
        return _build_response("SyntaxError", "High", 
            "There is a typo or incorrect syntax preventing code execution.", 
            "Missing parentheses, colons, quotes, or indentation errors.", 
            "Check the exact line indicated in the stack trace for missing characters.", 
            "if True\n    print('Hello')", "if True:\n    print('Hello')")

    # Pattern 6: NameError
    elif re.search(r'nameerror:.*name .* is not defined', text):
        return _build_response("NameError", "High", 
            "You are using a variable or function name that hasn't been defined.", 
            "The Python interpreter couldn't find a matching element in the scope.", 
            "Check for typos, or ensure the variable is defined before usage.", 
            "print(undefined_var)", "undefined_var = 10\nprint(undefined_var)")

    # Fallback
    else:
        return _build_response("UnknownError", "Low", 
            "The system encountered an unclassified error pattern.", 
            "The trace text did not match any of our predefined structural heuristics.", 
            "Manually trace the log output referencing exact line bindings.", 
            "N/A", "N/A")


def _build_response(category, confidence, explanation, root, fix, inc, cor):
    return {
        "category": category,
        "confidence": confidence,
        "explanation": explanation,
        "root_cause": root,
        "fix": fix,
        "example": {
            "incorrect": inc,
            "correct": cor
        }
    }
