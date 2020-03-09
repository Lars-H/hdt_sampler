from .sampling_algorithm import Sampling_Algorithm
import logging
logging.basicConfig(level=logging.INFO)
from rdflib import Graph
import json

class Hybrid_Sampling(Sampling_Algorithm):

    def __init__(self, **kwargs):


        self.__ratio = kwargs.get("ratio", 0.5)

        if self.__ratio > 1.0 or self.__ratio < 0.0:
            raise ValueError("Ratio must be in [0,1]")

        dict.__init__(self,
                      name="Hybrid Sampling",
                      ratio=self.__ratio
                      )
        self.__chunksize = kwargs.get("chunksize", 10)


    def __str__(self):
        return "Hybrid Sampling"

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
                popular_sbj_cnt = int(self.__ratio * size)
                longtail_sbj_cnt = int(size-popular_sbj_cnt)

                popular_subjects = source.random_subjects(popular_sbj_cnt, weighted=True)
                longtail_subjects = source.random_subjects(longtail_sbj_cnt, weighted=False)
                subjects = popular_subjects.union(longtail_subjects)
                logging.info(f"Size: {size}; Popular: {len(popular_subjects)}; Longtail: {len(longtail_subjects)}; Ratio {self.__ratio}")
            except Exception as e:
                logging.exception("Could not get {} subjects from {}".format(size, source))
                raise e

            # Produce edges for all subjects
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