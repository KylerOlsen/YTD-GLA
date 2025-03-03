# Kyler Olsen
# Mar 2024

from json import load


class ResourceNotFound(Exception): pass


def load_uri(uri: str):

    parts = uri.lower().strip('/').split('/')
    if len(parts) == 3:
        vol, book, cv = parts
        chap = int(cv.split('-')[0].split('.')[0])

        if vol == 'ot': filename = "data/old-testament.json"
        elif vol == 'nt': filename = "data/new-testament.json"
        elif vol == 'bofm': filename = "data/book-of-mormon.json"
        elif vol == 'dc-testament': filename = "data/doctrine-and-covenants.json"
        elif vol == 'pgp': filename = "data/pearl-of-great-price.json"
        else: raise ResourceNotFound(f"{vol} ({uri})")

        with open(filename, 'r', encoding='utf-8') as file:
            data = load(file)

        if vol == 'dc-testament':
            if book == 'dc': pass
            elif book == 'od': pass
            else: raise ResourceNotFound(f"{vol}/{book} ({uri})")
        else:
            for book_data in data['books']:
                if book_data['lds_slug'] == book:
                    for chap_data in book_data['chapters']:
                        if chap_data['chapter'] == chap:
                            return chap_data
                    else: raise ResourceNotFound(f"{vol}/{book}/{chap} ({uri})")
            else: raise ResourceNotFound(f"{vol}/{book} ({uri})")

    raise ResourceNotFound(uri)
