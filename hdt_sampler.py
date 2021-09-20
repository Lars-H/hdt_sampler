import argparse
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import sys
import datetime as dt
from datasets import HDT_Dataset
from sampling import Starshaped_Sample, Hybrid_Sampling
import math


def get_options():
    parser = argparse.ArgumentParser(description="hdt_sampler: Sampling subgraphs from HDT Files")

    parser.add_argument("-f", "--file",
                        help="HDT File to be sampled from (required)", required=True)
    parser.add_argument("-s", "--size",
                        help="Percentage of subjects to be sampled, range: [0,1] (required)",
                        type=float, required=True)
    parser.add_argument("-n", "--number",
                        help="Number of samples to be created (default=1)",
                        default=1, type=int)
    parser.add_argument("-m", "--method",
                        help="Sampling method to be used (required: unweighted, weigthed, hybrid)",
                        choices=["unweighted", "weighted", "hybrid"],
                        required=True
                        )
    parser.add_argument("-r", "--ratio",
                        help="Ratio for hybrid sampling, range: [0,1] (default=0.5)",
                        default=0.5, type=float)
    parser.add_argument("-l", "--logging",
                        help="Set logging level (optional)",
                        choices=["INFO", "DEBUG", "ERROR"],
                        default="ERROR")
    args = parser.parse_args()
    return args


class Sampler(object):

    def __init__(self, **kwargs):

        self.logger = logging.getLogger("hdt_sampler")
        if kwargs.get("logging", None):
            self.logger.setLevel(kwargs.get("logging"))

        # Init Sample ID
        self.__sample_id = "{}_{}".format(dt.datetime.now().strftime("%Y%m%d-%H%M%S"), "study")

        # Init Sampling Method
        self.Sampling_Method = None
        method_name = kwargs.get("method")
        if method_name == "unweighted":
            self.Sampling_Method = Starshaped_Sample(weighted=False)
        elif method_name == "weighted":
            self.Sampling_Method = Starshaped_Sample(weighted=True)
        elif method_name == "hybrid":
            self.Sampling_Method = Hybrid_Sampling(ratio=kwargs.get("ratio"))
        else:
            raise Exception("Sampling method not instatiated.")

        # Sampling Params
        rel_sample = kwargs.get("size", 0)
        self.n = kwargs.get("number", 1)

        # Init HDT Dataset
        self.sampling_dataset = HDT_Dataset(**kwargs)

        # Compute abs. number of subjects to be sampled
        self.sample_size = max(int(math.floor(int(self.sampling_dataset.distinct_subjects) * float(rel_sample))), 1)
        self.logger.info(f"Sample size: {rel_sample * 100} % of all subject = {self.sample_size} subjects.")

    def execute(self):
        for i in range(self.n):
            start = dt.datetime.now()
            self.logger.info("{} : Generating Sample {}/{}".format(start, i + 1, self.n))
            sample_id = str(start.timestamp()).replace(".", "")

            # Set Sample File Name
            sample_fn = "{}".format("sample_{}.nt".format(sample_id))

            # Create Sample
            sampling_metadata = self.Sampling_Method.generate_sample_to_file(self.sampling_dataset, self.sample_size,
                                                                             sample_fn)
            self.logger.debug(sampling_metadata)

            end = dt.datetime.now()
            self.logger.info(
                f"Sample '{sample_fn}' with {sampling_metadata['sampled_triples']} triples created in {end - start}.")



if __name__ == '__main__':
    options = get_options()
    sampler = Sampler(**vars(options))
    sampler.execute()

    sys.exit(0)
