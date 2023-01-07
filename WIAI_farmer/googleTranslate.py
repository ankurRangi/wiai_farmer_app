import os
import six
from google.cloud import translate_v2
from . import schemas

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"./translateKey.json"

# async def translate_text(text, target):
#     translate_client = translate_v2.Client()
#     output = translate_client.translate(text, target_language=target)
#     return output

async def translate_text(target, text):
    translate_client = translate_v2.translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    return result


async def join_farmer_data(farmer: schemas.FarmerDetail, lang: str):
    # Creating the string format for conversion
    joined_data = str(
        farmer.farmer_name
        + ","
        + farmer.state_name
        + ","
        + farmer.district_name
        + ","
        + farmer.village_name
    )
    output = await translate_text(joined_data, lang)
    output = output["translatedText"]
    translated_data = output.split(",")
    return translated_data