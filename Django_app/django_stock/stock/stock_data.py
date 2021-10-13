import pandas as pd
 
class data_about_stock():
    def company(self):
        #ข้อมูลรายชื่อสำหรับขึ้นระบบ 
        #Name คือชื่อสำหรับการดึงข้อมูลจากเว็บ financ Yahoo เพราะต้องใช้ชื่อที่มีเอกลักษณ์
        # SYMBOL ไว้สำหรับแสดงบนระบบ แล้วแต่จะประยุกต์ในการเรียก
        company = [
        {'Name':'JMART.BK','Symbol':'JMART'},
        {'Name':'DELTA.BK','Symbol':'DELTA'},
        {'Name':'ADVANC.BK','Symbol':'ADVANC'},
        {'Name':'ALT.BK','Symbol':'ALT'},
        {'Name':'AIT.BK','Symbol':'AIT'},
        {'Name':'DIF.BK','Symbol':'DIF'},
        {'Name':'DTAC.BK','Symbol':'DTAC'},
        {'Name':'INTUCH.BK','Symbol':'INTUCH'},
        {'Name':'JTS.BK','Symbol':'JTS'},
        {'Name':'SIS.BK','Symbol':'SIS'},
        {'Name':'SYNEX.BK','Symbol':'SYNEX'},
        {'Name':'THCOM.BK','Symbol':'THCOM'},
        {'Name':'TRUE.BK','Symbol':'TRUE'},
        {'Name':'HUMAN.BK','Symbol':'HUMAN'},
        {'Name':'FORTH.BK','Symbol':'FORTH'} ]
        return company
    
    
