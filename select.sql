SELECT DISTINCT cs, hex, path_id, created FROM `flightinfo` WHERE path_id is not null group by cs;

