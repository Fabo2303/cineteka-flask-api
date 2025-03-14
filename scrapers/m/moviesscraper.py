import json
from playwright.sync_api import sync_playwright
from utils.formatter import capitalizer
from dotenv import load_dotenv
import os


URL = os.getenv("M_URL")
NOMBRE = os.getenv("M")

def obtener_peliculas():
    """Scrapea la lista de películas con Playwright."""
    peliculas = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        try:
            boton_cookies = page.wait_for_selector("button[data-automation='Btn_acepto_cookies']", timeout=5000)
            boton_cookies.click()
            print("Cookies aceptadas.")
        except:
            print("No se encontró el botón de cookies. Puede que ya estén aceptadas.")

        page.wait_for_selector(".movie-box-container", timeout=10000)

        peliculas_elements = page.query_selector_all(".movie-box-container")

        for pelicula in peliculas_elements:
            titulo_tag = pelicula.query_selector(".movie-title")
            titulo = titulo_tag.inner_text().strip() if titulo_tag else "Sin título"

            link_tag = pelicula.query_selector("a.cta-buy")
            link = link_tag.get_attribute("href") if link_tag else "Sin enlace"

            bg_content = pelicula.query_selector(".movies-bg-content")
            imagen = "Sin imagen"
            if bg_content:
                style = bg_content.get_attribute("style")
                if "background-image" in style:
                    imagen = style.split('url("')[1].split('")')[0]
                    
            titulo = capitalizer(titulo)
            peliculas.append({"titulo": titulo, "link": link, "imagen": imagen, "type": NOMBRE})

        browser.close()

    return peliculas

if __name__ == "__main__":
    obtener_peliculas()
