import mysql.connector
import xlsxwriter
def new_data(query):


    workbook = xlsxwriter.Workbook('/home/ullas/progamming/web_block/student_list12.xlsx')
    worksheet = workbook.add_worksheet()
    node_names=["node0"]
    sql_query=query


    master_lst=[]
    node_id="node0"
    x=mysql.connector.connect(  #ur id
    host="localhost",
    user="root",
    passwd="",#########add ur password
    database=node_id
    )
    mycourser = x.cursor()
    mycourser.execute(sql_query)
    print(type(mycourser))
    for y in mycourser:
        temp=list(y)
        master_lst.append(temp)
    master_tuple=tuple(master_lst)

    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for name, usn ,sub in (master_tuple):
        worksheet.write(row, col,     name)
        worksheet.write(row, col + 1, usn)
        worksheet.write(row, col + 2, sub)
        row += 1

    # Write a total using a formula.


    workbook.close()
