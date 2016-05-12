new_account = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string',
            'pattern': '^\w{6,}$',
            'maxLength': 50,},
        'password': {'type': 'string',
            'pattern': '^.+$',
            'maxLength': 50,},
        'email': {'type': 'string',
            'pattern': "^[a-zA-Z0-9!#$%&'*+-/=?^_`{|}~.]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$",
            'maxLength': 100},
        'first_name': {'type': 'string',
            'pattern': '^[^\d~`!@#$%^&*()_+=<>,.?/:;"\[\]\\\{}|]+$',
            'maxLength': 100},
        'last_name': {'type': 'string',
            'pattern': '^[^\d~`!@#$%^&*()_+=<>,.?/:;"\[\]\\\{}|]+$',
            'maxLength': 100},
        'dob': {'type': 'string',
            'pattern': '^\d\d\d\d[/-]\d\d[/-]\d\d$',},
        'sex': {'type': 'string',
            'pattern': '^male|Male|female|Female$',},
        'phone': {'type': 'string',
            'pattern': '^\d{10,}$',
            'maxLength': 20},
        'visible_in_directory': {'type': 'string',
            'pattern': '^y|Y|n|N$',},
        },
    'required': [
       'username',
       'password',
       'email',
       'first_name',
       'last_name',
       'dob',
       'sex',
       'phone',
       'visibile_in_directory',
       ],
   }