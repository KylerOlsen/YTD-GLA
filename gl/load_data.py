# Kyler Olsen
# Mar 2024

from json import load
from yaml import safe_load


class ResourceNotFound(Exception): pass


COLLECTION_RESOURCES = [
    'collection','scripture.volume','scripture.book','scripture.division']

def get_uri_data(uri: str, current):
    for i in uri.split('/'):
        if 'units' not in current:
            raise ResourceNotFound(f"Unknown URI: {uri}")
        for unit in current['units']:
            if (
                'url' in unit and unit['url'] == i) or (
                'range' in unit and i.isdigit() and int(i) <= unit['range']
            ):
                current = unit
                break
        else:
            raise ResourceNotFound(f"Unknown URI: {uri}")
    return current

def load_uri(uri: str):
    uri = uri.lower().strip('/')

    with open("data/page-urls.yaml", 'r', encoding='utf-8') as file:
        uri_data = {'units': safe_load(file), 'resource': 'collection'}
        if uri: uri_data = get_uri_data(uri, uri_data)

    if uri_data['resource'] == 'scripture.chapter' and uri.count('/') == 3:
        return load_chapter(uri, uri_data['resource'])
    elif uri_data['resource'] in COLLECTION_RESOURCES:
        return load_collection(uri, uri_data)

    raise ResourceNotFound(
        f"Unknown Resource Type: {uri_data['resource']} ({uri})")

def load_chapter(uri, resource_type):
    parts = uri.lower().strip('/').split('/')
    _, vol, book, cv = parts
    chap = int(cv.split('-')[0].split('.')[0])

    if vol == 'ot': filename = "data/old-testament.json"
    elif vol == 'nt': filename = "data/new-testament.json"
    elif vol == 'bofm': filename = "data/book-of-mormon.json"
    elif vol == 'pgp': filename = "data/pearl-of-great-price.json"
    else: raise ResourceNotFound(f"Unknown Volume: {vol} ({uri})")

    with open(filename, 'r', encoding='utf-8') as file:
        data = load(file)

    for book_data in data['books']:
        if book_data['lds_slug'] == book:
            for chap_data in book_data['chapters']:
                if chap_data['chapter'] == chap:
                    return chap_data, resource_type
            else: raise ResourceNotFound(
                f"Unknown Chapter: {vol}/{book}/{chap} ({uri})")
    else: raise ResourceNotFound(f"Unknown Book: {vol}/{book} ({uri})")

def load_collection(uri, uri_data):
    uri = (f"/{uri}/" if uri else "/")
    collection = []
    if 'units' in uri_data:
        for unit in uri_data['units']:
            if 'url' in unit:
                if 'name' in unit: name = unit['name']
                else: name = unit['url']
                collection.append((name, uri + unit['url'],))
            elif 'range' in unit:
                for i in range(unit['range']):
                    collection.append((str(i+1), uri + str(i+1),))
    return collection, uri_data['resource']

if __name__ == '__main__':
    load_uri("/scriptures/ot/gen/1")
