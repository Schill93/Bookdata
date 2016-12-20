
def isbn_converter(ISBN):


    while len(ISBN)!= 10:

        print("Please try again and make sure you entered 10 digits.")
        ISBN=int(input("Please enter the 10 digit number again: "))
        continue

    else:

        D1 = 9*1
        D2 = 7*3
        D3 = 8*1
        D4 =int(ISBN[0])*3
        D5 =int(ISBN[1])*1
        D6 =int(ISBN[2])*3
        D7 =int(ISBN[3])*1
        D8 =int(ISBN[4])*3
        D9 =int(ISBN[5])*1
        D10=int(ISBN[6])*3
        D11 = int(ISBN[7])*1
        D12 = int(ISBN[8])*3
        Sum=(D1+D2+D3+D4+D5+D6+D7+D8+D9+D10+D11+D12)
        Mod=Sum%10


        if Mod==0:
            D13=0
        else:
            D13=10-Mod


        ISBN13=str(978)+str(ISBN[:-1])+str(D13)
        return ISBN13

