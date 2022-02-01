from sqlite3 import *
class Db:
    def __init__(self,Db_Name):
        self.Db_Name = Db_Name
        
    def Db_Connection(self):
        try:
            con = connect(str(self.Db_Name) + '.db')
            return con
        except Error:
            print(Error)

    def Db_Add(self,table_name,table_columns_values,con):
        row = self.getTableInfo(table_name,con)
        execute_string="INSERT INTO [" + table_name + "] VALUES("
        for i in row:
            execute_string += "?, " 
        length = len(execute_string)
        execute_string = execute_string[:length-2] + execute_string[length:]
        execute_string+= ");"
        cur = con.cursor()
        for i in table_columns_values:
            cur.execute(execute_string,i)
            con.commit()

    def Db_Table_Create(self,table_name,table_parametrs,con):
        execute_string = "CREATE TABLE IF NOT EXISTS [" + str(table_name) + "]("
        for column_name in table_parametrs:
            execute_string += "[" + column_name + "] " + table_parametrs[column_name] + ", "
        length = len(execute_string)
        execute_string = execute_string[:length-2] + execute_string[length:]
        execute_string += ");"
        cur = con.cursor()
        cur.execute(execute_string)
        con.commit()

    def Db_Show(self,table_name,con):
        cur = con.cursor()
        cur.execute("SELECT * FROM [%s]" % table_name)
        con.commit()
        return cur.fetchall()

    def Db_Delete(self,table_name,id,con):
        try:
            row = self.getTableInfo(table_name,con)
            cur = con.cursor()
            for i in id:
                execute_string = "DELETE FROM [" + table_name + "] WHERE [" + str(row[0][1]) + "] = " + str(i);
                cur.execute(execute_string);
                con.commit()
        except Error:
            pass

    def Db_Update(self,table_name,data,con):
        row = self.getTableInfo(table_name,con)
        cur = con.cursor()
        execute_string = "UPDATE [" + table_name + "] SET "
        k = 0
        for i in row:
            if i[0] == "INT":
                execute_string += "[" + str(i[1]) + "] = " + str(data[k]) + ", "
                k+=1
            else:
                execute_string += "[" + str(i[1]) + "] = '" + str(data[k]) + "', "
                k+=1
        length = len(execute_string)
        execute_string = execute_string[:length-2] + execute_string[length:]
        execute_string += " WHERE " + str(row[0][1]) + " = " + str(data[0])
        cur.execute(execute_string);
        con.commit()

    def getTableInfo(self,table_name,con):
        execute_string = "PRAGMA table_info('" + table_name + "')"
        cur = con.cursor()
        cur.execute(execute_string);
        con.commit()
        return cur.fetchall();
