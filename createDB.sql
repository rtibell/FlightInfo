create table flightinfo  (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	sid INT NOT NULL,
	aid INT NOT NULL,
	hex CHAR(10),
	fid INT NOT NULL,
	cs CHAR(10),
	alt INT NOT NULL,
	gs INT NOT NULL,
	trk INT NOT NULL,
	lat CHAR(12),
	lan CHAR(12),
	vr INT,
	sq INT,
	alrt INT,
	emer INT,
	spi INT,
	gnd INT,
	created DATETIME,
	updated DATETIME,
	rec_created DATETIME,
	rec_updated DATETIME,
        path_id CHAR(48),
	new_path BOOLEAN) ENGINE=INNODB;


create table aircraft (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	icao24 CHAR(10),
	registration CHAR(10),
	manufacturericao CHAR(32),
	manufacturername CHAR(64),
	model CHAR(32),
	typecode CHAR(10),
	serialnumber CHAR(16),
	linenumber CHAR(10),
	icaoaircrafttype CHAR(6),
	operator CHAR(32),
	operatorcallsign CHAR(20),
	operatoricao CHAR(16),
	operatoriata CHAR(10),
	owner CHAR(32),
	testreg CHAR(10),
	registered CHAR(10),
	reguntil CHAR(10),
	status CHAR(10),
	built CHAR(16),
	firstflightdate CHAR(12),
	seatconfiguration CHAR(10),
	engines CHAR(32),
	modes BOOLEAN,
	adsb BOOLEAN,
	acars BOOLEAN,
	notes CHAR(64),
	categoryDescription CHAR(32)) ENGINE=INNODB;


create table plain (
	name CHAR(32),
	iata CHAR(3),
	icao CHAR(4)) ENGINE=INNODB;


create table airline (
	id INT NOT NULL PRIMARY KEY,
	name CHAR(40),
	alias CHAR(32),
	iata CHAR(2),
	icao CHAR(3),
	callsign CHAR(20),
	country CHAR(32),
	active CHAR(1)) ENGINE=INNODB;


create table airport (
	id INT NOT NULL PRIMARY KEY,
	name CHAR(64),
	city CHAR(32),
	country CHAR(32),
	iata CHAR(3),
	icao CHAR(5),
	latitude CHAR(12),
	longitude CHAR(12),
	altitude INT,
	timezone DECIMAL(5,1),
	dst CHAR(1),
	tz CHAR(20),
	type CHAR(20),
	source CHAR(20)) ENGINE=INNODB;



