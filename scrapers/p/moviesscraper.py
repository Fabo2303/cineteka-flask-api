import json
from playwright.sync_api import sync_playwright
from utils.formatter import convertir_a_slug
from dotenv import load_dotenv
import os


URL = os.getenv("P_URL")
NOMBRE = os.getenv("P")

def obtener_peliculas():
    """Scrapea la lista de películas con Playwright."""
    peliculas = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        # Aceptar cookies si el botón está presente
        try:
            boton_cookies = page.wait_for_selector("//button[span[span[text()='Aceptar Cookies']]]", timeout=5000)
            boton_cookies.click()
            print("Cookies aceptadas.")
        except:
            print("No se encontró el botón de cookies. Puede que ya estén aceptadas.")

        # Cargar todas las películas haciendo clic en "Ver más películas"
        while True:
            try:
                boton_ver_mas = page.wait_for_selector("//button[span[text()='Ver más películas']]", timeout=3000)
                boton_ver_mas.click()
                page.wait_for_timeout(1000)  # Pequeña espera para cargar más contenido
                print("Cargando más películas...")
            except:
                print("No hay más películas para cargar.")
                break

        # Esperar a que la lista de películas esté disponible
        page.wait_for_selector(".movies-list--large-item")

        # Obtener todas las películas
        peliculas_elements = page.query_selector_all(".movies-list--large-item")

        for pelicula in peliculas_elements:
            titulo_tag = pelicula.query_selector("h2.movies-list--large-movie-description-title")
            imagen_tag = pelicula.query_selector("img.image-loader--image")

            if titulo_tag and imagen_tag:
                titulo = titulo_tag.inner_text().strip()
                link = URL + "/" + convertir_a_slug(titulo)
                imagen = imagen_tag.get_attribute("src")

                peliculas.append({"titulo": titulo, "link": link, "imagen": imagen, "type": NOMBRE})

        browser.close()

    return peliculas

if __name__ == "__main__":
    obtener_peliculas()
