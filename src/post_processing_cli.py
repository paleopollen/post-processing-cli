import argparse
import logging

from datetime import datetime

from post_processor import PostProcessor


class PostProcessingCli:
    def __init__(self,):
        self.parser = argparse.ArgumentParser(description="Post process the pollen detection results.")
        self.args = None

        # Add arguments

        # Detections directory path
        self.parser.add_argument("--detections-dir", "-d", type=str, dest="detections_dir_path", nargs='?', default=None,
                                 required=True, help="Full path of the directory containing the detection results.")
        # SAM-2 model path
        self.parser.add_argument("--sam2-model-path", "-m", type=str, dest="sam2_model_path", nargs='?', default=None,
                                 required=True, help="Full path of the SAM-2 model.")
        # SAM-2 config path
        self.parser.add_argument("--sam2-config-path", "-c", type=str, dest="sam2_config_path", nargs='?', default=None,
                                 required=True, help="Full path of the SAM-2 config file.")

    def parse_args(self):
        self.args = self.parser.parse_args()

    def print_args(self):
        print("\nArguments\tValues")
        print("======================")
        print(f"Detections directory path\t{self.args.detections_dir_path}")


if __name__ == '__main__':
    start_time = datetime.now()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s : %(name)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger("post_processing_cli.py")
    logger.info("Starting Post Processing CLI")

    cli = PostProcessingCli()
    cli.parse_args()
    cli.print_args()

    post_processor = PostProcessor(cli.args.detections_dir_path, cli.args.sam2_model_path, cli.args.sam2_config_path)
    post_processor.run()

    logger.info("Post Processing CLI completed")
    logger.info(f"Time taken: {datetime.now() - start_time}")
