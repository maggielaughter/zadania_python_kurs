import pesel_moduls

pesel=str(input('Wpisz swoj pesel :'))

pesel_validation=pesel_moduls.PeselValidation(pesel)
pesel_info=pesel_moduls.PeselInfo(pesel)

print(pesel_validation)
print(pesel_info)