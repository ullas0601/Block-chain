import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from wit import Wit
import json
import hashlib
from hashlib import *
import mysql.connector
import json
import os
from collections import OrderedDict

import xlsxwriter


firebaseconfig = {
    #add your firebase key here###################
    

}
cred = credentials.Certificate("/home/ullas/progamming/web_block/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()
clouddb = firestore.client()
    #Wit framework access token
access = "UGJ52ABITEAEJ456BUEIWRASBBDNU557"
client = Wit(access)

    #flag_auth to check the authentication fail or sucess
flag_auth = 0
global usn
def admin_check(username,passwd):
    if username=='admin@ait':
        try:
            admin_info=clouddb.collection('admin').document(username).get().to_dict()
        except: 
            return 0
    else:
        return 0
    if admin_info["username"]==username:
        if admin_info["password"]==passwd:
            return 1
        else:
            return 0
    else:
        return 0
    
def hod_check(username,passwd):
    if username=='hod@ait':
        try:
            admin_info=clouddb.collection('hod').document(username).get().to_dict()
        except: 
            return 0
    else:
        return 0
   
    if admin_info["username"]==username:
        if admin_info["password"]==passwd:
            return 1
        else:
            return 0
    else:
        return 0


def authentic(username,passwd):
   

    #configuration of cloudstore  db for different things

      #enter the user name here and user name is usn
    usn = username.upper() 
    email = usn+"@gmail.com"
   
    try:
        auth.sign_in_with_email_and_password(email,passwd)
        r=1
    except:
        r=0
    if r==1:
        return 1
    else:
        return 0


def displaying_of_student_info(usn):

    get_info = clouddb.collection("students").document(usn).get().to_dict()
    name=get_info['name']
    usn=get_info['usn']
    list_of_subjects =[]
    for i in get_info:
        if i == 'selection':
            pass
        elif i =="usn":
            pass
        elif i == 'name':
            pass

        else:
            list_of_subjects.append(get_info[i])

    
    #ide_subjects_availabe = ['d','e','f']
    return name,usn,list_of_subjects,#ide_subjects_availabe

def selsection(ide_selected,usn):
    get_info = clouddb.collection("students").document(usn).get().to_dict()
    #split
    #wit ai
    select_val = get_info.get("selection")
    if select_val == False:
        repeat = True
        ide_short = ide_selected
        lst=ide_short.split('-')
        while(repeat == True):
           
            sub_code=lst[0]
            # Witt AI here
            result = client.message(lst[1])
            result_list = list(result.values())
            result_1 = result_list[2]
            result_2 = list(result_1.values())
            result_3 = result_2[0]
            result_4 = result_3[0]
            ide = result_4["value"]
            var1=clouddb.collection("seats").document(ide).get().to_dict()
            var=var1["seat"]
            repeat=False
            if ide in get_info.values():
                return -1,var   #ide exist
            else:
               return 1,var
    else:
        return 0,-1






#---------**********blockchain*******---------
#block chain
# following creates block
#  function calls
#BLOCKCHAIN_DIR = 'blockchainlist/'
def gethash(prev_block):
        content=clouddb.collection("blocks").document(prev_block).get().to_dict()
        dict1 = OrderedDict(sorted(content.items()))
        content=str(dict1)

        hash_no= hashlib.sha256(content.encode()).hexdigest()
        return hash_no
"""
def check_integrity():
    files = sorted(os.listdir(BLOCKCHAIN_DIR), key= lambda x : int(x))
    result=[]

    for file in files[1:]:
        with open(BLOCKCHAIN_DIR + file) as f:
            block = json.load(f)
        prev_hash = block.get('prev_block').get('hash')
        prev_filename = block.get('prev_block').get('filename')
        actual_hash = gethash(prev_filename)
        if prev_hash==actual_hash:
            res='OK'
        else:
            res='Changed'
        
        result.append({'block': prev_filename , 'result': res})
    return result
"""

#---------**********integrity*******---------
def check_integrity():
    results=[]
    size=len(clouddb.collection("blocks").get())
    prev_block='1'
    
    
    for i in range(2,size):
        content=clouddb.collection("blocks").document(prev_block).get().to_dict()
        dict1 = OrderedDict(sorted(content.items()))
        content=str(dict1)

        hash_no= hashlib.sha256(content.encode()).hexdigest()


        block_hash1=clouddb.collection("blocks").document(str(i)).get().to_dict()
        block_hash=str(block_hash1["hash"])
       
        if block_hash==hash_no:
            res='ok'
            results.append({'block': i , 'result': res})
        else:
            res='Changed'
            results.append({'block': i , 'result': res})
        prev_block=str(int(prev_block)+1)
    return results
        
        
    


#---------**********host database*******---------
#internal database its stores in host computer

#sheesh
def sheesh_database(dicto1):
    l=[]
    for x in dicto1.values():
        l.append(x)
        vals=tuple(l)
    #
    #
    #
    #---------**********testing purpose*******---------
    node_names=["node0",'node1','node2']
    #******BLOCK NUMBER,subject code  SHOULD BE ADDED ASK ULLAS ABOUT IT ******
    sql_query="INSERT INTO Blocks (student_name,Student_usn,ide_selected,subject_code,hashcode,block_no) VALUES(%s,%s,%s,%s,%s,%s)"

    for x in node_names:
        node_id=x
        x=mysql.connector.connect(  #ur id
        host="localhost",
        user="root",
        passwd="Witch06@",             #---------**********host_password_database*******---------

        database=node_id
        )

        mycourser = x.cursor()
        mycourser.execute(sql_query, vals)
        x.commit()

        

    
#---------**********new block function*******---------

def write_block(name, usn , IDE_sub,sub_code):  #creation of new block
    block_count =len(clouddb.collection("blocks").get())
   
    prev_block=str(block_count)
    

    data={
    "name" : name,
    "usn" : usn,
    "IDE_subject" : IDE_sub,
    "subject_codde":sub_code,
    "hash": gethash(prev_block),
    "filename": prev_block
    
    }
    current_block=str(block_count+1)
    sheesh_database(data)
    clouddb.collection("blocks").document(current_block).set(data)
    return check_integrity()      #check this on #############################################

    
    

#---------**********main_block*******---------
def main1(ide_sub,usn,sub_code):
    get_info = clouddb.collection("students").document(usn).get().to_dict()
    return write_block(get_info["name"] , usn , ide_sub,sub_code)
    
    
    #blocks_output has intergrity of blocks#########


    #results=check_integrity()
    #dict={}
    #for i in results:
        #if i['result']=='Changed':
            #print('block '+i['block']+' was '+i['result'])
        #else:
            #print('All okay')   



def block(usn,ide_short):
#getting sub name and sub code
    get_info = clouddb.collection("students").document(usn).get().to_dict()
    lst=ide_short.split('-')
    sub_code=lst[0]
    #wit
    result = client.message(lst[1])
    result_list = list(result.values())
    result_1 = result_list[2]
    result_2 = list(result_1.values())
    result_3 = result_2[0]
    result_4 = result_3[0]
    ide = result_4["value"]
    



    var1=clouddb.collection("seats").document(ide).get().to_dict()
    var=var1["seat"]
    clouddb.collection("students").document(usn).set({"ide_sub": ide, "selection": True}, merge=True)
    blocks_condition=main1(ide,usn,sub_code)
   
    var=var-1
    clouddb.collection("seats").document(ide).update({"seat":var})
    return blocks_condition



########################

############################get hod studentslist
def get_data(dept,query):
    workbook = xlsxwriter.Workbook('student_list2.xlsx')
    worksheet = workbook.add_worksheet()
    node_names=dept
    sql_query=query


    master_lst=[]
    node_id="node0"
    x=mysql.connector.connect(  #ur id
    host="localhost",
    user="root",
    passwd="Witch06@",
    database=node_id
    )
    mycourser = x.cursor()
    mycourser.execute(sql_query)
    
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
