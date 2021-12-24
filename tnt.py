def tnt():
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
    login = cfg.tntUser
    passw = cfg.tntPass

    result = ["Erro", "Erro"]

    # Conectar com Rodonaves (Logar)
    driver.get("https://radar.tntbrasil.com.br/radar/public/login.do")

    # Campos de Login
    loginInput = driver.find_element_by_id('login')
    passwInput = driver.find_element_by_id('senha')

    loginInput.send_keys(login)
    passwInput.send_keys(passw)
    driver.execute_script('document.querySelector("a#login").click()')

    # Check 404
    # if (driver.find_element_by_xpath("//title[text()='Error 404--Not Found']")):
    #     return "TNT: Erro 404 - Página fora do ar."

    time.sleep(2)

    # Entrar nas cotações
    # driver.execute_script("document.querySelectorAll('.img-circle')[0].click()")
    driver.get("https://radar.tntbrasil.com.br/radar/private/cotacaoOnline.do")

    time.sleep(2)

    # CNPJ
    Select(driver.find_element_by_id('cnpjsSelect')).select_by_value('40887025000173')
    # driver.find_element_by_xpath("//option[@value='40887025000173']").click()

    time.sleep(2)

    # Dados do Destinatário
    tipoPessoaDestinatario = Select(driver.find_element_by_id('tipoPessoaDestinatario'))
    tipoPessoaDestinatario.select_by_value('F')

    time.sleep(1)

    driver.find_element_by_id('nomeDestinatario').send_keys(rq.name)

    Select(driver.find_element_by_id('sitTributariaDestinatario')).select_by_value('ME')

    time.sleep(2)

    # Dados do Responsável
    driver.find_element_by_id('manterDadosClientes').click()

    time.sleep(2)

    # Dados do Frete
    Select(driver.find_element_by_id('naturezaProduto')).select_by_value('10')
    time.sleep(1)
    driver.find_element_by_id('manterDadosFrete').click()

    time.sleep(5)

    # Itens
    driver.find_element_by_id('cepDestinatario').send_keys(rq.cepTo)

    time.sleep(5)

    driver.find_element_by_id('vlrMercadoria').send_keys(rq.total)
    if (rq.total >= 100): # Casas decimais
        driver.find_element_by_id('vlrMercadoria').send_keys("00")

    driver.find_element_by_id('pesoKg').send_keys(mt.getTotalWeight())

    driver.find_element_by_id('qtd').send_keys(mt.getTotalQty(mt.getPackages()))

    time.sleep(2)

    # Iteração de produtos
    driver.execute_script('document.querySelector("a#btnDimensoes").click()')

    for i in mt.getPackages():
        print(i)
        # driver.find_element_by_id('altura').send_keys(cfg.height[i[0]] * i[2]) # Altura
        # driver.find_element_by_id('largura').send_keys(cfg.width[i[0]]) # Largura
        # driver.find_element_by_id('comprimento').send_keys(cfg.length[i[0]]) # Comprimento
        # driver.find_element_by_id('quantidade').send_keys(i[1]) # Quantidade

        driver.execute_script('document.querySelector("#altura").value = {}'.format(cfg.height[i[0]] * i[2]))
        driver.execute_script('document.querySelector("#largura").value = {}'.format(cfg.width[i[0]]))
        driver.execute_script('document.querySelector("#comprimento").value = {}'.format(cfg.length[i[0]]))
        driver.execute_script('document.querySelector("#quantidade").value = {}'.format(i[1]))

        driver.execute_script('document.querySelector("#salvarDimensoes").click()') # Salvar

    time.sleep(2)

    driver.execute_script('document.querySelector("#fecharDimensoes").click()') # Fechar
    driver.execute_script('document.querySelector("#gravar").click()') # Gravar
    driver.execute_script('document.querySelector("#telefone").value = {}'.format(rq.phone)) # Telefone

    prazo = driver.find_element_by_id('prazoDias').get_attribute('value')
    print("O prazo é {} dias".format(prazo))

    driver.execute_script('document.querySelector("#confirmar").click()') # Confirmar

    time.sleep(1)

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")

    # Resultado: prazo
    result[1] = prazo

    time.sleep(7)

    driver.execute_script('document.querySelectorAll("a")[47].click()') # Calc

    return result
    time.sleep(130)
    driver.quit()