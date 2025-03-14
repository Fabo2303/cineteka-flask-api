import json
from playwright.sync_api import sync_playwright
from utils.formatter import limpiar_texto

def obtener_horarios(url):
    """Scrapea los horarios de una película con Playwright."""
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        
        page.wait_for_selector(".cinema-showcases--summary-name")

        sedes = page.query_selector_all(".Collapsible.accordion.cinema-showcases")

        for sede in sedes:
            nombre_sede = limpiar_texto(sede.query_selector(".cinema-showcases--summary-name").inner_text())
            formato = limpiar_texto(sede.query_selector(".sessions-details--formats-dimension").inner_text())
            tipo_sala = limpiar_texto(sede.query_selector(".sessions-details--formats-theather").inner_text())
            idioma = limpiar_texto(sede.query_selector(".sessions-details--formats-language").inner_text())

            horarios = [
                limpiar_texto(btn.inner_text()) 
                for btn in sede.query_selector_all(".showtime-selector--link")
            ]

            data.append({
                "sede": nombre_sede,
                "formato": formato,
                "tipo_sala": tipo_sala,
                "idioma": idioma,
                "horarios": horarios
            })

        browser.close()

    return data

if __name__ == "__main__":
    obtener_horarios("busca tu url")
