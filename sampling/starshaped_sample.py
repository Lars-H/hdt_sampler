from .sampling_algorithm import Sampling_Algorithm
import logging
logging.basicConfig(level=logging.INFO)
from rdflib import Graph
import json

class Starshaped_Sample(Sampling_Algorithm):

    def __init__(self, **kwargs):

        self.__weighted = kwargs.get("weighted", True)

        dict.__init__(self,
                      name="Starshaped Sampling",
                      weighted=self.__weighted
                      )
        self.__chunksize = kwargs.get("chunksize", 10)


    def __str__(self):
        return "Starshaped Sampling"

    def __repr__(self):
        return json.dumps(self.__dict__)


    def __chunk_list(self, l, n):
        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]


    def generate_sample_to_file(self, source, size, filename, **kwargs):
        with open(filename, "w+") as file:
            # Get Subjects
            try:
                subjects = source.random_subjects(size, weighted=self.__weighted)
            except Exception as e:
                logging.exception("Could not get {} subjects from {}".format(size, source))
                raise e

            # Get subjects edges
            total_cardinality = 0
            chunksize = self.__chunksize
            for index, subject in enumerate(self.__chunk_list(list(subjects), chunksize)):
                try:
                   added_edges = source.outgoing_edges(subject, file=file)
                   total_cardinality += added_edges
                except Exception as e:
                    logging.exception("Could not get outgoing edges for subject {}".format(subject))
                    logging.exception(e)

            return {
                "sampled_triples" : int(total_cardinality)
            }
