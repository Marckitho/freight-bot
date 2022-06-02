# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

import config as cfg
import methods as mt
import rodonaves as rd
import expresso as ex
import tnt

rdResult = ["Erro", "Erro"]
tntResult = ["Erro", "Erro"]
exResult = ["Erro", "Erro", ""]

# driver = webdriver.Chrome(ChromeDriverManager().install())

# Rodar
if (cfg.useRodonaves): rdResult = rd.rodonaves()
if (cfg.useExpresso): exResult = ex.expresso()
if (cfg.useTnt): tntResult = tnt.tnt()

print("- Rodonaves -\nPreço: {}\nPrazo: {}\n".format(rdResult[0], rdResult[1]))
print("- TNT -\nPreço: {}\nPrazo: Até {} dias úteis\n".format(tntResult[0], tntResult[1]))
print("- Expresso -\nPreço:{}\nPrazo:{}\n{}".format(exResult[0], exResult[1], exResult[2]))