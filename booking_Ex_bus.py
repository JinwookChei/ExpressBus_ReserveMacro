from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
import time

url = "https://www.kobus.co.kr/main.do"

#-----------------------------------------------------------------------------------

# 출발역 입력
depart_station = "서울경부"
# 도착역 입력 
arrival_station = "평택용이동"

# 날짜 입력
# ex) "8", "12", "23" - 문자열 
booking_month = "1"
booking_day = "22"

# 출발 시간 입력
# ex) : "07 : 30" - 문자열
# ex) : "21 : 50"
booking_time = "23 : 30"

# 예약할 좌석 수 입력
# ex) 3 - 숫자
booking_seat_cnt = 1
#-----------------------------------------------------------------------------------------------------
# Code 시작

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
driver.find_element(By.ID, "terminalSearch").send_keys(depart_station)
driver.find_element(By.ID, "terminalSearch").send_keys(Keys.ENTER)

time.sleep(0.5)
driver.find_element(By.ID, "terminalSearch").click()
driver.find_element(By.ID, "terminalSearch").send_keys(arrival_station)
driver.find_element(By.ID, "terminalSearch").send_keys(Keys.ENTER)

driver.find_element(By.CLASS_NAME, "ui-datepicker-trigger").click()

#-------------------------------------------------------------------------------------------------------
# 예매 날짜 및 시간 조회

time.sleep(0.5)
while(True):
    date_month = driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
    if date_month == booking_month: 
        break
    else:
        driver.find_element(By.CSS_SELECTOR, "[data-handler='next']").click()


date_day = driver.find_elements(By.CLASS_NAME, "ui-state-default")

for i in date_day:
    if(booking_day == i.text):
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
        if(booking_time == i.text):
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

for i in range(booking_seat_cnt):
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

