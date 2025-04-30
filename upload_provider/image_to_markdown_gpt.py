
"""
Utility: convert an uploaded image (Werkzeug FileStorage) to
GitHub-flavoured Markdown using an OpenAI Vision model.

Environment:
  * OPENAI_API_KEY – already set in your container / host
"""

import base64
from typing import Union, IO
from openai import OpenAI

client = OpenAI(timeout=60.0)          # uses OPENAI_API_KEY from env, 60 second timeout

def _encode_image(file_obj: Union[IO[bytes], "FileStorage"]) -> str:
    """
    Return a data-URL string (data:image/…;base64,...) that the
    Chat Completions endpoint accepts.
    """
    mime = getattr(file_obj, "mimetype", None) or "image/png"
    b64 = base64.b64encode(file_obj.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def image_to_markdown(file_storage, detail: str = "high") -> str:
    """
    Send the image to the model and return the Markdown transcription.
    """
    data_url = _encode_image(file_storage)

    response = client.chat.completions.create(
        model="gpt-4.1",  # any vision-capable model is fine
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Transcribe every piece of text in this image, and make sure to correct any spelling errors (do not change spelling of names or places or any other proper nouns)."
                            "re-create the layout in Markdown. "
                            "Preserve headings, tables, and structure of the document."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url, "detail": detail},
                    },
                ],
            }
        ]
    )

    return response.choices[0].message.content.strip()
