import numpy as np
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)
    product_id = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    size = Column(String, nullable=False)
    price = Column(String, nullable=False)


def read_db(path):
    """
    Lee la base de datos SQL y devuelve arrays numpy limpios (sin datos vacíos).
    Retorna: country, gender, size, price
    """
    engine = create_engine(path)
    Session = sessionmaker(bind=engine)
    session = Session()

    countries, genders, sizes, prices = [], [], [], []
    
    
    for venta in session.query(Venta).all():
        # Verificar que no haya valores vacíos o nulos
        if any([
            venta.country is None or str(venta.country).strip() == "",
            venta.gender is None or str(venta.gender).strip() == "",
            venta.size is None or str(venta.size).strip() == "",
            venta.price is None or str(venta.price).strip() == ""
        ]):
            continue  # descartamos fila inválida



    # Limpieza del precio: quitar "$" y convertir a float
    precio_limpio = float(str(venta.price).replace("$", "").strip())

    # Guardar valores limpios
    countries.append(venta.country)
    genders.append(venta.gender)
    sizes.append(venta.size)
    prices.append(precio_limpio)

    session.close()
    
    # Convertir a arrays numpy
    country = np.array(countries)
    gender = np.array(genders)
    size = np.array(sizes)
    price = np.array(prices, dtype=float)

    return country, gender, size, price


# =============================
# 4️⃣ Función: países únicos
# =============================

def paises_unicos(country):
    """Devuelve un array con los países únicos."""
    return np.unique(country)

# =============================
# 5️⃣ Función: ventas totales por país
# =============================

def ventas_pais(countries, country, price):
    """Retorna un diccionario con el dinero total recaudado por cada país."""
    resultado = {}
    for c in countries:
        mask = country == c
        resultado[c] = np.sum(price[mask])
    return resultado

# =============================
# 6️⃣ Función: calzado más vendido por país
# =============================

def calzado_pais(countries, country, size):
    """Retorna un diccionario con el tamaño de calzado más vendido por país."""
    resultado = {}
    for c in countries:
        mask = country == c
        if np.sum(mask) == 0:
            resultado[c] = None
            continue
        sizes_country = size[mask]
        valores, conteos = np.unique(sizes_country, return_counts=True)
        resultado[c] = valores[np.argmax(conteos)]
    return resultado

# =============================
# 7️⃣ Función: cantidad de ventas por género y país
# =============================

def ventas_genero_pais(countries, gender_target, country, gender):
    """Retorna un diccionario con la cantidad de calzados vendidos del género solicitado por país."""
    resultado = {}
    for c in countries:
        mask_pais = country == c
        mask_genero = gender == gender_target
        total = np.sum(mask_pais & mask_genero)
        resultado[c] = int(total)
    return resultado

# =============================
# 8️⃣ Función: imprimir tabla formateada
# =============================

def print_table(title, data_dict, value_format="{:.2f}"):
    """Imprime un diccionario en formato de tabla."""
    print(f"\n{'=' * 60}")
    print(f"{title:^60}")
    print(f"{'=' * 60}")
    print(f"{'País':<25} | {'Valor':>20}")
    print(f"{'-' * 60}")

    for key, value in data_dict.items():
        # Si el valor es numérico, aplica formato
        if isinstance(value, (int, float)):
            print(f"{key:<25} | {value_format.format(value):>20}")
        else:
            print(f"{key:<25} | {str(value):>20}")

    print(f"{'-' * 60}\n")

# =============================
# 9️⃣ Bloque principal
# =============================

if __name__ == "__main__":
    print("\n¡Aquí utilizo mis funciones!\n")

    # Ruta de la base de datos
    path = "sqlite:///ventas_calzados.db"

    # Leer datos limpios
    country, gender, size, price = read_db(path)

    # Paises únicos
    countries_unique = paises_unicos(country)
    print_table("PAÍSES ÚNICOS", {i+1: p for i, p in enumerate(countries_unique)}, value_format="{}")

    # Ventas totales por país
    ventas = ventas_pais(countries_unique, country, price)
    print_table("VENTAS TOTALES POR PAÍS", ventas)

    # Calzado más vendido por país
    calzado = calzado_pais(countries_unique, country, size)
    print_table("CALZADO MÁS VENDIDO POR PAÍS", calzado, value_format="{}")

    # Ventas por género (ejemplo: 'Female')
    ventas_female = ventas_genero_pais(countries_unique, "Female", country, gender)
    print_table("VENTAS DE GÉNERO 'FEMALE' POR PAÍS", ventas_female, value_format="{}")
