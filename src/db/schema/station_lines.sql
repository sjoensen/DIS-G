CREATE TABLE station_lines (
    station VARCHAR NOT NULL,
    line VARCHAR NOT NULL,
    position INT NOT NULL, -- add constraint that position should be between 0 and line.length - 1
    PRIMARY KEY (station, line),
    UNIQUE (line, position),
    FOREIGN KEY(station) REFERENCES stations(name),
    FOREIGN KEY(line) REFERENCES lines(name)
);

CREATE FUNCTION check_station_lines_position() RETURNS TRIGGER AS $$
BEGIN
    IF
        NEW.position < (SELECT length
                        FROM lines
                        WHERE name = NEW.line)
        AND NEW.position >= 0
    THEN
        RETURN NEW;
    ELSE
        RAISE EXCEPTION 'Position has to be a value between 0 and length of line - 1.';
    END IF;
END;$$ language plpgsql;

CREATE CONSTRAINT TRIGGER check_station_lines_position_is_valid
AFTER UPDATE OR INSERT
ON station_lines FOR EACH ROW
EXECUTE FUNCTION check_station_lines_position();