CS 140 MP2

Requirements to run
Python 2	<a href = "www.python.org">www.python.org</a>
Pygame		<a href = "www.pygame.org">www.pygame.org</a>

---

Instructions:
	To run the game, simply run main.py.

Controls:
	Z, X       = Rotate tetrimo
	Left Shift = Hold current tetrimo
	Space Bar  = Drop tetrimo
	P, Escape  = Pause

	For absolute control(Can be changed in the ingame options):
		Up          : Rotate tetrimo
		Down        : Speed up drop rate
		Left, Right : Control the tetrimo to the left or right

	For relative control:
		Same as absolute but direction is relative to where the tetrimo is dropping
		(i.e. If the tetrimo is going left, the right arrow key will rotate the tetrimo
			and left arrow key speeds up the drop rate of the tetrimo)

Modes:
	Easy:
		Tetrimos only goes up or down
	Normal:
		Tetrimos goes on all sides with 10% chance of random events every 10 seconds
	Hard:
		Tetrimos goes on all sides with 25% chance of random events every 10 seconds
	Insane:
		Double speed, tetrimos goies on all sides with 45% chance of random events every 10 seconds

Notes:

Threads are implemented on the Random events and the Timer since updates on this game objects happen on a specific time interval. The thread could
be paused then resumed for updates after a certain time.

Executables can be build by executing:
	python setup.py build
*this requires cx_freeze http://cx-freeze.sourceforge.net/
