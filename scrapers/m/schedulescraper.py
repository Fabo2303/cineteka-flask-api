import json
import time
from playwright.sync_api import sync_playwright
from utils.formatter import capitalizer, limpiar_texto, convertir_hora


def obtener_horarios(url):
    """Scrapea los horarios de una película con Playwright."""
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        try:
            boton_cookies = page.wait_for_selector(
                "button[data-automation='Btn_acepto_cookies']", timeout=5000
            )
            boton_cookies.click()
            print("Cookies aceptadas.")
        except:
            print("No se encontró el botón de cookies. Puede que ya estén aceptadas.")

        while True:
            try:
                time.sleep(5)
                page.evaluate(
                    'document.getElementsByClassName("more-theatres")[0].click()'
                )
                time.sleep(5)
                print("Cargando más cines cercanos...")
            except:
                print("No hay más cines cercanos para cargar.")
                break

        page.wait_for_selector(".theatre-name h1", timeout=10000)

        sedes_principales = page.query_selector_all(".movie-schedule")
        for sede in sedes_principales:
            nombre_sede = capitalizer(
                limpiar_texto(sede.query_selector(".theatre-name h1").inner_text())
            )

            formatos = [
                limpiar_texto(tag.inner_text())
                for tag in sede.query_selector_all(".movie-version span")
            ]

            tipo_sala = list(
                set(
                    [
                        limpiar_texto(tag.inner_text())
                        for tag in sede.query_selector_all(".movie-seats span")
                    ]
                )
            )
            tipo_sala = [
                sala for sala in tipo_sala if sala not in ["ASIENTO:", "ASIENTOS:", ""]
            ]

            if not tipo_sala:
                tipo_sala = ["GENERAL"]

            idioma = [
                limpiar_texto(tag.inner_text())
                for tag in sede.query_selector_all(".movie-lenguaje span")
            ]
            if not idioma:
                idioma = ["DOBLADA"]

            horarios = [
                convertir_hora(limpiar_texto(btn.inner_text()))
                for btn in sede.query_selector_all(".btn-buy")
            ]

            data.append(
                {
                    "sede": nombre_sede,
                    "formato": formatos,
                    "tipo_sala": tipo_sala,
                    "idioma": idioma,
                    "horarios": horarios,
                }
            )

        sedes_cercanas = page.query_selector_all(".nearestWrap")
        nombre_sede_anterior = None 

        for sede in sedes_cercanas:
            nombre_sede_elem = sede.query_selector(".nearest-theatre-title h4")

            if nombre_sede_elem:
                nombre_sede = capitalizer(limpiar_texto(nombre_sede_elem.inner_text()))
                nombre_sede_anterior = nombre_sede
            else:
                nombre_sede = (
                    nombre_sede_anterior
                )

            formatos = [
                limpiar_texto(tag.inner_text())
                for tag in sede.query_selector_all(".movie-version span")
            ]

            tipo_sala = list(
                set(
                    [
                        limpiar_texto(tag.inner_text())
                        for tag in sede.query_selector_all(".movie-seats span")
                    ]
                )
            )
            tipo_sala = [
                sala for sala in tipo_sala if sala not in ["ASIENTO:", "ASIENTOS:", ""]
            ]

            if not tipo_sala:
                tipo_sala = ["GENERAL"]

            idioma = [
                limpiar_texto(tag.inner_text())
                for tag in sede.query_selector_all(".movie-lenguaje span")
            ]
            if not idioma:
                idioma = ["DOBLADA"]

            horarios = [
                convertir_hora(limpiar_texto(btn.inner_text()))
                for btn in sede.query_selector_all(".btn-buy")
            ]

            data.append(
                {
                    "sede": nombre_sede,
                    "formato": formatos,
                    "tipo_sala": tipo_sala,
                    "idioma": idioma,
                    "horarios": horarios,
                }
            )

        browser.close()

    return data


if __name__ == "__main__":
    obtener_horarios("busca tu url")
