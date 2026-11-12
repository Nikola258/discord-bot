# Discord bot that checks fat level of users
Project for school, a discord bot that makes the server more fun by checking the fat levels of users and giving them funny roles.


### Bot functionality's:

- [ ] Checks that an image was uploaded in fat check channel 
- [ ] Estimates visible face shape in the image 
- [ ] Gives the user their result with a role
- [ ] Saves the anonymous data to a JSON(used to count average obesity level in the server)

### Extra functionality(things that can be useful to make later):

- [ ] Remove the user's previous face-shape role when assigning a new one 
- [ ] Delete uploaded photos after processing
- [ ] Prevent users from checking repeatedly(spam) 
- [ ] Command !tips for extra tips how to stay healthy
- [ ] Top list of most and least fat people


### Technologies we plan to use:

- Discord API - for roles [API reference](https://docs.discord.com/developers/reference)
- Python - Main language
- OpenCV - Image loading, resizing and processing [Image processing guide](https://docs.opencv.org/4.13.0/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- MediaPipe - Detects facial landmarks [ML to see face landmarks](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker#python)
- JSON - Storing anonymous statistics
- Git - Version control

### How the complete system will work

[[Discord-Bot-Flow.excalidraw]]

### File structure i would use

```File 

fat-checker-bot/
│
├── main.py
├── config.py
│
├── bot/
│   ├── __init__.py
│   ├── commands.py
│   ├── events.py
│   └── roles.py
│
├── vision/
│   ├── __init__.py
│   ├── image_processing.py
│   ├── face_detection.py
│   └── face_classifier.py
│
├── database/
│   ├── __init__.py
│   ├── statistics.py
│   └── statistics.json
│
├── utils/
│   ├── __init__.py
│   ├── cooldown.py
│   ├── image_cleanup.py
│   └── validation.py
│
├── models/
│   └── face_landmarker.task
│
├── tests/
│   ├── test_image_processing.py
│   ├── test_face_detection.py
│   └── test_statistics.py
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md

```

What each file does:

| File                  | Responsibility                |
| --------------------- | ----------------------------- |
| `main.py`             | Starts the bot                |
| `config.py`           | Configuration and settings    |
| `commands.py`         | Bot commands                  |
| `events.py`           | Detects uploaded photos       |
| `roles.py`            | Assigns and removes roles     |
| `image_processing.py` | Prepares images               |
| `face_detection.py`   | Uses MediaPipe                |
| `face_classifier.py`  | Classifies face shapes        |
| `statistics.py`       | Updates JSON statistics       |
| `cooldown.py`         | Prevents spam                 |
| `image_cleanup.py`    | Deletes temporary image files |
## Configuration for this project

### Configuration files

**Environment variables file, .env:**

```dotenv
# Discord
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here

# Channels
FAT_CHECK_CHANNEL_ID=your_channel_id_here
RESULT_CHANNEL_ID=your_result_channel_id_here

# Permissions / behavior
DELETE_PROCESSED_IMAGES=true
IMAGE_RETENTION_SECONDS=60

# Processing
MAX_IMAGE_SIZE_MB=20
IMAGE_TIMEOUT_SECONDS=20

# Statistics
STATISTICS_FILE=database/statistics.json
```

**Configuration file, config.py:**

```python

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Discord configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

# Channel configuration
FAT_CHECK_CHANNEL_ID = int(
    os.getenv("FAT_CHECK_CHANNEL_ID", "0")
)

RESULT_CHANNEL_ID = int(
    os.getenv("RESULT_CHANNEL_ID", "0")
)

# Image configuration
DELETE_PROCESSED_IMAGES = (
    os.getenv("DELETE_PROCESSED_IMAGES", "true").lower()
    == "true"
)

IMAGE_RETENTION_SECONDS = int(
    os.getenv("IMAGE_RETENTION_SECONDS", "60")
)

MAX_IMAGE_SIZE_MB = int(
    os.getenv("MAX_IMAGE_SIZE_MB", "8")
)

IMAGE_TIMEOUT_SECONDS = int(
    os.getenv("IMAGE_TIMEOUT_SECONDS", "15")
)

# Database
STATISTICS_FILE = BASE_DIR / os.getenv(
    "STATISTICS_FILE",
    "database/statistics.json"
)

# Validate configuration
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is missing!")

if not GUILD_ID:
    raise ValueError("GUILD_ID is missing!")

```

File referenced: `config.py`

Install the required dependency:

```
pip install discord.py python-dotenv
```

For the facial-analysis version, you can separately install OpenCV and MediaPipe.

### Requirements

```requirements.txt

discord.py
python-dotenv
opencv-python
mediapipe
numpy
pytest

```

### Git Ignire

```gitignore

# Secrets
.env

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Temporary images
temp/
uploads/

# IDE
.idea/
.vscode/

# Testing
.pytest_cache/

# Logs
*.log

```

### Discord role configuration

Create a central role configuration.

`bot/roles.py`  for example:

```
FACE_SHAPE_ROLES = 
{    
	"oval": 123456789012345678,    
	"round": 123456789012345679,    
	"square": 123456789012345680,    
	"heart": 123456789012345681,    
	"oblong": 123456789012345682,
}
```

Replace those example numbers with actual Discord role IDs.

Bot Discord permissions:

|Permission|Purpose|
|---|---|
|Manage Roles|Assign and remove roles|
|View Channels|Access the checking channel|
|Send Messages|Send results|
|Read Message History|Read relevant messages|
|Attach Files|Only if sending image attachments|

### Bot commands

| Command | Responsibility | Status |
| --- | --- | --- |
| `/fatcheck {foto}` | Analyze a photo and assign matching roles. | Available |
| `/info` | Show bot information, commands, and a disclaimer. | Available |
| `/tips` | Show a random healthy-living tip and free cooking and exercise resources. | Available |
| `/list` | List users near a score. | Planned |
| `/topfat` | Show the highest scores. | Planned |
| `/topskinny` | Show the lowest scores. | Planned |

### Used discord roles

| Disocord fun Roles | funny role | Role ID             |
| ------------------ | ---------- | ------------------- |
| `stick`            | 🪾stick    | 1570370456983310366 |
| `feather`          | 🪶feather  | 1570370492806995988 |
| `skinny`           | 🦴skinny   | 1570370511681355776 |
| `fat`              | 🫃🏻fat    | 1570370535400149003 |
| `chunky`           | 🍪chunky   | 1570370559294832732 |
| `fatass`           | 🍔fatass   | 1570370853504286783 |



| Face shape  | Funny role      | Role ID             |
| ----------- | --------------- | ------------------- |
| `oval`      | 🥚 Egghead      | 1570369164080586822 |
| `round`     | 🥔 Potato       | 1570369839564857424 |
| `square`    | 🧀 Cheese Block | 1570369865166884924 |
| `triangle`  | 🔻Doritos       | 1570369904102871100 |
| `oblong`    | 🦒 Giraffe      | 1570370162106830918 |
| `rectangle` | 🐊 Crocodile    | 1570370410099253255 |


### Hosting methode

Docker
