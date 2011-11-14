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
    (2, 'Microsoft Office 2010', 'Microsoft, Inc.', '14.1.0.22'),
    (3, 'Adobe Acrobat Reader', 'Adobe, Inc.', '8.1.4'),
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
    (3, 'computer03')
;

--
-- Audits
--

INSERT INTO audits (
    audit_id,
    computer_id,
    audit_date
) VALUES
    (1, 1, '2011-09-01'),
    (2, 1, '2011-09-15'),
    (3, 1, '2011-10-01'),
    (4, 2, '2011-09-01'),
    (5, 2, '2011-09-15'),
    (6, 2, '2011-10-01'),
    (7, 3, '2011-09-01'),
    (8, 3, '2011-09-15'),
    (9, 3, '2011-10-01')
;

--
-- Installations
--

INSERT INTO installations (
    audit_id,
    application_id
) VALUES 
    (1, 1),
    (1, 4),
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 2),
    (3, 3),
    (3, 6),
    
    (4, 2),
    (4, 3),
    (4, 4),
    (5, 2),
    (5, 3),
    (5, 5),
    (6, 2),
    (6, 3),
    (6, 6),
    
    (7, 2),
    (7, 3),
    (7, 6),
    (8, 2),
    (8, 3),
    (8, 4),
    (9, 2),
    (9, 4)
;



