import cv2
import os



def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


def main():
    load_images_from_folder(os.path.join('data', 'sample_drive'))


if __name__ == "__main__":
    main()