from pathlib import Path

ROOT_PATH = Path(__file__)
PROJECT_PATH = ROOT_PATH.parent.parent

CAM02_UCS_LUT_PATH = PROJECT_PATH / "rgb_cam02ucs_lut.npz"


def main():
    paths = [ROOT_PATH, PROJECT_PATH, CAM02_UCS_LUT_PATH]

    for path in paths:
        print(path, "exists:", path.exists())


if __name__ == "__main__":
    main()
