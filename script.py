# Nhập thư viện và gói cho dự án
import csv
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Mở Firefox và truy cập trang đăng nhập Linkedin
driver = webdriver.Firefox()
url = 'https://www.linkedin.com'
driver.get(url)
sleep(3)

# Nhập tên người dùng (email) và mật khẩu
credential = open('credentials.txt')
line = credential.readlines()
email = line[0]
password = line[1]
sleep(2)

# email
email_field = driver.find_element_by_id('session_key')

# send_keys () để mô phỏng các thao tác gõ phím
email_field.send_keys(email)
sleep(2)

# password 
password_field = driver.find_element_by_id('session_password')

# send_keys () để mô phỏng các thao tác gõ phím
password_field.send_keys(password)
sleep(2)

# xác định vị trí nút gửi đăng nhập
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

# .click () để bắt chước nhấp vào nút đăng nhập
log_in_button.click()
sleep(3)


# phương thức driver.get () sẽ điều hướng đến một trang được cung cấp bởi địa chỉ URL
driver.get('https://www.google.com')
sleep(3)

# Nhập từ khóa tìm kiếm
search = open('search.txt')
line = search.readlines()
skill = line[0]
local = line[1]
page_number = line[2]
keyword = f'site:linkedin.com/in/ AND "{skill}" AND "{local}"'
search_query = driver.find_element_by_name('q')

# send_keys () để mô phỏng các thao tác gõ phím
search_query.send_keys(keyword)
sleep(3)

# .send_keys () để mô phỏng khóa trả về
search_query.send_keys(Keys.RETURN)
sleep(3)

# thu thập thông tin URL của các cấu hình. viết một hàm để trích xuất các URL của một trang
def GetURL():
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    sleep(3)
    profiles = page_source.find_all('div', class_ = 'yuRUbf')
    
    all_profile_URL = []
    for profile in profiles:
        for a in profile.find_all('a'):
            sleep(3)
            profile_URL = a.get('href').replace('vn.','')
            if profile_URL not in all_profile_URL:
                all_profile_URL.append(profile_URL)
    return all_profile_URL

# Điều hướng qua nhiều trang và trích xuất URL hồ sơ của mỗi trang
URLs_all_page = []
for page in range(int(page_number)):
    URLs_one_page = GetURL()
    if len(URLs_one_page) == 0:
        print('''Xin hãy đảm bảo tất cả từ được đánh vần chính xác.
                Hãy thử các từ khóa khác nhau.
                Thử những từ khóa thông thường hơn.
                Hãy thử ít từ khóa hơn
        ''')
        break
    sleep(3)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(3)
    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]')
    sleep(3)
    driver.execute_script("arguments[0].click();", next_button)
    URLs_all_page = URLs_all_page + URLs_one_page
    sleep(3)

# thu thập dữ liệu của 1 hồ sơ Linkedin và ghi dữ liệu vào tệp .CSV
with open('profile_output.csv', 'w',  newline = '') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'College', 'Company', 'Link']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        driver.get(linkedin_URL)
        print('- Truy cập hồ sơ: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info = page_source.find('div',{'class':'display-flex justify-space-between pt2'})
        info_company = page_source.find('h2',{'class':'text-heading-small align-self-center flex-1'})
        info_college = page_source.find('div',{'class':'pv-entity__degree-info'})
        info_exp = page_source.find('div', {'class':'pv-entity__summary-info pv-entity__summary-info--background-section'})
        try:
            name = info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
            print('--- Tên ứng viên: ', name)

            location = info.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip()
            print('--- Khu vực làm việc: ', location)

            title = info.find('div', class_='text-body-medium break-words').get_text().strip()
            print('--- Tiêu đề hồ sơ: ', title)

            company = info_company.find('div', class_='inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp').get_text().strip()
            print('--- Công ty  hiện tại: ', company)

            college = info_college.find('h3', class_='pv-entity__school-name t-16 t-black t-bold').get_text().strip()
            print('--- Học vấn: ', college)

            title_company_exp = info_exp.find('h3', class_='t-16 t-black t-bold').get_text().strip()
            print('--- title_company_exp: ', title_company_exp)

            company_exp = info_exp.find('p', class_='pv-entity__secondary-title t-14 t-black t-normal').get_text().strip()
            print('--- company_exp: ', company_exp)

            time_company_exp = info_exp.find('span', class_='pv-entity__bullet-item-v2').get_text().strip()
            print('--- time_company_exp: ', time_company_exp)             

            writer.writerow({headers[0]:name, headers[1]:title, headers[2]:location, headers[3]:college, headers[4]:company, headers[5]:linkedin_URL})
            print('\n')
        except:
            pass

# nhiệm vụ hoàn thành
print('nhiệm vụ hoàn thành!')
