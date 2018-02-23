from hdt import HDTDocument

DBPEDIA_RESOURCE_URI = "http://dbpedia.org/resource/{resource_name}"
DBPEDIA_ONTOLOGY_URI = "http://dbpedia.org/ontology/"

try:
    eng_dbpedia = HDTDocument("dbpedia_dump/en/instance_type.hdt")
except RuntimeError:
    raise RuntimeError("DBpedia english dump not found: Put dbpedia dump into dbpedia_dump folder")
try:
    fr_dbpedia = HDTDocument("dbpedia_dump/fr/instance_type.hdt")
except RuntimeError:
    raise RuntimeError("DBpedia french dump not found: Put dbpedia dump into dbpedia_dump folder")


def entity_types_request(query, lang='en'):
    if query:
        query = query.encode("utf-8")
        query = to_dbpedia_format(query)
        subject_query = DBPEDIA_RESOURCE_URI.format(resource_name=query)
        (triples, cardinality) = eng_dbpedia.search_triples(subject_query, "", "")
        if cardinality < 0:
            (triples, cardinality) = fr_dbpedia.search_triples(subject_query, "", "")
            print "FR"
        classes = []
        for triple in triples:
            cl = triple[2]
            if "owl#Thing" not in cl:
                cl = cl.replace(DBPEDIA_ONTOLOGY_URI, '')
                classes.append(cl)
        if classes:
            return classes
    return None


def to_dbpedia_format(query):
    query = query.title()
    query = query.replace(' ', '_')
    return query
