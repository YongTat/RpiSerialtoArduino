import multiprocessing
import time

def printonly():
    while True:
        print("Test")
        time.sleep(1)

def printuserin():
    userin = input("Enter: ")
    print(userin)

def main():
    while True:
        p1 = multiprocessing.Process(target=printonly)
        p1.start()
        printuserin()
        p1.terminate()
if __name__ == "__main__":
    main()