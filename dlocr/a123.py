import time
import dlocr

if __name__ == '__main__':
    ocr = dlocr.get_or_create()
    start = time.time()

    bboxes, texts = ocr.detect(r"C://Users//Hasee//Desktop//535.png")
    print('\n'.join(texts))
    print("cost: {:0.2f}s".format((time.time() - start)))