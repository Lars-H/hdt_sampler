from rdflib import URIRef, Graph
from utils import tuple_to_triple, tuple_to_ntriple
from hdt import HDTDocument
import random
import logging

logger = logging.getLogger("hdt_sampler")


class HDT_Dataset():

    def __init__(self, **kwargs):

        self.__source = kwargs.get("file", None)
        if self.__source is None:
            raise TypeError()
        try:
            self.document = HDTDocument(self.__source)
        except Exception as e:
            logger.exception("Could not load HDT File from {}.".format(self.__source))
            raise e
        self.card = None


    def __str__(self):
        return str(self.__source)

    def __len__(self):
        if self.card:
            return self.card
        else:
            (_, self.card) = self.document.search_triples("", "", "")
            return len(self)

    @property
    def distinct_subjects(self):
        return self.document.nb_subjects

    def random_subjects(self, size=100, weighted=True):

        logger.info(f"Generating a random sample, weighted = {weighted}")
        cardinality = len(self)
        sample = set()
        if size > len(self):
            raise Exception("Sample size exceeds dataset size")
        while (len(sample) < size):
            offset = random.randint(0, cardinality - 1)
            (triples, res_card) = self.document.search_triples("", "", "", limit=1, offset=offset)
            subject = tuple_to_triple(next(triples))[0]
            if weighted:
                if type(subject) == URIRef:
                    sample.add(subject)
            else:
                # Get the degree of the subject
                (ts, subject_degree) = self.document.search_triples(subject, "", "")
                # Assume the minimum degree of all subjects = 1
                min_degree = 1
                min_probability = min_degree / self.document.nb_subjects  # Minimum probaility of a subject to be chosen

                # Probability of the current subject to be chosen
                p = min_probability / (subject_degree / self.document.nb_subjects)

                # Draw random number
                r = random.random()

                if r < p:
                    if type(subject) == URIRef:
                        sample.add(subject)
        return sample

    def random_sample(self, size=100):

        cardinality = len(self)
        sample = set()
        if size > len(self):
            raise Exception("Sample size exceeds dataset size")
        while len(sample) < size:
            offset = random.randint(0, cardinality - 1)
            (triples, res_card) = self.document.search_triples("", "", "", limit=1, offset=offset)
            sample.add(tuple_to_triple(next(triples)))

        return list(sample)

    def outgoing_edges(self, terms, **kwargs):
        file = kwargs.get("file", None)
        total_cardinality = 0
        for term in terms:
            (triples, cardinality) = self.document.search_triples(str(term), "", "")
            for triple in triples:
                file.write(tuple_to_ntriple(triple))
            total_cardinality += cardinality
        return total_cardinality

    def random_edge(self, subject):

        (triples, cardinality) = self.document.search_triples(str(subject), "", "")
        if cardinality == 0:
            return None
        random_offset = random.randint(0, cardinality)
        (triples, cardinality) = self.document.search_triples(str(subject), "", "", limit=1, offset=random_offset)
        for triple in triples:
            object = tuple_to_triple(triple)[2]
            if type(object) is URIRef:
                return object
        return None
