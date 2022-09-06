#!/usr/bin/env python3

# 必要なライブラリをインポート
import cv2
import boto3

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

rekognition_client = boto3.client(service_name="rekognition")

print("[s]キーを押すと認識スタート")
while True:
    # 画像を取得
    success, image = cap.read()
    cv2.imshow("Camera", image)
    key = cv2.waitKey(1)
    if key == ord("s"):
        # カメラ画像を保存する
        image_filename = "camera.png"
        cv2.imwrite(image_filename, image)

        # ----------------------------
        # Rekognition
        # ----------------------------
        with open(image_filename, "rb") as f:
            # 画像を読み込む
            image = f.read()
            # レコグニションの処理を開始
            response_data = rekognition_client.detect_faces(
                Image={'Bytes': image}, Attributes=["ALL"]
            )["FaceDetails"]

            # 一個以上、認識できていたら顔が検出できたことにする
            if len(response_data) > 0:
                print("顔が検出できました！")
            else:
                print("顔が検出できませんでした。")
