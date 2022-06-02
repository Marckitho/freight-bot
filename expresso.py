def expresso():
    # Imports
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.common.exceptions import NoSuchElementException, TimeoutException
    
    import time
    from datetime import date

    import config as cfg
    import request as rq
    import methods as mt
    import credentials as cr

    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # Constantes
    login = cr.exUser
    passw = cr.exPass

    uf = mt.toStateAcronym(rq.ufTo)
    city = mt.cleanStateName(rq.cityTo)

    result = []

    # Resultados padrão em caso de erro
    result.append("???") # Preço
    result.append("???") # Prazo
    result.append("") # Erro

    # Conectar com Rodonaves (Logar)
    driver.get("https://intranet2.expressosaomiguel.com.br/")

    # Logar
    driver.find_element_by_id('formLogin:username').send_keys(login)
    driver.find_element_by_id('formLogin:password').send_keys(passw)
    # driver.find_element_by_id('formLogin:j_idt25').click()
    driver.find_element_by_xpath('//span[contains(text(), "Login")]').click()

    # Esperar logar
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".layout-menu-button"))
        )
    except NoSuchElementException:
        result[2] = "ERRO: LOGIN LENTO"
        return result
    except  TimeoutException:
        result[2] = "ERRO: LOGIN LENTO"
        return result
    else:
        # Negar atualizar perfil
        driver.execute_script('PF("dlgInformarPerfil").hide()')

    # Ir para as cotações
    driver.find_element_by_class_name('layout-menu-button').click()
    time.sleep(0.5)
    driver.find_element_by_id('menuform:menu-tudo_1_0').click()

    # Definir cidade
    driver.find_element_by_id('form_cotacao:cidadeDestino').click()
    time.sleep(1)
    # driver.find_element_by_xpath("//li[text()='{} / {}']".format(city, uf)).click()
    cmd = "//li[text()='{} / {}']".format(city, uf)

    # Busca pela cidade
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, cmd))
        )
    except NoSuchElementException:
        result[2] = "ERRO: CIDADE NÃO ENCONTRADA"
        return result
    except  TimeoutException:
        result[2] = "ERRO: CIDADE NÃO ENCONTRADA"
        return result
    else:
        driver.find_element_by_xpath(cmd).click()

    # time.sleep(25)

    # Preencher gerais
    # Total da Nota
    driver.find_element_by_id('form_cotacao:valor_nota_input').clear()
    driver.find_element_by_id('form_cotacao:valor_nota_input').send_keys(rq.total)

    # Peso total
    driver.find_element_by_id('form_cotacao:peso_input').clear()
    driver.find_element_by_id('form_cotacao:peso_input').send_keys(mt.getTotalWeight())

    # Pacotes
    for i in mt.getPackages():
        # Altura
        driver.find_element_by_id('form_cotacao:alturaMedidas_input').clear()
        driver.find_element_by_id('form_cotacao:alturaMedidas_input').send_keys(mt.convertToMeters(cfg.height[i[0]] * i[2]))
        # Largura
        driver.find_element_by_id('form_cotacao:larguraMedidas_input').clear()
        driver.find_element_by_id('form_cotacao:larguraMedidas_input').send_keys(mt.convertToMeters(cfg.width[i[0]]))
        # Comprimento
        driver.find_element_by_id('form_cotacao:profundidadeMedidas_input').clear()
        driver.find_element_by_id('form_cotacao:profundidadeMedidas_input').send_keys(mt.convertToMeters(cfg.length[i[0]]))
        # Quantidade
        driver.find_element_by_id('form_cotacao:volumesMedidas').clear()
        driver.find_element_by_id('form_cotacao:volumesMedidas').send_keys(i[1])

        # Confirmar
        driver.execute_script('PrimeFaces.ab({s:"form_cotacao:adicionarMedida",p:"@all",u:"form_cotacao growlMensagem"})')
        time.sleep(1)
        
    # Gerar cotação
    # time.sleep(2)
    #driver.execute_script('PrimeFaces.ab({s:"form_cotacao:j_idt562",u:"growlMensagem form_cotacao:pnlCotacao corpo_pagina",onst:function(cfg){startProcessando();},onco:function(xhr,status,args){stopProcessando();}})')

    time.sleep(cfg.checkTime) # Conferir medidas

    # Busca pelo botão de gerar cotação
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Gerar Cotação")]'))
        )
    except NoSuchElementException:
        result[2] = "ERRO: NÃO FOI POSSÍVEL GERAR A COTAÇÃO"
        return result
    except  TimeoutException:
        result[2] = "ERRO: NÃO FOI POSSÍVEL GERAR A COTAÇÃO"
        return result
    else:
        driver.find_element_by_xpath('//span[contains(text(), "Gerar Cotação")]').click()

    # time.sleep(15)
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Valor Cotação:')]"))
        )
    except TimeoutException:
        print("NÃO PÔDE SER CALCULADO")
    else:
        print("a")

    result[0] = driver.execute_script('return document.querySelectorAll("tr")[24].innerText')
    result[0] = result[0][14:]

    result[1] = driver.execute_script('return document.querySelectorAll("tr")[25].innerText')
    result[1] = result[1][65:76]

    # time.sleep(30)

    return result