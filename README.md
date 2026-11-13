# Discord Bot - Face Shape & Fun Roles
Project for school, a discord bot that makes the server more fun by analyzing user uploaded face image, estimates its visible face shape, and and giving them funny roles.

**Important:** This bot is for entertainment only. Face shape cannot determine a person body fat, weight or obesity level.
### Bot functionality

- [x] Checks that an image was uploaded in fat check channel 
- [x] Estimates visible face shape in the image 
- [x] Gives the user their result with a role
- [x] Saves the anonymous data to a JSON

### Extra functionality

- [x] Remove the user's previous face-shape role when assigning a new one 
- [x] Delete uploaded photos after processing
- [ ] Prevent users from checking repeatedly(spam) 
- [x] Command !tips for extra tips how to stay healthy
- [x] Top list of most and least fat people


### ## Technologies

- Discord API - for roles [API reference](https://docs.discord.com/developers/reference)
- Python - Main language
- OpenCV - Image loading, resizing and processing [Image processing guide](https://docs.opencv.org/4.13.0/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- MediaPipe - Detects facial landmarks [ML to see face landmarks](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker#python)
- JSON - Storing anonymous statistics
- Git and GitHub - Version control and source code hosting
- Docker – Running the bot in an isolated container
- Docker Compose – Managing the container
- Dockge – Web interface for managing Docker Compose stacks

### How the complete system will work

1. A user uploads a photo in the designated Discord channel
2. The bot checks the uploaded image
3. MediaPipe detects facial landmarks
4. The bot estimates the visible face shape
5. The bot sends the result to Discord and assigns funny role
6. Statistics are saved in a JSON file

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

## Configuration

### ### Environment variables

**Environment variables file, .env:**

```dotenv
# Discord
DISCORD_TOKEN=your_bot_token_here

# Channels
FAT_CHECK_CHANNEL_ID=your_channel_id_here

# Image processing
MAX_IMAGE_SIZE_MB=8
```

### Git ignore

The `.gitignore` file should exclude private configuration and temporary files:

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
### Requirements

```requirements.txt

discord.py
python-dotenv
opencv-python
mediapipe
numpy
pytest

```

## Discord role configuration

Central role configuration.

`bot/roles.py` example:

```
FACE_SHAPE_ROLES = {
    "oval":      1570369164080586822,
    "round":     1570369839564857424,
    "square":    1570369865166884924,
    "triangle":  1570369904102871100,
    "oblong":    1570370162106830918,
    "rectangle": 1570370410099253255,
}
```

### Discord bot permissions

The bot requires those permissions:

|Permission|Purpose|
|---|---|
|Manage Roles|Assign and remove roles|
|View Channels|Access the checking channel|
|Send Messages|Send results|
|Read Message History|Read relevant messages|

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

## Hosting method: Docker

The Discord bot is hosted on an Ubuntu Server virtual machine using Docker and Docker Compose.
Dockge is used to manage the Docker Compose stack through a web interface.

### Hosting environment

|Component|Configuration|
|---|---|
|Virtualization|Proxmox VE|
|Operating system|Ubuntu Server 24.04|
|Container runtime|Docker Engine|
|Container management|Docker Compose|
|Web management|Dockge|
|Container name|`discord-bot`|
|Deployment directory|`/opt/stacks/discord-bot/`|
|Source code directory|`/opt/stacks/discord-bot/source/`|
|Persistent statistics|`/opt/stacks/discord-bot/data/statistics.json`|
|Environment variables|`/opt/stacks/discord-bot/.env`|

### Deployment structure on the server

The server has a separate deployment directory containing the Docker configuration and the GitHub repository checkout:

```text
/opt/stacks/discord-bot/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
│
├── data/
│   └── statistics.json
│
└── source/
    ├── main.py
    ├── config.py
    ├── bot/
    ├── vision/
    ├── database/
    ├── models/
    └── requirements.txt
```

The Dockerfile builds the Python environment, installs the required dependencies, and copies the application source into the Docker image.
Docker Compose manages the bot container and its settings.

### Persistent data

The statistics file is stored outside the container and mounted into it:

```text
Host:
/opt/stacks/discord-bot/data/statistics.json

Container:
/app/database/statistics.json
```

This means the statistics file remains on the server when the container is rebuilt or replaced.
The `.env` file is also stored on the server, separately from the GitHub repository.

### Network configuration

The bot connects to Discord using an outbound internet connection.
No incoming public port is required for the bot, and the container does not publish any host ports.

### How to update the bot

The bot is updated manually when new code is pushed to GitHub.
#### 1 Edit the code

Make changes to the project files locally.

#### 2 Push changes to GitHub

Commit and push the changes to the `main` branch.

#### 3 Pull the latest code on the server

Connect to the Ubuntu Server VM and run:

```bash
cd /opt/stacks/discord-bot/source
git pull origin main
```

Downloads the latest changes from GitHub.

#### Step 4 – Rebuild and redeploy the container

Move to the Docker deployment directory:

```bash
cd /opt/stacks/discord-bot
```

Rebuild the Docker image and start the updated container:

```bash
docker compose up -d --build
```

This builds a new image using the updated source code and recreates the container if needed.

The same can be done through Dockge by updating the source checkout first and then redeploying the stack with a build.


## Hosting limitations

The current hosting setup is a manual deployment process.

It does not automatically pull changes from GitHub. Each update requires pulling the latest code and rebuilding the Docker image.

Automatic deployment using GitHub Actions or another CI/CD solution could be added in the future.

## Privacy and responsible use

- Users should voluntarily submit their own photos
- Statistics may contain Discord user IDs and usernames
- Photos should not displayed on chat or saved
