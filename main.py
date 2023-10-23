import time


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

from config import driver



class getXlsx(driver):
    def __init__(self, enum, start, end):
        super().__init__()
        self.enum = enum
        self.start = start
        self.end = end



    def read_txt(self):
        with open('link.txt', mode='r', encoding='UTF-8') as f:
            return f.readlines()


    def get_hierarchy(self):
        hierarchy_webelement = self.driver.find_element(By.CLASS_NAME, 'breadcrumb').find_elements(By.TAG_NAME, 'a')
        hierarchy = [i.text for i in hierarchy_webelement]
        return '/'.join(hierarchy)

    def get_name(self):
        try:
            return self.driver.find_element(By.TAG_NAME, 'h1').text
        except:
            return ''

    def get_description(self):
        try:
            description_webelement = self.driver.find_element(By.CLASS_NAME, 'css-mljsh0').find_elements(By.TAG_NAME, 'li')
            description = [i.text for i in description_webelement]
            return ' '.join(description)
        except:
            return ''


    def get_partnum(self):
        try:
            return ''.join(self.driver.find_element(By.CLASS_NAME, 'css-17luso7').text.split(':')[1])
        except:
            return ''

    def get_price(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, 'css-cv8m5x').text
        except:
            return ''


    def get_advanced_details(self):
        try:
            time.sleep(2)
            detail_webelement = self.driver.find_elements(By.CLASS_NAME, 'css-1yibw5a')
            details = {'Product Details': '', 'Compatible Equipment': '', 'Return Details': '', 'Warranty Information': ''}
            for i in detail_webelement:
                if i.text == 'Product Details':
                    prod_det = self.driver.find_elements(By.CLASS_NAME, 'css-zyb0l3')
                    det_prod = self.driver.find_elements(By.CLASS_NAME, 'css-mf42sb')
                    for r in range(len(prod_det)):
                        details[i.text] += f'{det_prod[r].text}: {prod_det[r].text};'
                elif i.text == 'Compatible Equipment':
                    i.click()
                    self.driver.save_screenshot('123.png')
                    time.sleep(0.7)
                    equipment = self.driver.find_elements(By.CLASS_NAME, 'css-1fz6teg')
                    details[i.text] = ';'.join([r.text for r in equipment])

                elif i.text == 'Return Details':
                    i.click()
                    time.sleep(0.7)
                    return_deatails = self.driver.find_element(By.CLASS_NAME, 'css-1ktezi')
                    details[i.text] = return_deatails.text

                elif i.text == 'Warranty Information':
                    i.click()
                    time.sleep(0.7)
                    details[i.text] = self.driver.find_element(By.CLASS_NAME, 'css-go8jcr').text

            return details
        except Exception as e:
            print(e)
            return {'Product Details': '', 'Compatible Equipment': '', 'Return Details': '', 'Warranty Information': ''}


    def get_img(self, name):
        try:
            imges = self.driver.find_element(By.CLASS_NAME, 'slider-wrapper').find_elements(By.CLASS_NAME, 'imageContainer')
            enum = 1
            img_name = []
            for i in imges:
                img = i.find_element(By.TAG_NAME, 'img').get_attribute('src')
                """ time.sleep(5)
                res = requests.get(img)
                with open(f'img/{name}_{enum}.jpeg', mode='wb') as file:
                    file.write(res.content) """
                img_name.append(img)
                enum += 1
            return '\n'.join(img_name)
            #return 'asdasd'
        except:
            return ''

    def open_page(self):
        items = self.read_txt()
        hierarchy = []
        name = []
        description = []
        partnum = []
        img_name = []
        product_details = []
        compatible_quipment = []
        return_details = []
        warranty_information = []
        price = []

        ite = 0
        for i in items[self.start: self.end]:
            try:
                self.driver.get(i)
                time.sleep(20)
                hierarchy.append(self.get_hierarchy())
                name.append(self.get_name())
                description.append(self.get_description())
                self.driver.save_screenshot('12345.png')
                partnum.append(self.get_partnum().strip())
                price.append(self.get_price())
                img_name.append(self.get_img(str(partnum[ite])))
                print(1)
                time.sleep(2)
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                print(2)
                advanced_detail = self.get_advanced_details()
                print(3)
                product_details.append(advanced_detail['Product Details'])
                compatible_quipment.append(advanced_detail['Compatible Equipment'])
                return_details.append(advanced_detail['Return Details'])
                warranty_information.append(advanced_detail['Warranty Information'])
                ite += 1
            except Exception as e:
                print(e)
                return {'name': name,
                'hierarchy': hierarchy,
                'description': description,
                'partnum': partnum,
                'product_details': product_details,
                'compatible_quipment': compatible_quipment,
                'return_details': return_details,
                'warranty_information': warranty_information,
                'img_name': img_name,
                'price': price}
        self.driver.close()

        return {'name': name,
                'hierarchy': hierarchy,
                'description': description,
                'partnum': partnum,
                'product_details': product_details,
                'compatible_quipment': compatible_quipment,
                'return_details': return_details,
                'warranty_information': warranty_information,
                'img_name': img_name,
                'price': price}

    def xlsx_write(self):
        try:
            self.items = self.open_page()
        finally:
            df = pd.DataFrame({'Наименование': self.items['name'],
                        'Цена': self.items['price'],
                        'Иерархия': self.items['hierarchy'],
                        'Описание': self.items['description'],
                        'Номер детали': self.items['partnum'],
                        'Подробнее о продукте': self.items['product_details'],
                        'Совместимое оборудование': self.items['compatible_quipment'],
                        'Информация о возврате': self.items['return_details'],
                        'Гарантия': self.items['warranty_information'],
                        'Фото': self.items['img_name']})
            df.to_excel(f'info_{self.enum}.xlsx', index=False)

xls = getXlsx(1, 0, 20)
xls.xlsx_write()