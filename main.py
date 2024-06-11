from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd


def extracao():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.get('http://enem.evolucional.com.br/microdados/ranking-enem-2020')
    sleep(1)
    caixa_principal = driver.find_element(By.ID, 'dataTable')
    caixa_info = caixa_principal.find_element(By.TAG_NAME, 'tbody')


    while True:
        if caixa_info.text == 'Aguarde, carregando...':
            sleep(1)
        else:
            caixa_info = caixa_principal.find_element(By.TAG_NAME, 'tbody')
            break

    sleep(1)
    lista_info_fato = []
    lista_estado_dim,lista_estado = [], []
    qtd_pag = driver.find_element(By.XPATH, '//*[@id="dataTable_paginate"]/span/a[6]').text
    cont_page = 0
    for pagina in range(int(qtd_pag)):
        elementos = caixa_info.find_elements(By.TAG_NAME, 'tr')
        cont = 0
        for elemento in elementos:
            cont += 1
            posicao = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[1]').text
            escola = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[2]/div').text
            inep = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[2]/small').text
            localizacao = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[3]').text
            cidade, estado = localizacao.split('\n')
            tipo_escola = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[4]').text
            dp_adm, tipo_dp = tipo_escola.split('\n')
            qtd_alunos = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[5]').text
            linguagens_codigos = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[6]').text
            ciencias_humanas = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[7]').text
            ciencias_natureza = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[8]').text
            matematica = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[9]').text
            redacao = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[10]').text
            media_sem_redacao = elemento.find_element(By.XPATH, f'//*[@id="dataTable"]/tbody/tr[{cont}]/td[11]').text
            lista_info_fato.append({'Posição':posicao,
                                'Escola':escola,
                                'Inep':inep,
                                'Cidade':cidade,
                                'Estado':estado,
                                'Dp_Adm':dp_adm,
                                'Tipo_dp':tipo_dp,
                                'Qtd_alunos': qtd_alunos,
                                'Linguagens_Codigos': linguagens_codigos,
                                'Ciencias_Humanas':ciencias_humanas,
                                'Ciencias_Natureza':ciencias_natureza,
                                'Matematica':matematica,
                                'Redacao':redacao,
                                'Media':media_sem_redacao
                               })
        if cont_page == 3:
            break
        cont_page += 1
        
        sleep(1)
        btn_proximo = driver.find_element(By.ID, "dataTable_next")
        ActionChains(driver).click(btn_proximo).perform()
        sleep(1)

    return lista_info_fato

informacoes = extracao()

fato_df = pd.DataFrame({
    'Posição':[posicao['Posição'] for posicao in informacoes],
    'Escola':[escola['Escola'] for escola in informacoes],
    'Inep':[inep['Inep'] for inep in informacoes],
    'Cidade':[cidade['Cidade'] for cidade in informacoes],
    'Estado':[estado["Estado"] for estado in informacoes],
    'Dp_Adm':[dp_adm['Dp_Adm'] for dp_adm in informacoes],
    'Tipo_dp':[tipo_dp['Tipo_dp'] for tipo_dp in informacoes],
    'Qtd_alunos': [qtd_alunos['Qtd_alunos'] for qtd_alunos in informacoes],
    'Linguagens_Codigos': [lc['Linguagens_Codigos'] for lc in informacoes],
    'Ciencias_Humanas':[ch['Ciencias_Humanas'] for ch in informacoes],
    'Ciencias_Natureza':[cn['Ciencias_Natureza'] for cn in informacoes],
    'Matematica':[mat['Matematica'] for mat in informacoes],
    'Redacao':[red['Redacao'] for red in informacoes],
    'Media':[media['Media'] for media in informacoes]

})
fato_df.to_csv('ranking.csv', sep=',')
