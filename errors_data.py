errors = {
    "IndexError": {
        "description": "Occurs when trying to access an index that does not exist in a list.",
        "solution": "Make sure the index is within the valid range of the list.",
        "example": "my_list = [1, 2, 3]\nprint(my_list[5])",
        "fixed_code": "my_list = [1, 2, 3]\nprint(my_list[2])",
        "notes": "Use a valid index based on the list length."
    },

    "TypeError": {
        "description": "Occurs when an operation is used with the wrong data type.",
        "solution": "Check the types of your variables before using them together.",
        "example": "print('2' + 2)",
        "fixed_code": "print('2' + str(2))",
        "notes": "Convert int to str or str to int before combining."
    },

    "NameError": {
        "description": "Occurs when you use a variable or function name that has not been defined.",
        "solution": "Define the variable or make sure the name is spelled correctly.",
        "example": "print(x)",
        "fixed_code": "x = 10\nprint(x)",
        "notes": "Variables must be defined before use."
    },

    "ZeroDivisionError": {
        "description": "Occurs when you try to divide a number by zero.",
        "solution": "Make sure the denominator is not zero before dividing.",
        "example": "print(5 / 0)",
        "fixed_code": "x = 0\nif x != 0:\n    print(5 / x)\nelse:\n    print('Cannot divide by zero')",
        "notes": "Always validate the denominator first."
    },

    "KeyError": {
        "description": "Occurs when trying to access a dictionary key that does not exist.",
        "solution": "Check if the key exists before accessing it.",
        "example": "data = {'name': 'Ali'}\nprint(data['age'])",
        "fixed_code": "data = {'name': 'Ali'}\nif 'age' in data:\n    print(data['age'])\nelse:\n    print('Key not found')",
        "notes": "Use if key in dictionary before access."
    },

    "SyntaxError": {
        "description": "Occurs when Python finds invalid code syntax.",
        "solution": "Check your code for missing colons, brackets, quotes, or wrong structure.",
        "example": "if True\n    print('Hello')",
        "fixed_code": "if True:\n    print('Hello')",
        "notes": "A colon is required after if statements."
    }
}