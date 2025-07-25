import cv2
import mediapipe as mp
import time
import serial

# === Serial Setup ===
ser = serial.Serial('COM7', 9600)  # Change COM port as per your system
time.sleep(2)  # Wait for Arduino to initialize

# === Mediapipe Setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)
min_dist = 30

# === State Variables ===
selected_box = None
pinch_active = False
distance = 0

# === Brightness values for each LED ===
brightness_values = [0, 0, 0]  # For LED-1, LED-2, LED-3

# === Define boxes (label, box-xywh, color) ===
boxes = [
    ("LED-1", (50, 50, 150, 150), (0, 0, 255, 80)),     # Red
    ("LED-2", (250, 50, 150, 150), (0, 255, 255, 80)),  # Yellow
    ("LED-3", (450, 50, 150, 150), (255, 0, 0, 80))     # Blue
]

# === Arduino Pin Mapping ===
arduino_pins = [9, 10, 11]  # Corresponding to LED-1, LED-2, LED-3

# === Utility Functions ===
def calculate_distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5

def point_in_box(point, box):
    x, y = point
    bx, by, bw, bh = box
    return bx <= x <= bx + bw and by <= y <= by + bh

def send_brightness_to_arduino():
    for i in range(3):
        command = f"{arduino_pins[i]}:{brightness_values[i]}\n"
        ser.write(command.encode())
        time.sleep(0.02)  # Avoid flooding serial

# === Main Loop ===
while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    overlay = img.copy()
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    index_tip_pos = None
    thumb_tip_pos = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip_pos = (int(index_tip.x * w), int(index_tip.y * h))
            thumb_tip_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            # Draw red circles
            cv2.circle(img, index_tip_pos, 6, (0, 0, 255), -1)
            cv2.circle(img, thumb_tip_pos, 6, (0, 0, 255), -1)

            # Blue line
            cv2.line(img, index_tip_pos, thumb_tip_pos, (255, 0, 0), 2)

            # Calculate pinch distance
            distance = calculate_distance(index_tip_pos, thumb_tip_pos)

            if distance <= min_dist and not pinch_active:
                # Pinch started
                pinch_active = True
                for i, (label, (x, y, w_box, h_box), _) in enumerate(boxes):
                    if point_in_box(index_tip_pos, (x, y, w_box, h_box)):
                        selected_box = i
                        break

            elif distance > min_dist and pinch_active:
                # Pinch released
                pinch_active = False

    # === Update brightness of selected LED ===
    if selected_box is not None:
        max_dist = 150  # Customize as needed
        brightness = int(min(max((distance - min_dist) / (max_dist - min_dist) * 255, 0), 255))
        brightness_values[selected_box] = brightness
        send_brightness_to_arduino()

    # === Draw UI Elements ===
    # Distance at top-left
        cv2.putText(img, f'Distance: {int(brightness)} px', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Boxes with transparency
    for i, (label, (x, y, w_box, h_box), color) in enumerate(boxes):
        r, g, b, alpha = color
        cv2.rectangle(overlay, (x, y), (x + w_box, y + h_box), (r, g, b), -1)
        cv2.putText(img, label, (x + 10, y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Merge overlay
    cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

    # Green outline for selected
    if selected_box is not None:
        label, (x, y, w_box, h_box), _ = boxes[selected_box]
        cv2.rectangle(img, (x, y), (x + w_box, y + h_box), (0, 255, 0), 3)
        cv2.putText(img, f'Selected: {label}', (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show final
    cv2.imshow("Hand Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
ser.close()