--
-- Database schema for Auditr app
-- Note: tables are dropped if they exist!
--

DROP TABLE IF EXISTS installations;
DROP TABLE IF EXISTS audits;
DROP TABLE IF EXISTS computers;
DROP TABLE IF EXISTS applications;

--
-- applications
-- Software products / versions that have been observed
--

CREATE TABLE applications (
    application_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    application_name VARCHAR(128) NOT NULL,
    application_vendor VARCHAR(128) NOT NULL,
    application_version VARCHAR(128) NOT NULL,
    
    UNIQUE INDEX application_characteristics (
        application_name,
        application_vendor,
        application_version
    )
) ENGINE=InnoDB
;

--
-- computers
-- Computers that have been audited
--

CREATE TABLE computers (
    computer_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    computer_name VARCHAR(15) NOT NULL UNIQUE,
    
    INDEX (
        computer_name
    )
) ENGINE=InnoDB
;

--
-- audits
-- Record of software audits submitted
--

CREATE TABLE audits (
    audit_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    audit_date DATE NOT NULL,
    computer_id INTEGER NOT NULL,
    
    FOREIGN KEY fk_computer (computer_id)
        REFERENCES computers (computer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB
;

--
-- installations
-- Observed software installations
--

CREATE TABLE installations (
    installation_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    application_id INTEGER NOT NULL,
    audit_id INTEGER NOT NULL,
    
    FOREIGN KEY fk_application (application_id)
        REFERENCES applications (application_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    FOREIGN KEY fk_audit (audit_id)
        REFERENCES audits (audit_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB
;



