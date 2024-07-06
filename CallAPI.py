import gspread
import datetime as dt
import pandas as pd
import IPython.display as display
gs = gspread.service_account("cre.json")
sht = gs.open_by_url('https://docs.google.com/spreadsheets/d/1Rt0iD5R2f46vpD3pGnc3gNfdgBfc8Dq-3jBBQfvWZsI/edit#gid=974746864')
wks = sht.get_worksheet(2) ## search result table
wks_sv = sht.get_worksheet(5) ## member table
query_wks = sht.get_worksheet(4)

process_wks = sht.get_worksheet(7) ## process trade wks

log_wks = sht.get_worksheet(6) ## 

store_wks = sht.get_worksheet(1)

# test_status = test_wks.update_cell()

# display book stored
def store():
    selected_columns = [0, 3, 4, 5, 6, 7, 8, 9,23]
    temp_result = []
    title = ['ID','Chỉ số ISBN','DDC','Tác giả','Năm Xb','Tên sách','Nơi xb','Nhà xb','Trích dẫn']
    store_list = store_wks.get_all_values()
    filted_data = [[row[i] for i in selected_columns ] for row in store_list[1:]]

    for row in filted_data:
        temp_result.append(row)

    result = pd.DataFrame(temp_result)
    result.columns=title
    return result

# update param to param table (search) col F
def TimSach(book_name):
    query_wks.update_cell(1,6,book_name)
    data_list = pd.DataFrame(wks.get_all_records())
 
    # a = display.display(data_list)
    return data_list

# update param to param table col  E, G
def MuonSach(mssv, bookid):
    query_wks.update_cell(1,5,mssv)
    query_wks.update_cell(1,7,bookid)

# display search result 
def SearchResult():
    data_list = pd.DataFrame(wks.get_all_records())
 
    a = display.display(data_list)
    
# need pandas dataframe to show data in table (maybe)

def AddMember(member):
    target = wks_sv.find(member[0])
    if(target == None):
        wks_sv.append_row(member)
        return 1
    else:
        return -1

def RemoveMember(id):
    target = wks_sv.find(id)
    if(target != None):
        wks_sv.delete_rows(target.row)
        return 1
    else:
        return -1

# update record to log table
def Record(svid, bookid: str):
    query_wks.update_cell(1,1,svid)
    query_wks.update_cell(1,2,bookid)
    a = process_wks.get_all_values()
    log_wks.append_rows(a)
    c = log_wks.find(bookid)
    b = dt.datetime.now() 
    d = b + dt.timedelta(15)
    log_wks.update_cell(c.row, 6, b.strftime("%x"))
    log_wks.update_cell(c.row, 7, d.strftime("%x"))
    

def Rtn_book( bookid: str):
    c = log_wks.find(bookid)
    log_wks.update_cell(c.row, 8 , "Chờ")

# search member from log table
def memfromlog(id):
    row  = log_wks.find(id)
    memberid = log_wks.cell(row=row.row,col=1).value
    book_name = log_wks.cell(row=row.row, col=4).value
    a = wks_sv.find(memberid)
    email = wks_sv.cell(row=a.row, col= 5).value
    user = wks_sv.cell(row = a.row, col = 2).value
    info = []
    info.append(email)
    info.append(user)
    info.append(book_name)
    return info

# update status in log
def update_log(bookid: str, status: str):
    id = log_wks.find(bookid)
    log_wks.update_cell(id.row,8,f"{status}")

# return transaction history
def log():
    log_list = pd.DataFrame(log_wks.get_all_records())
    return log_list
    
# find member from member table by ID
def find_member(id):
    a = []
    temp = wks_sv.find(id)
    if(temp != None):
        name_book = process_wks.cell(1,4).value
        name_member = process_wks.cell(1,2).value
        email_member = wks_sv.cell(temp.row,5).value
        a.append(email_member)
        a.append(name_book)
        a.append(name_member)
        return a
    else:
        return a

# return DF of book has status = "Chờ xử lí"
def ret():
    log_list = log_wks.findall("Chờ")
    result = []
    for item in log_list:
        a = log_wks.row_values(item.row)
        result.append(a)
    a = pd.DataFrame(result,columns=['ID Sinh viên', 'Họ và tên','Đơn vị','Tên sách','ID sách','Ngày mượn','Ngày trả', 'Tình trạng'])
    return a


def member():
    mem_list = pd.DataFrame(wks_sv.get_all_records())
    return mem_list


