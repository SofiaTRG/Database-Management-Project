from django.shortcuts import render
from .models import Content, Transactions, Investor
from django.db import connection
from datetime import datetime


# Create your views here.
def index(request):
    return render(request, 'index.html')

def query_results(request):
    return render(request, 'query_results.html')

def add_transaction(request):
    return render(request, 'add_transaction.html')

def buying(request):
    return render(request, 'buying.html')

def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def query_results(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Name, Totalsum
            FROM WantedInvestors WI LEFT JOIN SumID SI ON WI.ID=SI.ID
            ORDER BY Totalsum DESC;""")
        query1 = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT PC.Symbol, Name, TotalQuantity
            FROM PopComp PC, HighestBuyers HB, Investor I
            WHERE PC.Symbol=HB.Symbol AND I.ID=HB.ID
            ORDER BY Symbol, Name ASC;""")
        query2 = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT PC.Symbol, COALESCE(BuyerNum, 0) AS BuyerNum
            FROM ProfitComp PC LEFT JOIN BroughtFirstDay BFD ON
            PC.Symbol = BFD.Symbol
            ORDER BY PC.Symbol;""")
        query3 = dictfetchall(cursor)

    return render(request, 'query_results.html',{'query1':query1, 'query2':query2, 'query3':query3})


def add_transaction(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TOP 10 *
            FROM Transactions T
            ORDER BY tDate DESC;""")
        query1 = dictfetchall(cursor)

    if request.method == 'POST' and request.POST:
        new_ID = request.POST["ID"]
        new_Sum = request.POST["Tamount"]
        today = getDateStock()

        # Check if there are existing ID in the Investors table
        if checkID(new_ID) == 0:
            error_message = "Error: This ID does not exist in the database."
            return render(request, 'add_transaction.html', {'query1': query1, 'error_message': error_message})
        # Check if there are existing transactions for today's date
        # if today == getDateTransactions():
        #     error_message = "Error: Transactions for today already exist."
        #     return render(request, 'add_transaction.html', {'query1': query1,'error_message':error_message})

        # if this id already made transaction in the last day
        if checkIDLastDay(new_ID) == 1:
            error_message = "Error: Transactions for today already exist."
            return render(request, 'add_transaction.html', {'query1': query1,'error_message':error_message})

        # new_content = Transactions(today,
        #                            new_ID,
        #                            new_Sum)
        # updaateInvestor(new_ID,new_Sum)

        # new_content.save()

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Transactions(tdate,ID,TAmount) VALUES (%s,%s,%s);""", (today, new_ID, new_Sum))
        # update in Investor table
        updateInvestor(new_ID, new_Sum)


    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TOP 10 *
            FROM Transactions T
            ORDER BY tDate DESC;""")
        query1 = dictfetchall(cursor)

    return render(request, 'add_transaction.html', {'query1': query1})


def buying(request):
    errors = []  # Initialize a list to store errors encountered

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TOP 10 *
            FROM Buying
            ORDER BY tDate DESC, ID DESC , Symbol;""")
        query1 = dictfetchall(cursor)

    if request.method == 'POST' and request.POST:
        new_ID = request.POST["ID"]
        new_Symbol = request.POST["Symbol"]
        new_Quantity = request.POST["BQuantity"]
        today = getDateStock()

        CID = checkID(new_ID)
        CSymbol = checkSymbol(new_Symbol)

        if CID == 0:
            errors.append("Error: This ID does not exist in the database.")

        if CSymbol == 0:
            errors.append("Error: This Company does not exist in the database.")

        if CID != 0 and CSymbol != 0:
            if checkIDAmount(new_ID, calculateSum(new_Symbol, new_Quantity)):
                errors.append("Error: This ID does not have enough money available for this operation.")

            if checkIDLastBuy(new_ID, new_Symbol) == 1:
                errors.append("Error: This ID already bought stocks from this company today.")

        if not errors:  # If there are no errors, proceed with the transaction
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Buying(tdate,ID,Symbol,BQuantity) VALUES (%s,%s,%s,%s);""", (today, new_ID, new_Symbol,
                                                                                             new_Quantity))
            # update in Investor table
            new_Sum = calculateSum(new_Symbol, new_Quantity)
            updateInvestor(new_ID, -new_Sum)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TOP 10 *
            FROM Buying
            ORDER BY tDate DESC, ID DESC , Symbol;""")
        query1 = dictfetchall(cursor)

    return render(request, 'buying.html', {'query1': query1, 'errors': errors})


def getDateStock():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tDate
            FROM Stock
            WHERE tDate = (SELECT MAX(tDate) FROM Stock);""")
        query1 = dictfetchall(cursor)
        lastDay = query1[0]['tDate'].strftime('%Y-%m-%d')
    return lastDay


def getDateTransactions():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tDate
            FROM Transactions
            WHERE tDate = (SELECT MAX(tDate) FROM Transactions);""")
        query1 = dictfetchall(cursor)
        lastDay = query1[0]['tDate'].strftime('%Y-%m-%d')
    return lastDay

def checkIDLastDay(newID):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tDate,ID
            FROM Transactions
            WHERE tDate = (SELECT MAX(tDate) FROM Transactions);""")
        query1 = dictfetchall(cursor)
        for row in query1:
            if str(newID) == str(row['ID']):
                return 1
    return 0

def checkID(newID):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID
            FROM Investor;""")
        query1 = dictfetchall(cursor)
        for row in query1:
            if str(newID) == str(row['ID']):
                return 1
    return 0

def updateInvestor(newID, newSum):
    newAmount = float(newSum)
    newID = str(newID)
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE Investor
            SET Amount = Amount + %s
            WHERE ID = %s;""", (newAmount, newID))
        connection.commit()

def checkSymbol(newSymbol):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Symbol
            FROM Company;""")
        query1 = dictfetchall(cursor)
        for row in query1:
            if str(newSymbol) == str(row['Symbol']):
                return 1
    return 0

def calculateSum(newSymbol, newQuantity):
    newSymbol = str(newSymbol)
    newDate = getDateStock()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Price
            FROM Stock
            WHERE tDate = %s AND Symbol = %s;""", (newDate, newSymbol))
        query1 = dictfetchall(cursor)
        price = float(query1[0]['Price'])
        # print("Price:", price)
        # print("newQuantity:", newQuantity)
    return price*float(newQuantity)

def checkIDAmount(newID, totalSUM):
    newID = str(newID)
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT Amount
                FROM Investor
                WHERE ID = %s;""", (newID,))
        query1 = dictfetchall(cursor)
        return float(totalSUM) > float(query1[0]['Amount'])

def checkIDLastBuy(newID, newSymbol):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, Symbol
            FROM Buying
            WHERE tDate = (SELECT MAX(tDate) FROM Buying);""")
        query1 = dictfetchall(cursor)
        for row in query1:
            if str(newID) == str(row['ID']) and str(newSymbol) == str(row['Symbol']):
                return 1
    return 0