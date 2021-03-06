import pickle

BSIZE = 16
BWIDTH = 37

B_L	 = ((0, 0), (1, 0), (2, 0), (2, 1), 2, 3, (255, 255, 0))
B_RL = ((0, 1), (1, 1), (2, 1), (2, 0), 2, 3, (255, 205, 0))
B_S  = ((0, 0), (1, 0), (1, 1), (2, 1), 2, 3, (255, 155, 0))
B_RS = ((0, 1), (1, 1), (1, 0), (2, 0), 2, 3, (255, 105, 0))
B_ST = ((0, 0), (1, 0), (2, 0), (3, 0), 1, 4, (255, 55, 0))
B_SQ = ((0, 0), (1, 1), (1, 0), (0, 1), 2, 2, (255, 5, 0))
B_LIST = [B_L, B_RL, B_S, B_RS, B_ST, B_SQ]

FPS = 60

NORTH = (-1, 0, "up.png")
SOUTH = (1, 0, "down.png")
WEST  = (0, -1, "left.png")
EAST  = (0, 1, "right.png")
D_LIST = [NORTH, EAST, SOUTH, WEST]

EASY = 0
NORMAL = 1
HARD = 2
EXTREME = 3

MODETEXT = ["EASY", "NORMAL", "HARD", "INSANE"]

settings = {"volume": 1, "control": 0, "highscore": [10, 10, 10, 10]}

def load_settings():
	f = file("config.cfg", "r")
	return pickle.load(f)

def save_settings():
	f = file("config.cfg", "w")
	pickle.dump(settings, f)

settings = load_settings()

def low_vol():
	settings["volume"] = .25

def med_vol():
	settings["volume"] = .50

def high_vol():
	settings["volume"] = 1

def relative_control():
	settings["control"] = 0

def absolute_control():
	settings["control"] = 1
