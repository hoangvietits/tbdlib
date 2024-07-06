import yagmail
import pyqrcode
import datetime as dt
yag = yagmail.SMTP("bigboss241200@gmail.com", "fvio fnev ldpw ctee")

def createMember(mssv, receiver):
    qr = pyqrcode.create(mssv)
    qr.png("./QR_Reader/mssv.png")
    to = receiver
    subject = "Welcome to TBD Library."
    body = "Đây là mã QR cá nhân của bạn, mã này được sử dụng để mượn hoặc trả sách tại thư viện."
    file_path = "./QR_Reader/mssv.png"

    yag.send(to=to,subject=subject, contents=body, attachments=file_path)

def brw_book_mail(receiver, book_name, user ):
    time = dt.datetime.now()
    deadline = time + dt.timedelta(days=10)
    to = receiver
    subject = "Muợn sách thành công"
    body = f""" Xin chào {user}
    Thư viện TBD thông báo: bạn đã mượn sách {book_name} tại thư viện lúc {time.strftime("%H:%M:%S %d/%m/%Y")}.
    Thời hạn trả sách là: {deadline.strftime("%d/%m/%Y")}. Vui lòng trả sách đúng theo thời hạn quy định, xin cảm ơn!"""
    yag.send(to=to,subject=subject, contents=body, attachments=None)    


def return_book_succes(reiceiver, user, book_name):
    to = reiceiver
    time = dt.datetime.now()
    subject = "Trả sách thành công"
    body = f"""Xin chào {user}
    Thư viện TBD thông báo: sách {book_name} bạn mượn đã được trả thành công.
    Xin cảm ơn vì đã đọc sách tại thư viện. Thư viện TBD rất mong được gặp lại bạn."""
    yag.send(to=to,subject=subject,contents=body,attachments=None)

def return_book_fail(reiceiver, user, book_name):
    to = reiceiver
    time = dt.datetime.now()
    subject = "Trả sách không thành công"
    body = f"""Xin chào {user}.
    Thư viện TBD thông báo: quá trình trả sách "{book_name}" xảy ra sự cố. Vui lòng liên hệ với thư viện để biết thêm chi tiết."""
    yag.send(to=to,subject=subject,contents=body,attachments=None)