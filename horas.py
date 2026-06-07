"""
Autor: Daniel Morera Torra
Descripción: Normalización de expresiones horarias en un fichero de texto.
"""

import re


def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero ficText, normaliza las expresiones horarias al formato
    HH:MM y escribe el resultado en ficNorm.
    """
    with open(ficText, encoding='utf-8') as f:
        texto = f.read()

    resultado = _procesaTexto(texto)

    with open(ficNorm, 'w', encoding='utf-8') as f:
        f.write(resultado)


def _procesaTexto(texto):

    def reemplazaDosPuntos(m):
        h, mi = int(m.group(1)), int(m.group(2))
        if 0 <= h <= 23 and 0 <= mi <= 59:
            return f'{h:02d}:{mi:02d}'
        return m.group(0)

    def reemplazaHm(m):
        h = int(m.group(1))
        mi = int(m.group(2)) if m.group(2) else 0
        if 0 <= h <= 23 and 0 <= mi <= 59:
            return f'{h:02d}:{mi:02d}'
        return m.group(0)

    def reemplazaColoquial(m):
        h = int(m.group(1))
        expr = m.group(2).strip()
        if h < 1 or h > 12:
            return m.group(0)
        if expr == 'en punto':
            mi = 0
        elif expr == 'y cuarto':
            mi = 15
        elif expr == 'y media':
            mi = 30
        elif expr == 'menos cuarto':
            h = h - 1 if h > 1 else 12
            mi = 45
        else:
            return m.group(0)
        return f'{h:02d}:{mi:02d}'

    def reemplazaParticula(m):
        h = int(m.group(1))
        mi = int(m.group(2)) if m.group(2) else 0
        particula = m.group(3).strip()

        if h < 1 or h > 12:
            return m.group(0)

        if particula == 'de la mañana' and not (4 <= h <= 12):
            return m.group(0)
        if particula == 'del mediodía' and not (h == 12 or 1 <= h <= 3):
            return m.group(0)
        if particula == 'de la tarde' and not (3 <= h <= 8):
            return m.group(0)
        if particula == 'de la noche' and not (8 <= h <= 12 or 1 <= h <= 4):
            return m.group(0)
        if particula == 'de la madrugada' and not (1 <= h <= 6):
            return m.group(0)

        if particula == 'de la mañana':
            h24 = h % 12
        elif particula == 'del mediodía':
            h24 = 12 if h == 12 else h + 12
        elif particula == 'de la tarde':
            h24 = h + 12
        elif particula == 'de la noche':
            h24 = (h + 12) % 24
        elif particula == 'de la madrugada':
            h24 = h % 12

        return f'{h24:02d}:{mi:02d}'

    texto = re.sub(
        r'\b(\d{1,2}):(\d{2})\b',
        reemplazaDosPuntos, texto
    )
    texto = re.sub(
        r'\b(\d{1,2})h(?:(\d{1,2})m)?(?=\s|$|[^a-zA-Z])',
        reemplazaHm, texto
    )
    texto = re.sub(
        r'\b(\d{1,2})\s+(en punto|y cuarto|y media|menos cuarto)\b',
        reemplazaColoquial, texto
    )
    texto = re.sub(
        r'\b(\d{1,2})(?::(\d{2}))?\s+(de la mañana|del mediodía|de la tarde|de la noche|de la madrugada)\b',
        reemplazaParticula, texto
    )

    return texto


if __name__ == '__main__':
    normalizaHoras('horas.txt', 'horas_norm.txt')
    with open('horas_norm.txt', encoding='utf-8') as f:
        print(f.read())