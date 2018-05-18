import sqlite3


class Column:
    def __init__(self, name, column_type, is_nullable=False,
                 is_fk=False, ref_table=None):
        self.name = name
        self.column_type = column_type
        self.is_nullable = is_nullable
        self.is_fk = is_fk
        self.ref_table = ref_table

    @property
    def nullable(self):
        return 'NOT NULL' if not self.is_nullable else ''

    @property
    def foreign_key(self):
        if not self.is_fk:
            return ''
        return ",\n FOREIGN KEY ({name}) REFERENCES {ref_table}(ID)".format(
            name=self.name,
            ref_table=self.ref_table
        )

    @property
    def to_sql_string(self):
        return "{name} {column_type} {nullable} {foreign_key}".format(
            name=self.name,
            column_type=self.column_type,
            nullable=self.nullable,
            foreign_key=self.foreign_key
        )


class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    @classmethod
    def create_table(cls, db_name, table_name, columns):

        CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS {table_name} (
    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    {columns}
)
        """.format(table_name=table_name,
                   columns=",\n ".join([c.to_sql_string for c in columns]))

        db = sqlite3.connect(db_name)
        crs = db.cursor()

        crs.execute(CREATE_TABLE_SQL)
        db.commit()
        db.close()



if __name__ == '__main__':
    DB_NAME = 'vehicle_system2.db'
    db = Database(DB_NAME)
    db.create_table(db_name=DB_NAME,
                    table_name='base_user',
                    columns=[
                        Column('user_name', 'text'),
                        Column('email', 'text'),
                        Column('phone_number', 'text'),
                        Column('address', 'text', True)
                    ])
