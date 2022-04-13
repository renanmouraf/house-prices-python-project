-- on security database
CREATE TABLE user_history (
    id serial primary key,
    user_id int not null,
    server text,
    endpoint text,
    search_values text,
    ip text,
    charge boolean,
    date_time timestamp default current_timestamp,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

--test insert record
INSERT INTO user_history (
        user_id, 
        endpoint, 
        search_values, 
        ip, 
        charge
    ) 
    VALUES (
        1, 
        '/total/advanced', 
        'company', 
        '192.168.0.1', 
        true
    );
