
import cProfile
import maude
import os
from pathlib import Path
import pstats
from pstats import SortKey
from datetime import date, datetime, timedelta
from timeit import default_timer as timer



def smt_overhead(profile):
    d = profile.func_profiles

    z3_time = 0
    smtlib_time = 0
    check_count = -1

    for key, val in d.items():
        if "z3" in val.file_name:
            z3_time += val.tottime

            if str(key) == "Z3_solver_check_assumptions":
                check_count = int(val.ncalls)

        elif "smtlib" in val.file_name:
            smtlib_time += val.tottime

    return (z3_time, smtlib_time, check_count)

def run_experiment(module, search_obj, start_terms, prefix_file, 
                   system_pattern, goal_pattern, system_name,
                    num_solvers=None, cycles=False, depth=None):

    today = date.today().strftime("%Y-%m-%d")
    name = search_obj.__name__

    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))

    Path(results_dir).mkdir(exist_ok=True)

    if depth is None:
        output_file = f"{results_dir}/{prefix_file}-{name}-{today}.txt"

    else:
        output_file = f"{results_dir}/{prefix_file}-{name}-depth={depth}-{today}.txt"


    with open(output_file, "w") as fo:
        for start_term in start_terms:
            now = datetime.now().time()

            print(f"Started at {now}", file=fo)
            print(f"Start term: {start_term}", file=fo)
            print(f"{name}", file=fo)

            term = module.parseTerm(start_term)
            depth_t = None

            if depth:

                if system_name == "ASystem":
                    print(f"Depth Mult: {depth}", file=fo)

                    # If CPS we take depth to either be 1/3, 2/3 or 3/3 of
                    # the search tree since it is bounded by stop time
                    stop_time = module.parseTerm(f"getStopTime({term})")
                    stop_time.reduce()
                    stop_time_int = stop_time.toInt()

                    depth_t = depth * stop_time_int

                if depth_t is None:
                    depth_t = depth

                print(f"Depth: {depth_t}", file=fo)

            fo.flush()
            

            if num_solvers:
                search = search_obj(num_solvers, system_name, cycles=cycles)
            else:
                search = search_obj(system_name)
            

            pr = cProfile.Profile()
            pr.enable()

            search.register_hooks()

            start = timer()
            if depth is None:
                search.search(term, system_pattern, goal_pattern)

            else:
                search.search(term, system_pattern, goal_pattern, depth_t)

            end = timer()


            pr.disable()

            p = pstats.Stats(pr)
            p = p.strip_dirs().sort_stats(SortKey.TIME)

            z3_time, smt_time, check_count = smt_overhead(
                p.get_stats_profile())
            

            print(search.found, file=fo)
            print(f"time {end - start}", file=fo)
            print(
                f"result {round(end - start, 5)} / {search.count} / {(z3_time / (end-start)) * 100}%", file=fo)
            print(
                f"z3 overhead: {z3_time} {(z3_time / (end-start)) * 100}%", file=fo)
            print(
                f"smtlib overhead: {smt_time} {(smt_time / (end-start)) * 100}%", file=fo)
            print(f"solver.check() calls: {check_count}", file=fo)
            print("="*80, file=fo)
            print("\n\n", file=fo)
            fo.flush()

            


