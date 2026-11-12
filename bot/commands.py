import random

import discord
from discord import app_commands
from discord.ext import commands

from vision.image_processing import load_image, InvalidImageError
from vision.face_detection import FaceDetector
from vision.face_classifier import classify_face_shape, calculate_fat_score, get_fat_level
from bot.roles import assign_face_shape_role, assign_fat_level_role, FACE_SHAPE_DISPLAY
from database import statistics


HEALTH_TIPS = (
    "Drink water regularly throughout the day",
    "Take a short walk each day",
    "Include fruits and vegetables in your meals",
    "Aim for 7–9 hours of sleep when you can",
    "Take a break from sitting now and then",
    "Try moving your body, even for 10 minutes",
    "Eat regular meals that work for you",
    "Spend a little time outdoors",
    "Brush your teeth twice a day",
    "Make time to care for your mental wellbeing",
)


class FatCheckCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="tips",
        description="Get a healthy-living tip and free food and exercise resources.",
    )
    async def tips(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"**A little healthy-living tip**\n{random.choice(HEALTH_TIPS)}\n\n"
            "**Free resources**\n"
            "🍽️ [BBC Good Food — healthy recipes]"
            "(https://www.bbcgoodfood.com/recipes/collection/healthy-recipes)\n"
            "🏋️ [DAREBEE — home workouts]"
            "(https://darebee.com/)\n"
            "🧘 [NHS — exercise and activity resources]"
            "(https://www.nhs.uk/better-health/get-active/how-to-be-more-active/)\n\n"
            "*General wellbeing ideas only, not medical advice.*"
        )

    @app_commands.command(
        name="info",
        description="Show what the bot does and which commands are available.",
    )
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "**About this bot**\n"
            "Upload a photo with `/fatcheck` for an face shape role, "
            "funny fat score and matching role for it\n\n"
            "**Available commands**\n"
            "• `/fatcheck` - Analyze an uploaded photo\n"
            "• `/info` - Show this information\n"
            "• `/tips` - Get a healthy-living tip and free resources\n\n"
            "**Planned commands**\n"
            "• `/list` - List users near a score\n"
            "• `/topfat` and `/topskinny` - Score rankings\n\n"
            "*The results are just for fun, are not a health assessment, "
            "and should not be taken seriously.*"
        )

    @app_commands.command(
        name="fatcheck",
        description="Upload a photo to check your face shape and fat score!",
    )
    @app_commands.describe(foto="The photo you want to check")
    async def fatcheck(
        self,
        interaction: discord.Interaction,
        foto: discord.Attachment,
    ):
        # Acknowledge immediately so Discord doesn't time out
        await interaction.response.defer(thinking=True)

        # --- 1. Download the image ---
        try:
            image_bytes = await foto.read()
        except Exception:
            await interaction.followup.send(
                "❌ Could not download your image. Please try again."
            )
            return

        # --- 2. Validate and decode the image ---
        try:
            image_rgb = load_image(image_bytes)
        except InvalidImageError as e:
            await interaction.followup.send(f"❌ {e}")
            return

        # --- 3. Detect facial landmarks ---
        try:
            detector = FaceDetector()
            faces = detector.detect(image_rgb)
            detector.close()
        except FileNotFoundError:
            await interaction.followup.send(
                "❌ The face detection model is missing. "
                "Make sure `models/face_landmarker.task` is present."
            )
            return
        except Exception:
            await interaction.followup.send(
                "❌ Face detection failed. Please try a clearer photo."
            )
            return

        if not faces:
            await interaction.followup.send(
                "😕 No face detected in your photo. "
                "Try a clearer front-facing photo with good lighting."
            )
            return

        landmarks = faces[0]

        # --- 4. Classify face shape + calculate score ---
        try:
            face_shape = classify_face_shape(landmarks)
            score = calculate_fat_score(landmarks)
            fat_level = get_fat_level(score)
        except ValueError:
            await interaction.followup.send(
                "❌ Could not analyse your face. "
                "Please upload a clearer front-facing photo."
            )
            return

        shape_display = FACE_SHAPE_DISPLAY.get(face_shape, face_shape)

        # --- 5. Assign both roles ---
        shape_role = await assign_face_shape_role(interaction.user, face_shape)
        fat_role = await assign_fat_level_role(interaction.user, fat_level)

        # --- 6. Save to JSON database ---
        user_id = str(interaction.user.id)
        existing = statistics.get_user(user_id) or {}
        statistics.update_user(user_id, {
            "username": str(interaction.user),
            "scans": existing.get("scans", 0) + 1,
            "last_shape": face_shape,
            "last_score": score,
            "last_fat_level": fat_level,
        })

        # --- 7. Build score bar (visual) ---
        filled = round(score / 10)
        bar = "█" * filled + "░" * (10 - filled)

        # --- 8. Reply with result ---
        shape_role_text = f" → **{shape_role.name}** role assigned!" if shape_role else ""
        fat_role_text = f" → **{fat_role.name}** role assigned!" if fat_role else ""

        await interaction.followup.send(
            f"**🔍 Fat Check result for {interaction.user.mention}**\n\n"
            f"**Face shape:** {shape_display}{shape_role_text}\n"
            f"**Fat score:** {score}/100  `[{bar}]`\n"
            f"**Level:** {fat_level}{fat_role_text}\n\n"
            f"*(Just for fun — don't take it seriously!)*"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(FatCheckCommands(bot))
