cpf = input('Insira seu CPF')

cpf = cpf.strip()
cpf = cpf.replace('.', '').replace('-', '')

if len(cpf) == 11 or cpf.isnumeric():
    print(cpf)
else:
    print('Digite seu CPF corretamente e digite apenas números')