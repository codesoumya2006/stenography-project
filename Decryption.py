from PIL import Image

def binary_to_text(binary_string):
    chars = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def xor_decrypt(text, password):
    return ''.join(chr(ord(t) ^ ord(password[i % len(password)])) for i, t in enumerate(text))

def extract_text(image_path, password):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    binary_message = ""
    for pixel in pixels:
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
    
    end_marker = "1111111111111110"
    binary_message = binary_message.split(end_marker)[0]
    
    encrypted_message = binary_to_text(binary_message)
    secret_message = xor_decrypt(encrypted_message, password)
    
    print(f"Hidden Message: {secret_message}")

# User Input
image_path = input("Enter the path of the stego image: ")
password = input("Enter the password: ")

extract_text(image_path, password)