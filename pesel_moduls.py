# centuries
nineteenth_century = ['81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92']
twentieth_century = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
twentyfirst_century = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
# months indexes
months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

def PeselValidation(pesel):
    p=[]

    for char in pesel:
        p.append(int(char))

    sum_pesel=p[0]*9+p[1]*7+p[2]*3+p[3]*1+p[4]*9+p[5]*7+p[6]*3+p[7]*1+p[8]*9+p[9]*7
    sum_con=sum_pesel%10

    def DaysCheck(year, month, day):

        year=getPeselYear(pesel)
        month=pesel[2:4]
        day=pesel[4:6]

        if (yesr % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if year < 1800 or year > 2100:
            raise ValueError('Niepoprawny rok')

        if month not in months:
            raise ValueError('Niepoprawny miesiac')

        if day < 0 or day > days[month - 1]:
            raise ValueError('Niepoprawna ilosc dni')

        return True

    return sum_con==int(pesel[-1]) and len(pesel)==11

def PeselInfo(pesel):
    if PeselValidation(pesel) is False:
        raise ValueError('To nie jest poprawny pesel!')
    #dictionary with pesel months as keys and number of months as values
    dictionary={}

    def addKeyValue(dictionary,keys):
        dictionary.update(dict(zip(keys,months)))

    addKeyValue(dictionary,nineteenth_century)
    addKeyValue(dictionary,twentieth_century)
    addKeyValue(dictionary, twentyfirst_century)


    def getPeselYear(pesel):
        pesel_month=pesel[2:4]
        pesel_year=pesel[0:2]
        if pesel_month in nineteenth_century:
            pesel_full_year='18'+pesel_year
        elif pesel_month in twentieth_century:
            pesel_full_year='19'+pesel_year
        else:
            pesel_full_year='20'+pesel_year
        return pesel_full_year


    def formatMonth(month):
        if len(month)==1:
            full_month='0'+month
        return full_month


    year=getPeselYear(pesel)
    month=formatMonth(dictionary[pesel[2:4]])
    day=pesel[4:6]
    full_birth_date=year+'-'+month+'-'+day

#validation sex - Famele or Male
    def FemaleOrMale(pesel):
        pesel_sex=pesel[9]
        if int(pesel_sex)%2==0:
            pesel_sex='Female'
        else:
            pesel_sex='Male'
        return pesel_sex

    sex=FemaleOrMale(pesel)


    info={}
    info['pesel']= pesel
    info['date_of_birth']= full_birth_date
    info['sex']= sex
    return info