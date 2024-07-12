--A
--how much paid each day
CREATE VIEW TotalSum
AS
SELECT ID, Price*BQuantity AS TotalSum
FROM Stock S JOIN dbo.Buying B ON
    S.Symbol = B.Symbol AND S.tDate = B.tDate
GROUP BY ID, BQuantity, Price;


--how much paid for total
CREATE VIEW SumID
AS
SELECT ID, ROUND(SUM(TotalSum),3) AS Totalsum
FROM TotalSum
GROUP BY ID;


--משקיע מגוון
CREATE VIEW WantedInvestors
AS
SELECT DISTINCT B.ID, I.Name
FROM Buying B JOIN Company C ON B.Symbol=C.Symbol JOIN
    Investor I ON B.ID = I.ID
GROUP BY B.ID, tDate, I.Name
HAVING COUNT(DISTINCT Sector)>=6;


--B
--every investor and their sum of stocks for each company
CREATE VIEW SumStocks
AS
SELECT B.ID, Symbol, SUM(BQuantity) AS Sum
FROM Investor I JOIN Buying B ON I.ID = B.ID
GROUP BY B.ID,Symbol;


--companies that was bought from all days (1)
CREATE VIEW BoughtAllDays
AS
SELECT B.Symbol, C.Sector
FROM Buying B JOIN Company C ON B.Symbol=C.Symbol
GROUP BY B.Symbol, C.Sector
HAVING COUNT(DISTINCT B.tDate) = (SELECT COUNT(DISTINCT tDate) FROM Buying);


--(2)
CREATE VIEW PopComp
AS
SELECT DISTINCT Symbol
FROM BoughtAllDays B1
WHERE NOT EXISTS (
    SELECT 1
    FROM BoughtAllDays B2
    WHERE B2.Sector = B1.Sector
      AND B2.Symbol <> B1.Symbol
);


--highest buyer for each company
CREATE VIEW HighestBuyers
AS
SELECT
    RankedSums.ID,
    RankedSums.Symbol,
    RankedSums.TotalQuantity
FROM (
    SELECT
        I.ID,
        B.Symbol,
        SUM(B.BQuantity) AS TotalQuantity,
        RANK() OVER (PARTITION BY B.Symbol ORDER BY SUM(B.BQuantity) DESC) AS rnk
    FROM Investor I
    JOIN Buying B ON I.ID = B.ID
    GROUP BY I.ID, B.Symbol
) AS RankedSums
WHERE rnk = 1;


--C
--how many bought in first day for each company
CREATE VIEW BroughtFirstDay
AS
SELECT Symbol, COUNT(*) AS BuyerNum
FROM Buying B
WHERE tDate = (SELECT MIN(tDate) FROM Stock)
GROUP BY Symbol;


--companies with first day price
CREATE VIEW FirstDayPrice
AS
SELECT *
FROM Stock S
WHERE tDate = (SELECT MIN(tDate) FROM Stock);


--companies with last day price
CREATE VIEW LastDayPrice
AS
SELECT *
FROM Stock S
WHERE tDate = (SELECT MAX(tDate) FROM Stock);


--profitable companies
CREATE VIEW ProfitComp
AS
SELECT FDP.Symbol
FROM FirstDayPrice FDP JOIN LastDayPrice LDP ON
    FDP.Symbol=LDP.Symbol
WHERE LDP.Price>1.06*FDP.Price;