from mazeinit import MazeInit, MazeConfigError
import sys
import traceback

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise MazeConfigError("Use as first argument a configuration file")
        data = MazeInit(sys.argv[1])
    except Exception as e:
        print("An error occured :", e)
        if len(sys.argv) > 2 and sys.argv[2] == "traceback":
            traceback.print_exc()
