from recore.openmc_run import build_pincell

def main():
    """Run the smoke test and return True if successful."""
    try:
        sp = build_pincell(particles=1000, batches=20)
        print(f"Smoke test complete. Statepoint: {sp}")
        return True
    except Exception as e:
        print(f"Smoke test failed: {e}")
        return False

if __name__ == "__main__":
    main()
