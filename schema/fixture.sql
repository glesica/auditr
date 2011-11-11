--
-- Test fixtures for Auditr app
--

--
-- Applications
--

INSERT INTO applications (
    application_id,
    application_name,
    application_vendor,
    application_version
) VALUES 
    (1, 'Microsoft Office 2007', 'Microsoft, Inc.', '12.0.1'),
    (2, 'Adobe Acrobat Reader', 'Adobe, Inc.', '8.1.4'),
    (3, 'Microsoft Office 2010', 'Microsoft, Inc.', '14.1.0.22'),
    (4, 'Mozilla Firefox', 'Mozilla, Inc.', '5.0'),
    (5, 'Mozilla Firefox', 'Mozilla, Inc.', '6.0'),
    (6, 'Mozilla Firefox', 'Mozilla, Inc.', '7.0')
;

--
-- Computers
--

INSERT INTO computers (
    computer_id,
    computer_name
) VALUES 
    (1, 'computer01'),
    (2, 'computer02'),
    (3, 'computer03'),
    (4, 'computer04'),
    (5, 'computer05'),
    (6, 'computer06'),
    (7, 'computer07'),
    (8, 'computer08'),
    (9, 'computer09')
;

--
-- Installations
--

INSERT INTO installations (
    computer_id,
    application_id,
    audit_date
) VALUES 
    (1, 1, '2011-11-10'),
    (1, 1, '2011-11-09'),
    (1, 2, '2011-11-10'),
    (1, 2, '2011-11-09'),
    (1, 6, '2011-11-10'),
    (1, 4, '2011-11-09'),
    (2, 3, '2011-11-10'),
    (2, 1, '2011-11-08'),
    (2, 4, '2011-11-08'),
    (2, 4, '2011-11-10'),
    (3, 5, '2011-11-10'),
    (3, 4, '2011-11-07'),
    (3, 3, '2011-11-10'),
    (3, 1, '2011-11-07'),
    (4, 4, '2011-11-08'),
    (4, 5, '2011-11-09'),
    (4, 6, '2011-11-10'),
    (4, 2, '2011-11-08'),
    (4, 2, '2011-11-09'),
    (4, 2, '2011-11-10')
;



