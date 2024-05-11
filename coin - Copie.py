from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
driver.get("https://coinmarketcap.com/fr/all/views/all/")

# Attendre que la page soit initialement chargée
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cmc-table-row")))

# Fonction pour défiler progressivement jusqu'en bas de la page
def slow_scroll(driver):
    scroll_pause_time = 0.5  # Vous pouvez ajuster le temps de pause
    screen_height = driver.execute_script("return window.innerHeight")  # obtenir la hauteur de la fenêtre
    i = 1

    while True:
        # scroll par la hauteur de la fenêtre
        driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
        i += 1
        time.sleep(scroll_pause_time)  # attendre le chargement de la page
        # Vérifier si le bas de la page est atteint
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        if (screen_height * i) > scroll_height:
            break

# Exécuter le scroll lent
slow_scroll(driver)

# Récupérer tous les éléments avec la classe 'cmc-table-row'
rows = driver.find_elements(By.CLASS_NAME, "cmc-table-row")
print(f"Nombre total de lignes récupérées: {len(rows)}")  # Imprimer le nombre de lignes

# Boucle sur chaque 'row' pour extraire les informations requises
for index, row in enumerate(rows):
    print(f"Traitement de la ligne {index + 1}:")  # Affiche le numéro de la ligne en cours de traitement
    
    # Extraire tous les 'cells' dans chaque 'row'
    cells = row.find_elements(By.CLASS_NAME, "cmc-table__cell")
    
    # Extraire le nom de la colonne, s'il existe dans cette 'row'
    column_name = row.find_elements(By.CLASS_NAME, "cmc-table__column-name")
    
    if column_name:
        print(f"Nom de la colonne récupéré : {column_name[0].text}")  # Affiche le nom de la colonne

    # Afficher le texte de chaque cellule récupérée
    for cell in cells:
        print(f"Texte de la cellule : {cell.text}")

# Fermer le navigateur une fois terminé
driver.quit()

