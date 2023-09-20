GET_TABLES_AND_COLUMNS = """
SELECT
    t.TABLE_NAME,
    c.COLUMN_NAME,
FROM
    INFORMATION_SCHEMA.TABLES AS t
JOIN
    INFORMATION_SCHEMA.COLUMNS AS c ON t.TABLE_NAME = c.TABLE_NAME
WHERE
    t.TABLE_TYPE = 'BASE TABLE'
ORDER BY
    t.TABLE_NAME, c.ORDINAL_POSITION;
"""


GET_TABLES_AND_COLUMNS_WITH_DATA = """
SELECT
    t.TABLE_NAME,
    c.COLUMN_NAME,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.IS_NULLABLE,
CASE WHEN ind.index_id IS NOT NULL THEN 'YES' ELSE 'NO' END AS IsUnique
FROM
    INFORMATION_SCHEMA.TABLES AS t
JOIN
    INFORMATION_SCHEMA.COLUMNS AS c ON t.TABLE_NAME = c.TABLE_NAME
LEFT JOIN
    sys.indexes AS ind ON ind.object_id = OBJECT_ID(t.TABLE_NAME)
    AND ind.is_unique = 1 AND ind.index_id IN (
        SELECT
            ic.index_id
        FROM
            sys.index_columns AS ic
        WHERE
            ic.object_id = OBJECT_ID(t.TABLE_NAME)
            AND ic.column_id = COLUMNPROPERTY(
            OBJECT_ID(t.TABLE_NAME), c.COLUMN_NAME, 'ColumnId'
            )
    )
WHERE
    t.TABLE_TYPE = 'BASE TABLE'
ORDER BY
    t.TABLE_NAME, c.ORDINAL_POSITION;
"""


GET_REFERENCES = """
SELECT
    f.name AS ForeignKeyName,
    tp.name AS ParentTable,
    tr.name AS ReferencedTable,
    cp.name AS ParentColumn,
    cr.name AS ReferencedColumn
FROM
    sys.foreign_keys AS f
INNER JOIN
    sys.tables AS tp ON f.parent_object_id = tp.object_id
INNER JOIN
    sys.tables AS tr ON f.referenced_object_id = tr.object_id
INNER JOIN
    sys.foreign_key_columns AS fc ON f.object_id = fc.constraint_object_id
INNER JOIN
    sys.columns AS cp ON fc.parent_object_id = cp.object_id
    AND fc.parent_column_id = cp.column_id
INNER JOIN
    sys.columns AS cr ON fc.referenced_object_id = cr.object_id
    AND fc.referenced_column_id = cr.column_id
ORDER BY
    tp.name, tr.name;
"""


GET_INDEXES = """
SELECT
    t.name AS TableName,
    i.name AS IndexName,
    c.name AS ColumnName
FROM
    sys.indexes AS i
JOIN
    sys.index_columns AS ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN
    sys.tables AS t ON i.object_id = t.object_id
JOIN
    sys.columns AS c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE
    t.type = 'U'
ORDER BY
    t.name, i.name, ic.key_ordinal;
"""


GET_STORED_PROCEDURES = """
SELECT
    ROUTINE_NAME,
    ROUTINE_TYPE,
    CREATED,
    LAST_ALTERED
FROM
    INFORMATION_SCHEMA.ROUTINES
WHERE
    ROUTINE_TYPE IN ('PROCEDURE', 'FUNCTION');
"""


GET_VIEWS = """
SELECT
    TABLE_NAME AS ViewName,
    VIEW_DEFINITION
FROM
    INFORMATION_SCHEMA.VIEWS;
"""


GET_PRIMARY_KEYS = """
SELECT
    t.name AS TableName,
    c.name AS ColumnName
FROM
    sys.tables AS t
JOIN
    sys.indexes AS i ON t.object_id = i.object_id
JOIN
    sys.index_columns AS ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN
    sys.columns AS c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE
    i.is_primary_key = 1
ORDER BY
    t.name, c.name;
"""
