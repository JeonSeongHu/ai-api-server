from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import io
import uvicorn
from datetime import datetime
import base64
import time
from typing import List
from PIL import Image
from logger import logger
import utils
import upload
from models import FaceListPayload, FaceSwapPayload, PresetParam, UploadImgParam, getBuildFaceModelPayload
from config import WEBUI_URL, BUCKET_PREFIX, FORMAT_DATE


app = FastAPI()


# @@ APIHandler ############################
@app.get("/api/status/")
async def upload_item():
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "200", "datetime": time_str}


@app.post("/test/webui/build")
async def getFaceModel(item: FaceListPayload):
    result = await buildFaceModel(req_id="123id", img_str_list=item.img_list)
    return {"result": result}


@app.post("/test/webui/swap")
async def getSwappedFace(item: FaceSwapPayload):
    result = await swapFaceApi(req_id="123id", face_model=item.face_model, src_img=item.src_img)
    return {"result": result}


@app.get("/test/img/preset")
async def getImagePreset(item: PresetParam):
    result_imgs = utils.loadPresetImages(is_male=item.is_male, is_black=item.is_black, univ=item.univ, cnt=1)
    image_bytes = io.BytesIO()
    result_imgs[0].save(image_bytes, format="PNG")
    image_bytes.seek(0)
    return StreamingResponse(content=image_bytes, media_type="image/png")


@app.post("/test/img/upload")
async def uploadImage(item: UploadImgParam):
    decoded_bytes = base64.b64decode(item.image)

    # Create a BytesIO object from the decoded bytes
    image_bytes_io = io.BytesIO(decoded_bytes)

    # Open the BytesIO object as a PIL Image
    pil_image = Image.open(image_bytes_io)
    
    upload.upload_image_to_gcs(pil_image, f"{item.id}/{item.idx}.png")
    return {"status":"done"}


@app.post("/api/img/process")
async def getBuildFaceModel(item: getBuildFaceModelPayload):
    logger.info("")
    logger.info(f"*********************")
    logger.info(f"Request: {item.id} start")
    logger.info(f"recieved: {len(item.image_list)} images")
    start_time = time.time()
    
    result_urls: List[str] = []
    
    start_time_build = time.time()
    face_model = await buildFaceModel(req_id=item.id, img_str_list=item.image_list)
    end_time_build = time.time()

    preset_img_list = utils.loadPresetImages(is_male=item.param.is_male, is_black=item.param.is_black, univ=item.param.univ, cnt=item.cnt)
    
    start_time_swap = time.time()
    for idx in range(item.cnt):
        result_img_str = await swapFaceApi(req_id=item.id, face_model=face_model, src_img=preset_img_list[idx])
        result_img = utils.decodeBase642Img(result_img_str)

        # @@ TODO : OpenCV -> result_img modification

        file_url = upload.upload_image_to_gcs(result_img, f"{item.id}/{idx}.png")
        result_urls.append(file_url)
        logger.info(f"{idx+1}/{item.cnt} Done!")
    end_time_swap = time.time()
    
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Done id: {item.id}")
    logger.info(f"Build time: {(end_time_build-start_time_build):.2f} seconds")
    logger.info(f"Swap time: {(end_time_swap-start_time_swap):.2f} seconds")
    logger.info(f"Total time: {execution_time:.2f} seconds")
    logger.info(f"*********************")

    
    return {"id": item.id, "images" : result_urls}


# @@ WebUI_API ############################
async def buildFaceModel(req_id:str, img_str_list: List[str]) -> str | None:
    try:
        face_build_url = WEBUI_URL + "/faceswaplab/build"
        (is_succ ,response) = await utils.requestPostAsync(face_build_url, img_str_list)

        # TODO: upload intermediate base64_safetensors to bucket
        if is_succ:
            logger.info(f"Success - build_face - req_id: {req_id}")
            return response
        else:
            logger.error(f"Error - build_face - req_id: {req_id} - detail: RequestFail")
            return
    except Exception as e:
        logger.error(f"Error - build_face - req_id: {req_id} - detail: {e}")
        return


async def swapFaceApi(req_id: str, face_model: str, src_img: str)-> str:
    try:
        face_swap_url = WEBUI_URL + "/faceswaplab/swap_face"
        src_img_base64 = utils.encodeImg2Base64(src_img)
        swap_api_payload = dict({
        "image": src_img_base64,
        "units": [
                {
                    "source_face": face_model,
                    "same_gender": True,
                    "faces_index": [
                        0
                    ]
                }
            ]
        })
        (is_succ, response) = await utils.requestPostAsync(face_swap_url, swap_api_payload)
        if is_succ:
            logger.info(f"Success-swap_face-req_id:{req_id}")
            return response["images"][0]
        else:
            logger.error("Error - swap_face - req_id: {req_id} - detail: RequestFail")
            return {"error": response}
    except Exception as e:
        logger.error(f"Error - swap_face - req_id: {req_id} - detail: {e}")
        return {"error" :e}


class ErrorResponse(BaseModel):
    detail: str


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail":"Internal server error", "exception": exc}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
