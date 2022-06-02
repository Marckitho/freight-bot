def rodonaves():
    # Imports
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.alert import Alert
    
    import time
    # import main
    import config as cfg
    import request as rq
    import methods as mt
    import credentials as cr

    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # Constantes
    login = cr.rdUser
    passw = cr.rdPass

    rodoFields = [rq.ufFrom, rq.cityFrom, mt.toStateName(rq.ufTo), mt.cleanStateName(rq.cityTo)]
    selectSource = ['selectUfSource', 'selectCitySource', 'selectUfDestiny1', 'selectCityDestiny2']
    result = []

    # Resultados padrão em caso de erro
    result.append("???") # Preço
    result.append("???") # Prazo
    result.append("") # Erro

    # Conectar com Rodonaves (Logar)
    driver.get("https://cliente.rte.com.br/Quotation/QuotationSimulation")

    # Pegar campos de login
    driver.find_element_by_css_selector("#cpfcnp").clear()
    driver.find_element_by_css_selector("#cpfcnp").send_keys(login)

    driver.find_element_by_css_selector("#passwordToLogin").clear()
    driver.find_element_by_css_selector("#passwordToLogin").send_keys(passw)

    driver.find_element_by_css_selector("#loginSubmit").click()

    # Aguardar o carregamento
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#dropdownQuotation"))
        )
    except NoSuchElementException:
        result[2] = "ERRO: ERRO NO LOGIN"
    except TimeoutException:
        result[2] = "ERRO: ERRO NO LOGIN"
    else:
        # Cotação
        # Ir até cotações
        driver.find_element_by_css_selector("#dropdownQuotation").click()

    # Simule seu frete
    simulate = driver.find_element_by_xpath("//a[contains(text(), 'Simule seu Frete')]")
    simulate.click()

    # time.sleep(3)
    try:
        element = WebDriverWait(driver, 7).until(
            EC.url_to_be("https://cliente.rte.com.br/Quotation/QuotationSimulation")
        )
    except TimeoutException:
        result[2] = "ERRO: LOGIN LONGO"
    else:
        assert driver.current_url == "https://cliente.rte.com.br/Quotation/QuotationSimulation"

    # Na tela de fretes

    # Local
    # Definir IDs
    # driver.execute_script('var btnList = document.querySelectorAll("[data-id]"); for (let index = 0; index < btnList.length; index++) { btnList[index].id = btnList[index].getAttribute("data-id") }; btnList[0].click()')

    # Selecionar
    for i in rodoFields:
        try:
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '{}')]".format(i)))
            )
        except TimeoutException('timeout'):
            result[2] = "ERRO: CIDADE NÃO ENCONTRADA"
        else:
            cmd = 'for (let index = 0; index < spanList.length; index++) {if (spanList[index].innerText == "' +i +'") target = index}; spanList[target].click()'
            driver.execute_script('spanList = document.querySelectorAll("span")')
            driver.execute_script(cmd)

    # Permitir cookies
    driver.find_element_by_xpath("//a[contains(text(), 'Permitir cookies')]").click()

    # Preencher com valores fornecidos
    # Total NF-e
    total_input = driver.find_element_by_id('eletronicInvoiceValue')
    total_input.send_keys(str(rq.total))
    if (rq.total >= 100): # Casas decimais
        total_input.send_keys("00")

    # Tipo de embalagem
    # Abrir caixa
    package_input = driver.find_element_by_id('packageType')
    package_input.click()

    # Selecionar
    driver.find_element_by_xpath("//option[@value='1']").click()

    # Adicionar quantidade de pacotes
    for i in range(len(mt.getPackages()) - 1):
        driver.find_element_by_id('addPack').click()

    for index, i in enumerate(mt.getPackages()):
        driver.find_element_by_id('amountPacks{}'.format(str(index + 1))).send_keys(i[1]) # Número de Pacotes
        driver.find_element_by_id('height{}'.format(str(index + 1))).send_keys(str(cfg.height[i[0]] * i[2])) # Altura
        driver.find_element_by_id('width{}'.format(str(index + 1))).send_keys(str(cfg.width[i[0]])) # Largura
        driver.find_element_by_id('length{}'.format(str(index + 1))).send_keys(str(cfg.length[i[0]])) # Comprimento
        driver.find_element_by_id('weight{}'.format(str(index + 1))).send_keys(str(cfg.weight[i[0]] * i[2])) # Peso

    time.sleep(cfg.checkTime) # Conferir medidas

    # Calcular
    simulate_btn = driver.find_element_by_id('BtnQuotationSimulation')
    simulate_btn.click()

    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "quotation-result-table"))
        )
    finally:
        time.sleep(2)
        # driver.execute_script('l = document.querySelectorAll("td")')
        # for i in range(4):
        #     cmd = 'l[{}].id = "{}"'.format(i, 'result' +str(i))
        #     driver.execute_script(cmd)
        #     result.append(driver.find_element_by_id('result' +str(i)).get_attribute('innerText'))
        final = driver.find_element_by_xpath("//img[@src = '/images/timeline/package_in-route.svg']")
        final = final.find_element_by_xpath("../..")
        final = final.find_elements_by_xpath("//td")
        result[0] = final[1].text
        result[1] = final[3].text
        # time.sleep(55) # Conferir final
    
    # Tratar resultado
    # result.pop(3)
    # result.pop(0)

    return(result)
    driver.close()
    # time.sleep(50)