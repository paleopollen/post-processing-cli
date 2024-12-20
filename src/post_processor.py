import os
import json
import cv2 as cv
import numpy as np
import logging
import matplotlib

# Set matplotlib backend to Agg to avoid GUI
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import hydra
import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from PIL import Image
from utils import segmentation_utils


class PostProcessor:
    def __init__(self, detections_dir_root_path: str, sam2_model_path: str, sam2_config_path: str):
        self.detections_dir_root_path = detections_dir_root_path
        self.sam2_model_path = sam2_model_path
        self.sam2_config_path = sam2_config_path

        self.detections_dirs_path_list = []
        self.in_focus_images_list = []
        self.max_pollen_detection_image_dimension = (0, 0)

        logging.basicConfig(format='%(asctime)s %(levelname)-7s : %(name)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger("post_processor.py")

    def populate_detections_dit_list(self):
        pass

    @staticmethod
    def read_images_in_folder(images_dir_path):
        image_paths = []
        for filename in os.listdir(images_dir_path):
            if filename.endswith("z.png"):
                image_paths.append(os.path.join(images_dir_path, filename))
        return image_paths

    @staticmethod
    def find_in_focus_image(images_paths):
        max_count_edge_pixels = 0
        max_count_edge_pixels_img = None
        in_focus_image_path = None

        for image_path in images_paths:
            img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
            if img is not None:
                # Noise removal
                cv.GaussianBlur(img, (5, 5), 0, img)
                # Edge detection
                edges = cv.Canny(img, 100, 200, L2gradient=True)
                count_edge_pixels = np.count_nonzero(edges == 255)
                if count_edge_pixels > max_count_edge_pixels:
                    max_count_edge_pixels = count_edge_pixels
                    max_count_edge_pixels_img = img
                    in_focus_image_path = image_path

        return max_count_edge_pixels, max_count_edge_pixels_img, in_focus_image_path

    def find_in_focus_images_and_update_metadata(self):
        image_dir_names = []

        for directory in self.detections_dirs_path_list:
            image_dir_names.append(directory)
            images_paths = self.read_images_in_folder(os.path.join(self.detections_dir_root_path, directory))
            max_count_edge_pixels, max_count_edge_pixels_img, in_focus_image_path = self.find_in_focus_image(
                images_paths)
            if in_focus_image_path is not None:
                self.in_focus_images_list.append(in_focus_image_path)
                metadata_file_path = os.path.join(self.detections_dir_root_path, directory, "metadata_1.json")
                if os.path.exists(metadata_file_path):
                    self.update_metadata(metadata_file_path, {"in_focus_image": os.path.basename(in_focus_image_path)})
                else:
                    self.logger.warning("Metadata file not found in directory: ", directory)
            else:
                self.logger.warning("No in-focus image found in directory: ", directory)

    def find_largest_pollen_detection_image_dimension(self):
        for in_focus_file_path in self.in_focus_images_list:
            img = cv.imread(in_focus_file_path, cv.IMREAD_GRAYSCALE)
            if img is not None:
                height, width = img.shape
                if height > self.max_pollen_detection_image_dimension[0] and width > self.max_pollen_detection_image_dimension[1]:
                    self.max_pollen_detection_image_dimension = (height, width)
        self.logger.info("Largest pollen detection image dimension: " +  str(self.max_pollen_detection_image_dimension))

    def update_detection_directories_list(self):
        for root, dirs, _ in os.walk(self.detections_dir_root_path):
            for directory in dirs:
                self.detections_dirs_path_list.append(directory)

    @staticmethod
    def update_metadata(metadata_file_path, sub_metadata_dict):
        with open(metadata_file_path, 'r') as metadata_file:
            metadata = json.load(metadata_file)
            metadata.update(sub_metadata_dict)

        with open(metadata_file_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

    def perform_segmentation(self):
        # if using Apple MPS, fall back to CPU for unsupported ops
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

        # select the device for computation
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")
        print(f"using device: {device}")

        if device.type == "cuda":
            # use bfloat16 for the entire notebook
            torch.autocast("cuda", dtype=torch.bfloat16).__enter__()
            # turn on tfloat32 for Ampere GPUs (https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices)
            if torch.cuda.get_device_properties(0).major >= 8:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
        elif device.type == "mps":
            print(
                "\nSupport for MPS devices is preliminary. SAM 2 is trained with CUDA and might "
                "give numerically different outputs and sometimes degraded performance on MPS. "
                "See e.g. https://github.com/pytorch/pytorch/issues/84936 for a discussion."
            )

        checkpoint = self.sam2_model_path
        model_cfg = "configs/sam2/sam2_hiera_l.yaml"

        # clear the global hydra state
        # hydra.core.global_hydra.GlobalHydra.instance().clear()
        # self.logger.info(os.path.dirname(model_cfg))
        # hydra.initialize_config_module(os.path.dirname(model_cfg), version_base='1.2')

        predictor = SAM2ImagePredictor(build_sam2(model_cfg, checkpoint, device=device))

        for directory in self.detections_dirs_path_list:
            metadata_file_path = os.path.join(self.detections_dir_root_path, directory, "metadata_1.json")
            with open(metadata_file_path, 'r') as metadata_file:
                metadata = json.load(metadata_file)
                in_focus_image_path = os.path.join(self.detections_dir_root_path, directory, metadata["in_focus_image"])
                logging.info("Segmenting image: " + in_focus_image_path)
                # img = cv.imread(in_focus_image_path, cv.IMREAD_GRAYSCALE)
                # find image size
                if os.path.exists(in_focus_image_path):
                    with Image.open(in_focus_image_path) as img:
                        img = np.array(img.convert("RGB"))
                        height, width, _ = img.shape
                        predictor.set_image(img)
                        input_point = np.array([[int(height/2), int(width/2)]])
                        input_label = np.array([1])
                        masks, scores, _ = predictor.predict(point_coords=input_point, point_labels=input_label, multimask_output=True)
                        # save the mask
                        mask = masks[0]
                        mask = mask * 255
                        mask = mask.astype(np.uint8)
                        mask = cv.resize(mask, (width, height), interpolation=cv.INTER_NEAREST)
                        mask_path = os.path.join(self.detections_dir_root_path, directory, "sam2_segmentation_mask.png")
                        cv.imwrite(mask_path, mask)
                        self.update_metadata(metadata_file_path, {"sam2_segmentation_mask": "sam2_segmentation_mask.png"})

                        # save the prompt image
                        plt.figure(figsize=(10, 10))
                        plt.imshow(img)
                        segmentation_utils.show_points(input_point, input_label, plt.gca())
                        plt.axis('on')
                        plt.savefig(os.path.join(self.detections_dir_root_path, directory, "sam2_segmentation_prompt_image.png"))
                        plt.show()
                        plt.close()

                        mask = masks[:1]
                        score = scores[:1]
                        inverted_mask, inverted_dilated_mask = segmentation_utils.perform_dilation(mask, score)

                        # save the image after applying segmentation mask
                        segmentation_utils.show_masks(img, inverted_mask, score, point_coords=input_point, input_labels=input_label, borders=True, save=True, filepath=os.path.join(self.detections_dir_root_path, directory, "sam2_segmentation_mask_applied.png"))

                        # save the image after applying segmentation mask and dilation
                        segmentation_utils.show_masks(img, inverted_dilated_mask, score, point_coords=input_point, input_labels=input_label, borders=True, save=True, filepath=os.path.join(self.detections_dir_root_path, directory, "sam2_segmentation_mask_applied_after_dilation.png"))

    def run(self):
        self.logger.info('Running post processing')
        self.update_detection_directories_list()
        self.logger.info('Detection directories list updated')

        # Find the in-focus image for each pollen detection image
        self.find_in_focus_images_and_update_metadata()
        self.logger.info('In-focus images found and metadata updated')

        # Find the largest pollen detection image dimension
        self.find_largest_pollen_detection_image_dimension()
        self.logger.info('Largest pollen detection image dimension found')

        # TODO - Add more post processing steps here
        # Generate segmented in focus images using SAM-2 model
        self.perform_segmentation()

        # Use the largest pollen detection image dimension to create a blank image with gray background
        # Create image for clustering by adding an in-focus segmented image to a blank image with gray background
        self.logger.info('Post processing completed')



