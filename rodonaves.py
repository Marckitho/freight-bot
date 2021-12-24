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
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.alert import Alert
    
    import time
    # import main
    import config as cfg
    import request as rq
    import methods as mt

    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # Constantes
    login = cfg.rdUser
    passw = cfg.rdPass

    rodoFields = [rq.ufFrom, rq.cityFrom, mt.toStateName(rq.ufTo), mt.cleanStateName(rq.cityTo)]
    result = []

    # Conectar com Rodonaves (Logar)
    driver.get("https://cliente.rte.com.br/Quotation/QuotationSimulation")

    # Pegar campos
    login_input = driver.find_element_by_id('cpfcnp')
    pass_input = driver.find_element_by_id('passwordToLogin')
    confirm_btn = driver.find_element_by_id('loginSubmit')

    # Preencher
    login_input.send_keys(login)
    pass_input.send_keys(passw)

    confirm_btn.click()

    # Aguardar o carregamento
    time.sleep(2)

    # Fechar pop-up
    popup = driver.find_element_by_id('popUpRTE')
    popup.click()

    # Ir até cotações
    # Cotação
    quot_btn = driver.find_element_by_id('dropdownQuotation')
    quot_btn.click()

    # Simule seu frete
    simulate = driver.find_element_by_xpath("//a[text()='Simule seu Frete']")
    simulate.click()

    time.sleep(3)

    # Na tela de fretes

    # Local
    # Definir IDs
    # driver.execute_script('var btnList = document.querySelectorAll("[data-id]"); for (let index = 0; index < btnList.length; index++) { btnList[index].id = btnList[index].getAttribute("data-id") }; btnList[0].click()')

    # Selecionar
    for i in rodoFields:
        cmd = 'for (let index = 0; index < spanList.length; index++) {if (spanList[index].innerText == "' +i +'") target = index}; spanList[target].click()'
        driver.execute_script('spanList = document.querySelectorAll("span")')
        driver.execute_script(cmd)
        time.sleep(1)

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

    # time.sleep(35) # Conferir medidas

    # Calcular
    simulate_btn = driver.find_element_by_id('BtnQuotationSimulation')
    simulate_btn.click()

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "quotation-result-table"))
        )
    finally:
        time.sleep(2)
        driver.execute_script('l = document.querySelectorAll("td")')
        for i in range(4):
            cmd = 'l[{}].id = "{}"'.format(i, 'result' +str(i))
            driver.execute_script(cmd)
            result.append(driver.find_element_by_id('result' +str(i)).get_attribute('innerText'))
        # time.sleep(55) # Conferir final
    
    # Tratar resultado
    result.pop(3)
    result.pop(0)

    return(result)
    driver.close()
    # time.sleep(50)