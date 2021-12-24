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
    
    import time
    import config as cfg
    import request as rq
    import methods as mt

    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # Constantes
    login = cfg.exUser
    passw = cfg.exPass

    uf = mt.toStateAcronym(rq.ufTo)
    city = mt.cleanStateName(rq.cityTo)

    result = []

    # Conectar com Rodonaves (Logar)
    driver.get("https://intranet2.expressosaomiguel.com.br/")

    # Logar
    driver.find_element_by_id('formLogin:username').send_keys(login)
    driver.find_element_by_id('formLogin:password').send_keys(passw)
    driver.find_element_by_id('formLogin:j_idt25').click()

    time.sleep(6)

    # Negar atualizar perfil
    driver.find_element_by_id('j_idt284').click()

    # Ir para as cotações
    driver.find_element_by_class_name('layout-menu-button').click()
    time.sleep(0.5)
    driver.find_element_by_id('menuform:menu-tudo_1_0').click()

    # Definir cidade
    driver.find_element_by_id('form_cotacao:cidadeDestino').click()
    time.sleep(1)
    # driver.find_element_by_xpath("//li[text()='{} / {}']".format(city, uf)).click()
    cmd = "//li[text()='{} / {}']".format(city, uf)
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
    driver.execute_script('PrimeFaces.ab({s:"form_cotacao:j_idt562",u:"growlMensagem form_cotacao:pnlCotacao corpo_pagina",onst:function(cfg){startProcessando();},onco:function(xhr,status,args){stopProcessando();}})')

    time.sleep(15)

    result.append(driver.execute_script('return document.querySelectorAll("tr")[24].innerText'))
    result[0] = result[0][14:]

    result.append(driver.execute_script('return document.querySelectorAll("tr")[25].innerText'))
    result[1] = result[1][65:]

    # time.sleep(30)

    return result