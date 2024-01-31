from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton

url = "https://www.kobus.co.kr/main.do"

class InputUI(QWidget):
    def __init__(self):
        super().__init__()

        self.depart_station = QLineEdit()
        self.arrival_station = QLineEdit()
        self.booking_month = QLineEdit()
        self.booking_day = QLineEdit()
        self.booking_time = QLineEdit()
        self.booking_seat_cnt = QLineEdit()

        self.init_ui()
    
    #UI 생성
    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("출발역 입력 : "))
        layout.addWidget(QLabel("Ex)  서울경부"))
        layout.addWidget(self.depart_station)

        layout.addWidget(QLabel("도착역 입력 : " ))
        layout.addWidget(QLabel("Ex) 평택용이동" ))
        layout.addWidget(self.arrival_station)

        layout.addWidget(QLabel("날짜 입력 (월) : "))
        layout.addWidget(QLabel("Ex) \"1\" \"12\"" ))
        layout.addWidget(self.booking_month)

        layout.addWidget(QLabel("날짜 입력 (일) : "))
        layout.addWidget(QLabel("Ex) \"1\" \"12\"" ))
        layout.addWidget(self.booking_day)

        layout.addWidget(QLabel("출발 시간 입력 : "))
        layout.addWidget(QLabel("Ex) \"08 : 20\" <- 숫자 중간 띄어쓰기사용!" ))
        layout.addWidget(self.booking_time)

        layout.addWidget(QLabel("예약할 좌석 수 입력 : "))
        layout.addWidget(QLabel("Ex) \"1\"" ))
        layout.addWidget(self.booking_seat_cnt)

        layout.addWidget(QLabel(""))
        submit_button = QPushButton("RUN")
        submit_button.clicked.connect(self.RUN_clicked)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle('Booking EX BUS')
        self.show()

    def RUN_clicked(self):
        self.depart_station = self.depart_station.text()
        self.arrival_station = self.arrival_station.text()
        self.booking_month = self.booking_month.text()
        self.booking_day = self.booking_day.text()
        self.booking_time = self.booking_time.text()
        self.booking_seat_cnt = self.booking_seat_cnt.text()
        self.booking_seat_cnt = int(self.booking_seat_cnt)
        
        self.close()
        self.Booking()

    def Booking(self):
        # Chrome 설정
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)

        # 드라이브 get
        driver.get(url)
        driver.implicitly_wait(10)

        #-------------------------------------------------------------------------------------------------------

        # 고속버스 예매 출발역 도착역 입력 및 조회
        driver.find_element(By.ID, "rotinf").click()
        driver.find_element(By.ID, "readDeprInfoList").click()

        driver.find_element(By.ID, "terminalSearch").click()
        driver.find_element(By.ID, "terminalSearch").send_keys(self.depart_station)
        driver.find_element(By.ID, "terminalSearch").send_keys(Keys.ENTER)

        time.sleep(0.5)
        driver.find_element(By.ID, "terminalSearch").click()
        driver.find_element(By.ID, "terminalSearch").send_keys(self.arrival_station)
        driver.find_element(By.ID, "terminalSearch").send_keys(Keys.ENTER)

        driver.find_element(By.CLASS_NAME, "ui-datepicker-trigger").click()

        #-------------------------------------------------------------------------------------------------------
        # 예매 날짜 및 시간 조회

        time.sleep(0.5)
        while(True):
            date_month = driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
            if date_month == self.booking_month: 
                break
            else:
                driver.find_element(By.CSS_SELECTOR, "[data-handler='next']").click()


        date_day = driver.find_elements(By.CLASS_NAME, "ui-state-default")

        for i in date_day:
            if(self.booking_day == i.text):
                i.click()
                break
        driver.find_element(By.CSS_SELECTOR, "[onclick='fnAlcnSrch();']").click()


        try:
            while(1):
                driver.switch_to.alert.accept()

        except NoAlertPresentException:
            pass

        time.sleep(0.5)

        #-------------------------------------------------------------------------------------------------------
        # 배차 조회 및 새로고침 메크로
        noselect = True

        while(noselect):
            start_times = driver.find_elements(By.CLASS_NAME, "start_time")
            for i in start_times:
                if(self.booking_time == i.text):
                    parent = i.find_element(By.XPATH, "..")
                    if parent.get_attribute("class") == "noselect":
                        driver.find_element(By.CLASS_NAME, "box_refresh").click()
                        time.sleep(0.5)
                        break
                    else:
                        i.click()
                        noselect = False
                        time.sleep(0.5)
                        break

        try:
            while(1):
                driver.switch_to.alert.accept()

        except NoAlertPresentException:
            pass

        time.sleep(0.5)

        #-------------------------------------------------------------------------------------------------------
        # 좌석선택 및 결제창

        driver.find_element(By.CSS_SELECTOR, "[href='#none']").click()
        check_seats = []

        for i in range(self.booking_seat_cnt):
            driver.find_element(By.XPATH, "//*[@id='seatChcPage']/div/div[1]/div[2]/div[3]/div[1]/ul/li[1]/div/div/ul/li[1]").click()
            seatBoxs = driver.find_elements(By.CLASS_NAME, "seatBox " )

            for j in seatBoxs:
                if("disabled" not in j.get_attribute("class") and (j.text not in check_seats)):
                    check_seats.append(j.text)
                    j.click()
                    break

        driver.find_element(By.XPATH, "//*[@id='satsChcCfmBtn']").click()

        while(1):
            time.sleep(10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    input_ui = InputUI()
    sys.exit(app.exec_())