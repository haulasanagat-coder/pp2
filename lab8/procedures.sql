-- upsert single user
CREATE OR REPLACE PROCEDURE upsert_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS(SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- batch insert
CREATE OR REPLACE PROCEDURE batch_insert(users TEXT[][])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    invalid_data TEXT[];
    current_name TEXT;
    current_phone TEXT;
BEGIN
    invalid_data := '{}';
    FOR i IN 1..array_length(users, 1) LOOP
        current_name := users[i][1];
        current_phone := users[i][2];

        IF current_phone ~ '^[0-9\-]+$' THEN
            CALL upsert_user(current_name, current_phone);
        ELSE
            invalid_data := array_append(invalid_data, current_name || ':' || current_phone);
        END IF;
    END LOOP;

    RAISE NOTICE 'Invalid entries: %', invalid_data;
END;
$$;

-- delete user
CREATE OR REPLACE PROCEDURE delete_user(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM contacts WHERE name = p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;
    END IF;
END;
$$;