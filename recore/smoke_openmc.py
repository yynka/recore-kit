from recore.openmc_run import build_pincell
 
if __name__ == "__main__":
    sp = build_pincell(particles=1000, batches=20)
    print(f"Smoke test complete. Statepoint: {sp}") 