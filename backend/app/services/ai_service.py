import base64

from google import genai
from google.genai import types

from app.core.config import settings
from app.services.cloudinary_service import CloudinaryService


class AIService:

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.cloudinary = CloudinaryService()

    # ============================================================
    # GENERATE CAPTION
    # ============================================================

    async def generate_caption(
        self,
        topic: str,
        platform: str,
        tone: str,
    ) -> dict:

        prompt = f"""
You are an expert social media copywriter.

Generate social media content for the following:

Topic:
{topic}

Platform:
{platform}

Tone:
{tone}

Return ONLY valid JSON in exactly this format:

{{
    "caption": "Your complete social media caption here",
    "hashtags": [
        "#Hashtag1",
        "#Hashtag2",
        "#Hashtag3",
        "#Hashtag4",
        "#Hashtag5"
    ]
}}

Requirements:
- Write one natural and engaging caption.
- Match the requested tone.
- Optimize the writing for the requested platform.
- Make it suitable for a real social media post.
- Generate 5 relevant hashtags.
- Every hashtag must start with #.
- Do not put hashtags inside the caption.
- Do not explain your reasoning.
- Return ONLY the JSON object.
"""

        response = await self.client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        text = (response.text or "").strip()

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        import json

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            )

        caption = str(data.get("caption", "")).strip()
        hashtags = data.get("hashtags", [])

        if not caption:
            raise RuntimeError(
                "Gemini returned an empty caption."
            )

        if not isinstance(hashtags, list):
            raise RuntimeError(
                "Gemini returned invalid hashtags."
            )

        hashtags = [
            str(tag).strip()
            for tag in hashtags
            if str(tag).strip()
        ]

        return {
            "caption": caption,
            "hashtags": hashtags,
        }

    # ============================================================
    # GENERATE IMAGE
    # ============================================================

    async def generate_image(
        self,
        topic: str,
        platform: str,
        aspect_ratio: str = "4:5",
    ) -> str:

        prompt = f"""
Create a high-quality social media image.

Topic:
{topic}

Platform:
{platform}

Requirements:
- Create a visually striking professional social media graphic.
- Clearly communicate the topic.
- Use a modern, polished visual style.
- Make it suitable for a business social media account.
- Use attractive composition and professional lighting.
- Avoid unnecessary text.
- Do not include logos of real companies.
- Do not include watermarks.
- Generate the image only.
"""

        response = await self.client.aio.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                ),
            ),
        )

        image_bytes = None
        mime_type = "image/png"

        for part in response.parts:

            if part.inline_data is not None:

                image_bytes = part.inline_data.data

                if part.inline_data.mime_type:
                    mime_type = part.inline_data.mime_type

                break

        if not image_bytes:
            raise RuntimeError(
                "Gemini did not return an image."
            )

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        data_uri = (
            f"data:{mime_type};base64,{encoded_image}"
        )

        upload_result = await self.cloudinary.upload_image(
            file=data_uri,
            folder="social-media-platform/ai-generated",
        )

        image_url = upload_result.get("secure_url")

        if not image_url:
            raise RuntimeError(
                "Cloudinary did not return an image URL."
            )

        return image_url