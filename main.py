from tqdm import tqdm

import libraries.dataloader as dataloader
from libraries.optimizers import (
    SimulatedAnnealing,
    GeneticAlgorithm,
)
from libraries.algorithms import EDF
from libraries.graphplot import getTimetablePlot
import config


def experiment(data_path, profiling=False):

    # load tasks
    dl = dataloader.DataLoader(data_path)
    TT, ET = dl.loadFile()

    if config.algorithm == "SA":
        optim = SimulatedAnnealing(
            TT,
            ET,
            numinstances=config.SA["numinstances"],
            numworkers=config.SA["numworkers"],
            maxiter=config.SA["maxiter"],
            toll=config.SA["toll"],
            wandblogging=config.SA["wandblogging"],
            iterationPerTemp=config.SA["iterationPerTemp"],
            initialTemp=config.SA["initialTemp"],
            finalTemp=config.SA["finalTemp"],
            tempReduction=config.SA["tempReduction"],
            alpha=config.SA["alpha"],
            beta=config.SA["beta"],
        )

    elif config.algorithm == "GA":
        optim = GeneticAlgorithm(
            TT,
            ET,
            numinstances=config.GA["numinstances"],
            numworkers=config.GA["numworkers"],
            maxiter=config.GA["maxiter"],
            toll=config.GA["toll"],
            wandblogging=config.GA["wandblogging"],
            pop_size=config.GA["pop_size"],
            num_parents=config.GA["num_parents"],
            p_cross=config.GA["p_cross"],
            p_mut=config.GA["p_mut"],
        )
    else:
        print(f"{config.algorithm} not recognized")
        quit()

    if config.SA["temptune"]:
        optim.plotTemperature()
        quit()

    bar_iter = optim.maxIter * optim.numInstances if optim.numWorkers == 1 else optim.numInstances

    if profiling:
        import cProfile, pstats

        with cProfile.Profile() as pr:
            with tqdm(
                total=bar_iter, desc="Progress", bar_format="{desc}{percentage:3.0f}%|{bar:10}{r_bar}"
            ) as bar:  # progress bar
                optim.run(bar.update)
        pr = pstats.Stats(pr)
        pr.sort_stats("cumulative").print_stats(10)
    else:
        with tqdm(total=bar_iter, desc="Progress", bar_format="{desc}{percentage:3.0f}%|{bar:10}{r_bar}") as bar:
            optim.run(bar.update)

    optim.printSolution()
    optim.plotBars()
    optim.plotCost(instance_idx="all")

    __, timetable, __, __ = EDF(TT + optim.bestSolution)
    getTimetablePlot(TT + optim.bestSolution, timetable, group_tt=True).show()


if __name__ == "__main__":
    import cpuinfo

    cpu = cpuinfo.get_cpu_info()
    print("{}, {} cores".format(cpu["brand_raw"], cpu["count"]))

    experiment(config.test_case_path, config.profiling)
