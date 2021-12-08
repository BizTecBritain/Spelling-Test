__all__ = ['Database']
__version__ = '1.1.2'
__author__ = 'Alexander Bisland'

import sqlite3
from sqlite3 import Error
from typing import Union, List


class Database:
    def __init__(self, db_file: str) -> None:
        """
        Description: Constructor sets up attributes including objects
        :param db_file: the file of the database to access
        :return: void
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def create_table(self, table: str, fields: Union[list, str]) -> None:
        """
        Description: Function to create a table in the loaded database
        :param table: the table name to add
        :param fields: the fields of the table
        :return: void
        """
        if type(fields) == list:
            fields = ", ".join(fields)
        sql = """ CREATE TABLE IF NOT EXISTS {0} (
                  {1}
                  ); """.format(table, fields)
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def get_headers(self, table: str) -> List[str]:
        """
        Description: Function to get a list of the headers of the table
        :param table: the table name to add
        :return: list[str] - a list of all the headers in the table
        """
        cursor = self.conn.execute('select * from {0};'.format(table))
        return list(map(lambda x: x[0], cursor.description))

    def select(self, table: str, item: Union[str, list], *, where: Union[str, list] = None,
               order_by: Union[str, list] = None, distinct: bool = False, limit: Union[int, str] = -1) -> List[tuple]:
        """
        Description: Function to send a select query to the database
        See: https://www.w3schools.com/sql/sql_select.asp
        :param table: the table name to query
        :param item: the headers from the table of the items that will be reurned See: Database.get_headers
        :param where: [Optional] the items that will be reurned See: Database.get_headers
        :param order_by: [Optional] the way you want the response ordered
                            See: https://www.w3schools.com/sql/sql_orderby.asp
        :param distinct: [Optional] boolean to define if you only want distinct elements returned
                            See: https://www.w3schools.com/sql/sql_distinct.asp
        :param limit: [Optional] an integer defining the number of elements to return (-1 returns all elements)
        :return: list[tuple] - a list of tuples each tuple contains one row
        """
        if type(item) == list:
            item = ", ".join(item)
        if type(where) == list:
            where = ", ".join(where)
        if type(order_by) == list:
            order_by = ", ".join(order_by)
        if distinct:
            sql = '''SELECT DISTINCT {0} FROM {1}'''.format(item, table)
        else:
            sql = '''SELECT {0} FROM {1}'''.format(item, table)
        if where:
            sql += ''' WHERE {0}'''.format(where)
        if order_by:
            sql += ''' ORDER BY {0}'''.format(order_by)
        if limit != -1:
            sql += ''' LIMIT {0}'''.format(str(limit))
        sql += ";"
        return self.submit_sql(sql).fetchall()

    def insert(self, table: str, task: Union[tuple, list, str], *, headers: Union[list, str] = None) -> None:
        """
        Description: Function to send an insert query to the database
        See: https://www.w3schools.com/sql/sql_insert.asp
        :param table: the table name to query
        :param task: the list of values to insert
        :param headers: [Optional] the headers of the table where the values are inserted
                            (required if you dont insert all the values)
        :return: void
        """
        if headers:
            values = '?'
            if type(headers) == list:
                values = ('?,' * len(headers))[:-1]
                headers = ", ".join(headers)
            headers = '('+headers+')'
        else:
            header_names = self.get_headers(table)
            headers = '('+','.join(header_names)+')'
            values = ('?,' * len(header_names))[:-1]
        sql = '''INSERT INTO {0} {1}
                 VALUES({2}); '''.format(table, headers, values)
        try:
            self.submit_sql(sql, task)
        except sqlite3.ProgrammingError:
            header_names = self.get_headers(table)[1:]
            headers = '(' + ','.join(header_names) + ')'
            values = ('?,' * len(header_names))[:-1]
            sql = '''INSERT INTO {0} {1}
                                 VALUES({2}); '''.format(table, headers, values)
            self.submit_sql(sql, task)

    def update(self, table: str, changes: Union[list, str], where: Union[list, str]) -> None:
        """
        Description: Function to send an update query to the database
        See: https://www.w3schools.com/sql/sql_update.asp
        :param table: the table name to add
        :param changes: the changes in the format header1=change1, header2=change2...
        :param where: condition for selecting records to update
        :return: void
        """
        if type(changes) == list:
            changes = ", ".join(changes)
        if type(where) == list:
            where = ", ".join(where)
        sql = '''UPDATE {0}
                 SET {1}
                 WHERE {2}; '''.format(table, changes, where)
        self.submit_sql(sql)

    def submit_sql(self, sql: str, task: Union[list, str, tuple] = None) -> sqlite3.Cursor:
        """
        Description: Run a custom SQL query
        :param sql: the query to run
        :param task: [Optional] the list of values to replace ? in the query
        :return: sqlite3.Cursor - a cursor object so you can handle a response if there is one
        """
        cur = self.conn.cursor()
        if task is not None:
            if type(task) == str:
                task = task.split(",")
                task = [element.strip() for element in task]
            if type(task) == list:
                task = tuple(task)
            cur.execute(sql, task)
        else:
            cur.execute(sql)
        self.conn.commit()
        return cur
