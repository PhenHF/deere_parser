from selenium import webdriver



class driver:
    def __init__(self) -> None:
        self.__options = webdriver.ChromeOptions()
        self.__options.page_load_strategy = 'eager'
        """ self.__options.add_argument('--ignore-certificate-errors-spki-list')
        self.__options.add_argument('--ignore-ssl-errors') """
        self.__options.add_argument('--headless')
        #self.__options.add_argument('--no-sandbox')
        self.__service = webdriver.ChromeService(executable_path='chromedriver/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.__service, options=self.__options)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
        })