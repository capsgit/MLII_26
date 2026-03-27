from argostranslate import package

# Descarga e instala el paquete alemán -> español
package.update_package_index()
available = package.get_available_packages()

pkg = next(
    p for p in available
    if p.from_code == "de" and p.to_code == "es"
)

download_path = pkg.download()
package.install_from_path(download_path)

print("OK: Modelo DE->ES instalado.")
