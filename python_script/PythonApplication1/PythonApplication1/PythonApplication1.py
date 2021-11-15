# import the necessary packages
from imutils import face_utils
import dlib
import cv2
import time

# import C++ functions with the wrapping
from getpoints import c_get_point
from getpoints import c_get_point2

if __name__ == "__main__":
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    p = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(p)

    cap = cv2.VideoCapture(0)
    cap.set(5, 50)
    cap.set(3, 800)
    cap.set(4, 450)

    flag = 0

    while True:
        # time.sleep(0.1)
        # load the input image and convert it to grayscale
        _, image = cap.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale image
        rects = detector(gray, 0)

        # loop over the face detections
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)

            shape = face_utils.shape_to_np(shape)

            # print only the first 2 sets of 68 points
            # using C++ functions from the wrapping
            flag += 1
            if not flag % 80:
                flag = 0
                print("### AFFICHAGE DES 68 POINTS EN UTILISANT LES FONCTIONS DU WRAPPING ###")
                for k in range(len(shape)):
                    print('Point ' + str(k+1) + ' : ', end ='')
                    # use of wrapping functions imported from C++
                    print(int(c_get_point(shape[k][0])), int(c_get_point2(shape[k][1])/10));

            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw them on the image
            for (x, y) in shape:
                cv2.circle(image, (x, y), 2, (0, 255, 255), -1)

        # show the output image with the face detections + facial landmarks
        cv2.imshow("Output", image)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
