from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import linecache

class Scraping():
    def __init__(self, origin, destiny, date_go, date_back=None) -> None:
        if date_back:
            self.site = f'https://www.decolar.com/shop/flights/results/roundtrip/{origin}/{destiny}/{date_go}/{date_back}/1/0/0/NA/NA/NA/NA/NA?from=SB&di=1-0&reSearch=true'
        else:
            self.site = f'https://www.decolar.com/shop/flights/results/oneway/{origin}/{destiny}/{date_go}/1/0/0/NA/NA/NA/NA?from=SB&di=1-0'
        
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(self.site)
        
        self.element = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'cluster-container')))

        self.file = open('aires.txt', 'r+')
        self.values_formated()

    def values_formated(self):
        for el in self.element:
            for v in el.text.split('\n'):
                if "Adicione" in v or "Ver" in v or "Acumule" in v or "Comprar" in v or "Passaporte Decolar" in v or "ganharia" in v or "Em até" in v or "Preço" in v or "1 Adulto" in v or "Impostos" in v or "Em até" in v or "Voo mais" in v or "Você pode" in v or "você acumularia" in v or "Bagagem" in v or "Classe" in v:
                    pass
                else:
                    self.file.write(f'{v}\n')
            self.file.write(f'***\n')

# c = Scraping('GRU', 'SSA', '2022-08-05')
