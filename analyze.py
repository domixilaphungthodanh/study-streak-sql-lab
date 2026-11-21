from run_streak import prepare_environment, run

if __name__ == "__main__":
    run([prepare_environment(), "-c", "from streak_lab.analysis import export; export()"])
