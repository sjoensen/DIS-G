CREATE TABLE editors (
    login_name TEXT PRIMARY KEY,
    FOREIGN KEY (login_name) REFERENCES users (login_name)
)