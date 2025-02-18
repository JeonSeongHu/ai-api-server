from typing import Any, List
from pydantic import BaseModel


class ControlNetArgs(BaseModel):
    image: str
    batch_images: str = ""
    control_mode: str = "Balanced"
    enabled: bool = True
    guidance_end: int = 1
    guidance_start: int = 0
    low_vram: bool = False
    model: str = "control_v11p_sd15_openpose [cab727d4]"
    module: str = "openpose"
    pixel_perfect: bool = False
    processor_res: int = -1
    resize_mode: str = "Crop and Resize"
    save_detected_map: bool = False
    threshold_a: int = -1
    threshold_b: int = -1
    weight: float = 0.3


class ReactorArgs():
    def __init__(self, 
                 src_img: str, 
                 enable: bool = True, 
                 face_numbers: str = '0', 
                 target_face_numbers: str = '0', 
                 model_path: str = '/app/stable-diffusion-webui/models/insightface/inswapper_128.onnx', 
                 restore_face: str = 'CodeFormer', 
                 restore_visibility: int = 1, 
                 restore_face_upscale: bool = True, 
                 upscaler_type: str = None, 
                 upscaler_scale: int = 1, 
                 upscaler_visibility: int = 1, 
                 swap_in_source_img: bool = True, 
                 swap_in_generated_img: bool = True, 
                 console_log_level: int = 1, 
                 gender_detection_source: int = 0, 
                 gender_detection_target: int = 0, 
                 save_original_images: bool = False, 
                 codeformer_weight: float = 0.5, 
                 source_image_hash_check: bool = False, 
                 target_image_hash_check: bool = False, 
                 device: str = "CUDA", 
                 face_mask_correction: bool = True, 
                 select_source: int = 0, 
                 face_model_filename: str = "", 
                 source_folder_path: str = "", 
                 skip: str = None, 
                 random_image_selection: bool = True, 
                 force_upscale: bool = True, 
                 face_detection_threshold: float = 0.6, 
                 max_faces_to_detect: int = 1):
        """
        Args:
            src_img (str): The base64 encoded image.
            enable (bool): Enable ReActor.
            face_numbers (str): Comma separated face number(s) from swap-source image.
            target_face_numbers (str): Comma separated face number(s) for target image (result).
            model_path (str): The path to the model.
            restore_face (str): Restore Face: None, CodeFormer, GFPGAN.
            restore_visibility (int): Restore visibility value.
            restore_face_upscale (bool): Restore face -> Upscale.
            upscaler_type (str): Upscaler type (None if not needed).
            upscaler_scale (int): Upscaler scale value.
            upscaler_visibility (int): Upscaler visibility (if scale = 1).
            swap_in_source_img (bool): Swap in source image.
            swap_in_generated_img (bool): Swap in generated image.
            console_log_level (int): Console Log Level (0 - min, 1 - med, 2 - max).
            gender_detection_source (int): Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only).
            gender_detection_target (int): Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only).
            save_original_images (bool): Save the original image(s) made before swapping.
            codeformer_weight (float): CodeFormer Weight (0 = maximum effect, 1 = minimum effect), 0.5 - by default.
            source_image_hash_check (bool): Source Image Hash Check, True - by default.
            target_image_hash_check (bool): Target Image Hash Check, False - by default.
            device (str): CPU or CUDA (if available), CPU - by default.
            face_mask_correction (bool): Face Mask Correction.
            select_source (int): Select Source, 0 - Image, 1 - Face Model, 2 - Source Folder.
            face_model_filename (str): Filename of the face model (from "models/reactor/faces"), e.g. elena.safetensors, don't forget to set #22 to 1.
            source_folder_path (str): The path to the folder containing source faces images, don't forget to set #22 to 2.
            skip (None): Skip it for API.
            random_image_selection (bool): Randomly select an image from the path.
            force_upscale (bool): Force Upscale even if no face found.
            face_detection_threshold (float): Face Detection Threshold.
            max_faces_to_detect (int): Maximum number of faces to detect (0 is unlimited).
        """
        self.src_img = src_img
        self.enable = enable
        self.face_numbers = face_numbers
        self.target_face_numbers = target_face_numbers
        self.model_path = model_path
        self.restore_face = restore_face
        self.restore_visibility = restore_visibility
        self.restore_face_upscale = restore_face_upscale
        self.upscaler_type = upscaler_type
        self.upscaler_scale = upscaler_scale
        self.upscaler_visibility = upscaler_visibility
        self.swap_in_source_img = swap_in_source_img
        self.swap_in_generated_img = swap_in_generated_img
        self.console_log_level = console_log_level
        self.gender_detection_source = gender_detection_source
        self.gender_detection_target = gender_detection_target
        self.save_original_images = save_original_images
        self.codeformer_weight = codeformer_weight
        self.source_image_hash_check = source_image_hash_check
        self.target_image_hash_check = target_image_hash_check
        self.device = device
        self.face_mask_correction = face_mask_correction
        self.select_source = select_source
        self.face_model_filename = face_model_filename
        self.source_folder_path = source_folder_path
        self.skip = skip
        self.random_image_selection = random_image_selection
        self.force_upscale = force_upscale
        self.face_detection_threshold = face_detection_threshold
        self.max_faces_to_detect = max_faces_to_detect
    
    def to_list(self)-> List:
        return [
            self.src_img,
            self.enable,
            self.face_numbers,
            self.target_face_numbers,
            self.model_path,
            self.restore_face,
            self.restore_visibility,
            self.restore_face_upscale,
            self.upscaler_type,
            self.upscaler_scale,
            self.upscaler_visibility,
            self.swap_in_source_img,
            self.swap_in_generated_img,
            self.console_log_level,
            self.gender_detection_source,
            self.gender_detection_target,
            self.save_original_images,
            self.codeformer_weight,
            self.source_image_hash_check,
            self.target_image_hash_check,
            self.device,
            self.face_mask_correction,
            self.select_source,
            self.face_model_filename,
            self.source_folder_path,
            self.skip,
            self.random_image_selection,
            self.force_upscale,
            self.face_detection_threshold,
            self.max_faces_to_detect,
            ]
class ScriptArgs(BaseModel):
    args: List[Any] = []

class AlwaysOnScripts(BaseModel):
    ControlNet: ScriptArgs = ScriptArgs()
    reactor: ScriptArgs = ScriptArgs()

class T2IArgs(BaseModel):
    prompt: str = ""
    negative_prompt: str = ""
    alwayson_scripts: AlwaysOnScripts = {}
    sampler_name: str = "DPM++ 2M Karras"
    batch_size: int = 1
    cfg_scale: int = 7
    seed: int = 42
    seed_enable_extras: bool = True
    seed_resize_from_h: int = -1
    seed_resize_from_w: int = -1
    steps: int = 30
    height: int = 720
    width: int = 512
    comments: dict = {}
    disable_extra_networks: bool = False
    do_not_save_grid: bool = False
    do_not_save_samples: bool = False
    enable_hr: bool = False
    hr_negative_prompt: str = ""
    hr_prompt: str = ""
    hr_resize_x: int = 0
    hr_resize_y: int = 0
    hr_scale: int = 2
    hr_second_pass_steps: int = 0
    hr_upscaler: str = "Latent"
    n_iter: int = 1
    override_settings: dict = {}
    override_settings_restore_afterwards: bool = True
    restore_faces: bool = False
    s_churn: float = 0.0
    s_min_uncond: int = 0
    s_noise: float = 1.0
    s_tmax: int = None
    s_tmin: float = 0.0
    script_args: list = []
    script_name: str = None
    styles: list = []
    subseed: int = -1
    subseed_strength: int = 0
    tiling: bool = False


