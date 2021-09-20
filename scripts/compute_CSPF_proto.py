import os
import time
from tqdm import tqdm
import sys
import csv
import logging

logging.basicConfig(level="INFO")

def shuffle_and_sort_file(fn: str) -> (str, int, float):

    # Get File Length
    cnt_cmd = "wc -l {} | grep -Eo '[0-9]{{1,7}}'".format(fn)
    cnt_cmd_res = os.popen(cnt_cmd).read()
    line_cnt = int(cnt_cmd_res.split("\n")[0])

    # Shuffle first
    logging.info("Shuffling")
    shuf_cmd = "shuf {} -o {}".format(fn, fn)
    os.system(shuf_cmd)

    # Sort
    logging.info("Sorting")
    sorted_fn = fn.replace(".nt", "_sorted.nt")
    sort_cmd = "sort {} -o {}".format(fn, sorted_fn)
    t1 = time.time()
    os.system(sort_cmd)
    delta = time.time() - t1

    return (sorted_fn, line_cnt, delta)

def create_cs(fn: str) -> (dict, float):

    logging.info("Compute CS")
    t1 = time.time()
    with open(fn, "a") as ntriples_file:
        ntriples_file.write("null null null")
    with open(fn) as ntriples_file:

        current_subject = None

        cs_props = {}
        cs = {}
        for line in tqdm(ntriples_file):
            # Init Current subject
            triple = line.split(" ")
            if current_subject is None:
                current_subject = triple[0]


            if triple[0] != current_subject:
                # Update CS if subject changes
                cs_key = frozenset(cs_props.keys())
                cs.setdefault(cs_key, {})['count'] = cs.get(cs_key, {"count": 0})['count'] + 1
                for p, count in cs_props.items():
                    cs[cs_key][p] = cs[cs_key].get(p, 0) + count
                current_subject = triple[0]
                cs_props = {}
            cs_props[triple[1]] = cs.get(triple[1], 0) + 1
    t_delta = time.time() - t1
    return (cs, t_delta)

def write_cs_to_tsv(fn: str, cs: dict) -> (bool, float):

    logging.info("Write to file.")
    t1 = time.time()
    with open(fn, 'w') as outfile:
        tsv_writer = csv.writer(outfile, delimiter='\t')
        for cs, cs_info in tqdm(cs.items()):
            trpls = sum(cs_info.values()) - cs_info['count']
            tsv_writer.writerow([';'.join(c for c in cs), cs_info['count'], cs_info, trpls])

    t_delta = time.time() - t1
    return (True, t_delta)


if __name__ == '__main__':

    ## Argument = filepath of an n-triples file
    assert len(sys.argv) == 2
    fn = sys.argv[1]
    out_fn = fn.replace(".nt", "_cs.tsv")

    sorted_fn,line_cnt, t_sort = shuffle_and_sort_file(fn)
    cs, t_compute = create_cs(sorted_fn)

    _ , t_write = write_cs_to_tsv(out_fn, cs)

    stats = {
        "t_sort": t_sort,
        "t_compute": t_compute,
        "t_write": t_write,
        "t_total": t_sort + t_compute + t_write,
        "file": fn,
        "line_cnt" : line_cnt,
        "CS_count": len(cs.keys())
    }
    print(stats)