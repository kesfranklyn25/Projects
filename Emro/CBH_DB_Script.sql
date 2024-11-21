use master;
-- Create Database for Christbay Hospital CBH
DROP DATABASE IF EXISTS CBH;
GO
CREATE DATABASE CBH;
GO

USE CBH;

-- Card Details TABLE
DROP TABLE IF EXISTS tblCard;
GO
CREATE TABLE tblCard
(
  --  RegID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    RegID VARCHAR(50) NOT NULL,
    RegDate DATETIME,
	CardClass varchar(5) NOT NULL,
	CardType varchar(15),
	ShelveNo Varchar(50),
	HMO varchar(50)
	CONSTRAINT PK_RegID PRIMARY KEY (REGID),

);


-- CREATE PATIENT TABLE
DROP TABLE IF EXISTS tblPATIENT;
GO
CREATE TABLE tblPATIENT (
    PATID VARCHAR(50) PRIMARY KEY,
	REGID VARCHAR(50) NOT NULL,
    FName NVARCHAR(50) NOT NULL,
    LName NVARCHAR(50) NOT NULL,
    MName NVARCHAR(50),
    Gender NVARCHAR(10),
    MStatus NVARCHAR(20),
    StateOfOrigin NVARCHAR(50),
    DateOfBirth DATE,
    PhoneNo NVARCHAR(20),
    EmailAddress NVARCHAR(100),
	FOREIGN KEY (REGID) REFERENCES tblCard(REGID)
);

-- CREATE ADDRESS TABLE
DROP TABLE IF EXISTS tblADDRESS;
GO
CREATE TABLE tblADDRESS
(
    AddID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    PATID VARCHAR(50) NOT NULL,
    HouseNo VARCHAR(10),
    StreetName NVARCHAR(255) NOT NULL,
    City NVARCHAR(50),
    State VARCHAR(50),
    PostCode VARCHAR(20),
    Country VARCHAR(20),
    FOREIGN KEY (PATID) REFERENCES tblPATIENT(PATID)
);

-- NEXT OF KIN TABLE
DROP TABLE IF EXISTS tblNEXTOFKIN;
GO
CREATE TABLE tblNEXTOFKIN
(
    NOKID INT IDENTITY(1,1)  NOT NULL PRIMARY KEY,
    PATID VARCHAR(50) NOT NULL,
    nxtFName NVARCHAR(50),
    nxtLName NVARCHAR(50) NOT NULL,
    nxtRelationship VARCHAR(50),
    nxtEmailAddress VARCHAR(100),
    nxtPhoneNo VARCHAR(20),
    FOREIGN KEY (PATID) REFERENCES tblPATIENT(PATID)
);

CREATE TABLE staff(
	Username NVARCHAR(50) NOT NULL PRIMARY KEY,
	RegDate DATETIME2,
	FName NVARCHAR(50),
    LName NVARCHAR(50) NOT NULL,
	[Password] NVARCHAR (255) NOT NULL,
	ModifiedDate DATETIME2,
	DeptID NVARCHAR (20)
);
-- Table to keep track of Card integer ID generation at the frontend
CREATE TABLE tblCardTypeIncrement (
    CardType VARCHAR(50),
    Month INT,
    Year INT,
    LastUsedID INT,
    PRIMARY KEY (CardType, Month, Year)
);
select * from tblPATIENT
select * from tblCard
select * from tblCardTypeIncrement

CREATE INDEX idx_PATID_Address ON tblADDRESS(PATID);
CREATE INDEX idx_PATID_NextOfKin ON tblNEXTOFKIN(PATID);
CREATE INDEX idx_PATID_Card ON tblCard(REGID);

select * from tblCard

select * from tblPATIENT

select * from tblADDRESS

select * from tblNEXTOFKIN

select * from staff;


-- sequence of deletion

delete from tblNEXTOFKIN

delete from tblADDRESS

delete from tblPATIENT

delete from tblCard

delete from staff


SELECT CardClass, count(CardClass) FROM tblCard
    group by CardClass
	

SELECT p.patid, p.gender, c.CardClass, c.CardType FROM
tblPATIENT p
join tblCard c on p.PATID = c.RegID


SELECT p.*, c.*, a.*, n.*
FROM tblPATIENT p
LEFT JOIN tblCard c ON p.RegID = c.RegID
LEFT JOIN tblAddress a ON p.PATID = a.PATID
LEFT JOIN tblNextOfKin n ON p.PATID = n.PATID
WHERE p.PATID = 'FC/1/10/2024'
                

-- Testing RegID

SELECT MAX(CAST(SUBSTRING(PATID, CHARINDEX('/', PATID) + 1, 
        CHARINDEX('/', PATID, CHARINDEX('/', PATID) + 1) - CHARINDEX('/', PATID) - 1) AS INT)) 
        AS LastID 
FROM tblPATIENT 
WHERE PATID LIKE 'FC/%' OR PATID LIKE 'SC/%' OR PATID LIKE 'NHIS/%'
AND SUBSTRING(PATID, CHARINDEX('/', PATID, CHARINDEX('/', PATID) + 1) + 1, 2) = '11' 
AND SUBSTRING(PATID, CHARINDEX('/', PATID, CHARINDEX('/', PATID) + 1) + 4, 4) = '2024'



SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'staff';