# Display settings
DEFAULT_IMAGE_SIZE = (300, 300)
FPS = 120
HEIGHT = 1000
WIDTH = 1600
START_X, START_Y = 0, -300
X_OFFSET, Y_OFFSET = 20, 0

# Images
BG_IMAGE_PATH = 'graphics/0/bg.png'
GRID_IMAGE_PATH = 'graphics/0/gridline.png'
GAME_INDICES = [1, 2, 3] # 0 and 4 are outside of play area
SYM_PATH = 'graphics/0/symbols'

# Text
TEXT_COLOR = 'White'
# You need to provide your own font in the below directory
# I downloaded Kidspace font from https://www.dafont.com/kidspace.font
UI_FONT = 'graphics/font/kidspace.ttf'
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# 5 Symbols for demo
# symbols = {
#     'diamond': f"{SYM_PATH}/0_diamond.png", 
#     'floppy': f"{SYM_PATH}/0_floppy.png",
#     'hourglass': f"{SYM_PATH}/0_hourglass.png",
#     'seven': f"{SYM_PATH}/0_seven.png",
#     'telephone': f"{SYM_PATH}/0_telephone.png"
# }

# 4 Symbols for more wins
symbols = {
    'diamond': f"{SYM_PATH}/0_diamond.png", 
    'floppy': f"{SYM_PATH}/0_floppy.png",
    'hourglass': f"{SYM_PATH}/0_hourglass.png",
    'hourglass2': f"{SYM_PATH}/0_hourglass.png",
    'telephone': f"{SYM_PATH}/0_telephone.png"
}

# Autoplay settings
AUTO_SPIN_INTERVAL = 1000  # Interval between spins in milliseconds

# Button settings
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_FONT_COLOR = 'White'
BUTTON_FONT_SIZE = 25

# Button dimensions and positions
SPIN_BUTTON_POS = (1400, 910)
SPIN_BUTTON_SIZE = (150, 60)
AUTO_BUTTON_POS = (1200, 910)
AUTO_BUTTON_SIZE = (150, 60)
BET_UP_BUTTON_POS = (800, 910)
BET_DOWN_BUTTON_POS = (900, 910)
BET_BUTTON_SIZE = (80, 80)
VIRTUAL_REEL_HEIGHT = 1200
