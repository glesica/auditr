--
-- Database schema for Auditr app
-- Note: tables are dropped if they exist!
--

--
-- Software products / versions that have been observed
--

DROP TABLE IF EXISTS applications;
CREATE TABLE applications (
    application_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    application_name VARCHAR(128) NOT NULL,
    application_vendor VARCHAR(128) NOT NULL,
    application_version VARCHAR(128) NOT NULL
)
;

--
-- Computers that have been audited
--

DROP TABLE IF EXISTS computers;
CREATE TABLE computers (
    computer_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    computer_name VARCHAR(15) NOT NULL
)
;

--
-- Observed software installations
--

DROP TABLE IF EXISTS installations;
CREATE TABLE installations (
    installation_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    computer_id INTEGER NOT NULL,
    application_id INTEGER NOT NULL,
    audit_date DATE NOT NULL
)
;
