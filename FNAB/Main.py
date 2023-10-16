import pygame
import sys
import cv2
import numpy as np
import mss
import win32api, win32con, win32gui
import time

Clock = pygame.time.Clock() 
FPS = 30 

# Initialize pygame
pygame.init()

# Set up the display
screen_width, screen_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FNAB")

# Colors
bg_color = (47, 53, 66)   # Background color
button_color = (249, 38, 114)  # Button color
button_text_color = (255, 255, 255)  # Button text color
slider_color = (102, 217, 239)  # Slider color
slider_handle_color = (251, 73, 52)  # Slider handle color

# Font
font = pygame.font.Font(None, 36)

# Toggle variables
AB = False
Recoil = False

# Slider parameters
slider_min = 0
slider_max = 1
slider_value = slider_min
slider_dragging = False

# Button and slider rectangles
button_AB_rect = pygame.Rect(100, 100, 200, 50)
button_Recoil_rect = pygame.Rect(100, 200, 200, 50)
slider_rect = pygame.Rect(50, 300, 300, 10)
slider_handle_radius = 15

# Settings button and info page
settings_icon = pygame.image.load(r'settings_icon.png')  # Replace with your icon image file
settings_icon_size = (40, 40)  # New size for the settings icon
settings_button_rect = pygame.Rect(350, 10, *settings_icon_size)
show_info_page = False

#Icon
pygame_icon = pygame.image.load(r'OIG.LLWb.ico')
pygame.display.set_icon(pygame_icon)

# Info page
info_page_rect = pygame.Rect(50, 50, 300, 300)
info_text = [
    "V1.0",
    "Discord: Fv79nAg9e4",
]

# Resize the settings icon to the specified size
settings_icon = pygame.transform.scale(settings_icon, settings_icon_size)

# Info page text parameters
info_text_width = 280  # Width of the text box
info_text_padding = 10  # Padding around the text
info_text_line_height = 30  # Height of each line of text

# Function to wrap text
def wrap_text(text, font, max_width):
    words = text.split()
    wrapped_lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)
    return wrapped_lines

# Window Selector button parameters
window_selector_button_rect = pygame.Rect(100, 300, 200, 50)
window_selector_button_color = (52, 152, 219)
window_selector_button_text = "Window Selector"
window_selector_info_text = "Click on the Window Selector button, then click on the Fortnite tab and wait 5 seconds. If done correctly it should say 'Fortnite'"


#################### AB STUFF ####################
print("Loading AB")
# Load the pre-trained Haar Cascade Classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Define the center portion of the screen to capture
screen_width = 1920  # Adjust to your screen's width
screen_height = 1080  # Adjust to your screen's height
portion_width = 400   # Adjust to the desired portion width
portion_height = 400  # Adjust to the desired portion height

# Calculate the coordinates for the top-left corner of the portion
top_left_x = (screen_width - portion_width) // 2
top_left_y = (screen_height - portion_height) // 2

# Define the cursor movement delay (in seconds)
cursor_movement_delay = 0.005



#################### BLOOM STUFF ####################
movement_distance = 20
FN_Tab = None


# Main loop
with mss.mss() as sct:
    # Define the portion to capture
    monitor = {"top": top_left_y, "left": top_left_x, "width": portion_width, "height": portion_height}
    running = True
    while running:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_AB_rect.collidepoint(event.pos) and not show_info_page:
                        AB = not AB
                    elif button_Recoil_rect.collidepoint(event.pos) and not show_info_page:
                        Recoil = not Recoil
                    elif slider_handle_rect.collidepoint(event.pos) and not show_info_page:
                        slider_dragging = True
                    elif settings_button_rect.collidepoint(event.pos):
                        show_info_page = not show_info_page
                    elif window_selector_button_rect.collidepoint(event.pos) and show_info_page:
                        #print("Window Selector button clicked.")
                        time.sleep(5)
                        focused_window_handle = win32gui.GetForegroundWindow()
                        FN_Tab = win32gui.GetForegroundWindow()
                        window_selector_button_text = win32gui.GetWindowText(focused_window_handle)
                        
                        
                        

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    slider_dragging = False

        focused_window_handle = win32gui.GetForegroundWindow()
        movement_distance2 = round(movement_distance * slider_value)
        #print(AB, " ", Recoil, " ", movement_distance2)
        if AB:
            if focused_window_handle == FN_Tab:
                # Capture the portion of the screen
                screenshot = np.array(sct.grab(monitor))

                # Convert the screenshot to grayscale for detection
                gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                # Detect faces and bodies using the Haar Cascade Classifiers
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 100))

                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        face_center_x = x + w // 2
                        face_center_y = y + h // 2
                        cursor_dx = face_center_x - portion_width // 2
                        cursor_dy = face_center_y - portion_height // 2
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, cursor_dx, cursor_dy, 0, 0)
                        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
                elif len(bodies) > 0:
                    for (x, y, w, h) in bodies:
                        body_center_x = x + w // 2
                        body_center_y = y + h // 2
                        cursor_dx = body_center_x - portion_width // 2
                        cursor_dy = body_center_y - portion_height // 2
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, cursor_dx, cursor_dy, 0, 0)
                        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    
                    # Pause for cursor movement delay
                    time.sleep(cursor_movement_delay)

                # Display the result
                #cv2.imshow('Detection', screenshot)


        if Recoil:
            #movement_distance = round(movement_distance * slider_value)
            if win32api.GetKeyState(0x01)<0 and focused_window_handle == FN_Tab:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, movement_distance2, 0, 0)

                time.sleep(0.05)



        screen.fill(bg_color)

        # Draw the AB button
        pygame.draw.rect(screen, button_color if AB else bg_color, button_AB_rect)
        pygame.draw.rect(screen, button_color, button_AB_rect, 2)
        button_AB_text = font.render(f"AB = {AB}", True, button_text_color)
        text_AB_rect = button_AB_text.get_rect(center=button_AB_rect.center)
        screen.blit(button_AB_text, text_AB_rect)

        # Draw the Recoil button
        pygame.draw.rect(screen, button_color if Recoil else bg_color, button_Recoil_rect)
        pygame.draw.rect(screen, button_color, button_Recoil_rect, 2)
        button_Recoil_text = font.render(f"Recoil = {Recoil}", True, button_text_color)
        text_Recoil_rect = button_Recoil_text.get_rect(center=button_Recoil_rect.center)
        screen.blit(button_Recoil_text, text_Recoil_rect)

        # Draw the slider
        pygame.draw.rect(screen, slider_color, slider_rect, border_radius=slider_rect.height // 2)
        if not show_info_page:
            if slider_dragging:
                slider_value = max(slider_min, min(slider_max, (pygame.mouse.get_pos()[0] - slider_rect.left) / slider_rect.width))
            slider_handle_x = int(slider_rect.left + slider_value * slider_rect.width)
            slider_handle_rect = pygame.Rect(slider_handle_x - slider_handle_radius, slider_rect.centery - slider_handle_radius, slider_handle_radius * 2, slider_handle_radius * 2)
            pygame.draw.circle(screen, slider_handle_color, slider_handle_rect.center, slider_handle_radius)

            slider_value_text = font.render(f"Strength = {slider_value:.2f}", True, button_text_color)
            slider_value_text_rect = slider_value_text.get_rect(center=(200, slider_rect.top - 30))
            screen.blit(slider_value_text, slider_value_text_rect)

        # Draw the settings button
        screen.blit(settings_icon, settings_button_rect.topleft)

        # Draw the info page if visible
        if show_info_page:
            pygame.draw.rect(screen, button_color, info_page_rect)

            # Wrap and render info text
            wrapped_info_text = wrap_text("\n".join(info_text), font, info_text_width)
            current_y = info_page_rect.top + info_text_padding
            for line in wrapped_info_text:
                info_line = font.render(line, True, button_text_color)
                info_line_rect = info_line.get_rect(topleft=(info_page_rect.left + info_text_padding, current_y))
                screen.blit(info_line, info_line_rect)
                current_y += info_text_line_height

            # Wrap and render info text for button
            wrapped_info_text = wrap_text(window_selector_info_text, font, info_text_width)
            current_y = info_page_rect.top + info_text_padding
            for line in wrapped_info_text:
                info_line = font.render(line, True, button_text_color)
                info_line_rect = info_line.get_rect(topleft=(info_page_rect.left + info_text_padding, current_y + 70))
                screen.blit(info_line, info_line_rect)
                current_y += info_text_line_height

            # Draw the Window Selector button and info if visible
            pygame.draw.rect(screen, window_selector_button_color, window_selector_button_rect)
            pygame.draw.rect(screen, button_color, window_selector_button_rect, 2)
            window_selector_button_text_rendered = font.render(window_selector_button_text, True, button_text_color)
            window_selector_button_text_rect = window_selector_button_text_rendered.get_rect(center=window_selector_button_rect.center)
            screen.blit(window_selector_button_text_rendered, window_selector_button_text_rect)
        
        pygame.display.flip()

# Quit pygame
pygame.quit()
cv2.destroyAllWindows()
sys.exit()
