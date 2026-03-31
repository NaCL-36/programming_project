errors = {
    "IndexError": {
        "description": "Occurs when trying to access an index that does not exist in a list.",
        "solution": "Make sure the index is within the valid range of the list.",
        "example": "my_list = [1, 2, 3]\nprint(my_list[5])"
    },
    "TypeError": {
        "description": "Occurs when an operation is used with the wrong data type.",
        "solution": "Check the types of your variables before using them together.",
        "example": "print('2' + 2)"
    },
    "NameError": {
        "description": "Occurs when you use a variable or function name that has not been defined.",
        "solution": "Define the variable or make sure the name is spelled correctly.",
        "example": "print(x)"
    },
    "ZeroDivisionError": {
        "description": "Occurs when you try to divide a number by zero.",
        "solution": "Make sure the denominator is not zero before dividing.",
        "example": "print(5 / 0)"
    },
    "KeyError": {
        "description": "Occurs when trying to access a dictionary key that does not exist.",
        "solution": "Check if the key exists before accessing it.",
        "example": "data = {'name': 'Ali'}\nprint(data['age'])"
    },
    "SyntaxError": {
        "description": "Occurs when Python finds invalid code syntax.",
        "solution": "Check your code for missing colons, brackets, quotes, or wrong structure.",
        "example": "if True\n    print('Hello')"
    }
}