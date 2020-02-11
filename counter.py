import numpy as np
import cv2


def run_main():
    # load image
    img = cv2.imread('./coins/web-cam.jpg')
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # smoothens image to reduce amount of false circles detected
    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
    # the houghcircles function takes a grayscale image as input
    circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT,
                               1, 160, param1=50, param2=30, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))

    largestRadius = 0
    change = 0

    for i in circles[0, :]:
        if largestRadius < i[2]:
            largestRadius = i[2]

    for i in circles[0, :]:
        # draw the outer circle-green
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle-red
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

        radius = i[2]
        ratio = ((radius*radius) / (largestRadius*largestRadius))
        print(ratio)

        if(ratio > 0.89):
            change = change + 20
        elif((ratio >= 0.65) and (ratio <= 0.89)):
            change = change + 1
        elif(ratio <= 0.60):
            change = change + 5

    print(change)

    # displays the window
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Total value: " + str("%.2f" % round(change, 2)) + " shillings"
    cv2.putText(img, text, (0, 400), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('Detected coins', img)
    cv2.waitKey()


if __name__ == "__main__":
    run_main()
