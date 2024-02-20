import dao

while True:
    text = input('Dao > ')
    result, error = dao.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)
