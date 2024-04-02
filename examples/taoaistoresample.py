from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from superagi.helper.resource_helper import ResourceHelper
from superagi.llms.base_llm import BaseLlm
from superagi.tools.base_tool import BaseTool
import os
import replicate

from superagi.helper.s3_helper import S3Helper
from superagi.resource_manager.file_manager import FileManager

import json


class AdInpaintSchema(BaseModel):
    image_filename: str = Field(..., description="the image filename, if no value is given keep the default value as 'None'")
    prompt: str = Field(..., description="the prompt we want to do, if no value is given keep the default value as ''.")
    number_of_images: int = Field(..., description="the number of images we want to generate, if no value is given keep the default value as 1")
class AdInpaintTool(BaseTool):
    """
    mask generation tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.

    Model:
        logerzhu/ad-inpaint
    """
    llm: Optional[BaseLlm] = None
    name = "Ad内画工具"
    description = (
        "A tool for generating image based on the prompt."
        "Input should be a the image filename, the prompt  "
    )
    args_schema: Type[AdInpaintSchema] = AdInpaintSchema
    resource_manager: Optional[FileManager] = None
    
    def _execute(self, image_filename: str, prompt: str, number_of_images: int) -> tuple:
        """
        Execute the impaint tool

        Args:
            query : The query to search for.

        Returns:
            Search result summary along with related links
        """
        # we get the downloadable file name of s3
        image_url = ResourceHelper.get_resource_download_url(self, image_filename)

        client = replicate.Client(api_token=self.get_tool_config('REPLICATE_API_TOKEN'))
        output = client.run(
            "logerzhu/ad-inpaint:b1c17d148455c1fda435ababe9ab1e03bc0d917cc3cf4251916f22c45c83c7df",
            input={
                "pixel": "512 * 512",
                "scale": 3,
                "prompt": prompt,
                "image_num": number_of_images,
                "image_path": image_url,
                "manual_seed": -1,
                "product_size": "0.5 * width",
                "guidance_scale": 7.5,
                "negative_prompt": "illustration, 3d, sepia, painting, cartoons, sketch, (worst quality:2)",
                "num_inference_steps": 20
            }
        )
        images = (output)
        
        print(images)
        for image in images:
            self.resource_manager.download_file_from_url(image)
            print(f'{image} has been stored \n')

        return images       
