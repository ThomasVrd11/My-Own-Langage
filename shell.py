import dao

while True:
    text = input('My-Own-Langage > ')
    result, error = dao.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)
