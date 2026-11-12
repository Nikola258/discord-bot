import discord
from discord import app_commands
from discord.ext import commands

from vision.image_processing import load_image, InvalidImageError
from vision.face_detection import FaceDetector
from vision.face_classifier import classify_face_shape, calculate_fat_score, get_fat_level
from bot.roles import assign_face_shape_role, assign_fat_level_role, FACE_SHAPE_DISPLAY
from database import statistics


class FatCheckCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
        statistics.record_scan(
            user_id=str(interaction.user.id),
            face_shape=face_shape,
            score=score,
            fat_level=fat_level,
        )

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
