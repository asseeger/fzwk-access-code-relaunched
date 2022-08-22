/*
Author:
Version History:
    1.3: 2022-08-22 changed to be sqlite compatible
    1.2: 2019-04-30 adding System User to have an id for generic loge entries
    1.1: 2019-02-16 changing [Badge]badgeId to concrete id of badge
    1.0: 2019-02-14 Init

*/

DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS badge;
DROP TABLE IF EXISTS person_badge;
DROP TABLE IF EXISTS logEntry;

-- [Person] --
CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL
);
---- INSERT INTO Person
INSERT INTO person (firstname, lastname) VALUES
  ("System", "Admin"),
  ("Pascal", "Steck"),
  ("Andreas", "Seeger"),
  ("Jo", "Stutz")
;

-- [Badge] --
CREATE TABLE badge (
  id INTEGER PRIMARY KEY AUTOINCREMENT, -- using existing badge id as the main id of this table
  isAssigned BOOLEAN NOT NULL CHECK (isAssigned IN (0, 1)), --hacking BOOLEAN as there is no BOOL in SQLITE...
  number INTEGER UNIQUE NOT NULL,
  lastDistribution NOT NULL DEFAULT CURRENT_TIMESTAMP
);
---- INSERT INTO Badge
INSERT INTO badge (id, isAssigned, number)
VALUES
  (157125606304,false,1),
  (584198792543,false,2),
  (279635118494,false,3)
;

-- [PersonBadge] --
CREATE TABLE person_badge (
  personId INTEGER UNIQUE NOT NULL,
  badgeId INTEGER UNIQUE NOT NULL,
  PRIMARY KEY (personId, badgeId),
  FOREIGN KEY (personId) REFERENCES person(id),
  FOREIGN KEY (badgeId) REFERENCES badge(id)
);
---- INSERT INTO PersonBadge
INSERT INTO person_badge VALUES
  (1001,157125606304),
  (1002,584198792543)
;

-- [LogEntry] --
CREATE TABLE logEntry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  personId INTEGER NOT NULL,
  badgeId INTEGER,
  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  message TEXT,
  FOREIGN KEY (personId) REFERENCES person(id),
  FOREIGN KEY (badgeId) REFERENCES badge(id)
);