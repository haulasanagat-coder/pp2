import pygame
from clock import MickeyClock

def main():
    mickey_clock = MickeyClock()
    try:
        mickey_clock.run()
    except Exception as e:
        print(f"wrong：{e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()