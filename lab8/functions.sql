-- search_pattern
CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    WHERE name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- get_contacts_page
CREATE OR REPLACE FUNCTION get_contacts_page(limit_size INT, offset_size INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts
    ORDER BY id
    LIMIT limit_size OFFSET offset_size;
END;
$$ LANGUAGE plpgsql;