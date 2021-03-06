import argparse
import codecs
import csv
import sys
from typing import Dict, List

import yaml


def get_argparse() -> argparse.Namespace:
    """ Get argsparse.

    Returns:
        argparse.Namespace: Args data (configuration file)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Please set the path of the configuration file.")
    args = parser.parse_args()

    return args


def read_yaml(path: str) -> Dict:
    """ Read yaml and return the read data.

    Args:
        path (str): Yaml path

    Returns:
        Dict: Yaml data
    """
    try:
        with open(path) as file:
            cfg = yaml.safe_load(file)
    except Exception as e:
        print("Exception occurred while loading yaml...", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    return cfg


def write_yaml(path: str, cfg: Dict) -> None:
    """ Write yaml.

    Args:
        path (str): Yaml path
        Dict: Yaml data
    """
    with codecs.open(path, "w", "utf-8") as f:
        yaml.dump(cfg, f, encoding="utf-8", allow_unicode=True)


def tracking(tracker: List) -> None:
    """ Error tracking.

    Args:
        tracker (List): Tracking list
    """
    for idx, t in enumerate(tracker):
        print(f"===== Trace number: {idx + 1} =====")
        print(f"[Config parameters]\n{t[0]}\n")
        print(f"[Error message]\n{t[1]}\n")


def test_logger(data_obj, imgreco_obj, logger) -> None:
    """ Test logging.

    Args:
        data_obj (DataObject): DataObject
        imgreco_obj (ImgRecoObject): ImgRecoObject
        logger (Dict): Test result
    """
    with open(logger["LOG_FILE"], "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["labels", data_obj.classes])
        writer.writerow(["weight path", imgreco_obj.cfg["WEIGHT_PATH"]])
        writer.writerow(["Total", logger["COUNTER"], "Correct", logger["CORRECT"],
                         "Miss", logger["MISS"], "Acc", f"{logger['ACC']:.2f}%"])
        writer.writerow(["Confusion matrix"])

        for m in logger["MATRIX"]:
            writer.writerow(m)

        writer.writerow(["Details"])
        writer.writerow(["path", "label", "judge",
                         "pred", "Degree of reliability"])

        for sample, pred, dor in zip(data_obj.datasets.samples, logger["PREDS_LIST"], logger["DOR_LIST"]):
            if sample[1] == pred:
                judge = "correct"
            else:
                judge = "miss"

            writer.writerow([sample[0], sample[1], judge, pred, dor])
