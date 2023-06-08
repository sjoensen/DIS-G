CREATE TABLE station_lines (
    station VARCHAR,
    line VARCHAR,
    position INT, -- add constraint that position should be between 0 and line.length - 1
    CONSTRAINT pk_station_lines PRIMARY KEY (station, line),
    CONSTRAINT uk_line_position UNIQUE (line, position),
    CONSTRAINT fk_stations FOREIGN KEY(station) REFERENCES stations(name),
    CONSTRAINT fk_lines FOREIGN KEY(line) REFERENCES lines(name)
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