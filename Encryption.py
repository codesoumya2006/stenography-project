from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def xor_encrypt(text, password):
    return ''.join(chr(ord(t) ^ ord(password[i % len(password)])) for i, t in enumerate(text))

def hide_text(image_path, output_path, secret_message, password):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    encrypted_message = xor_encrypt(secret_message, password)
    binary_message = text_to_binary(encrypted_message) + '1111111111111110'  # End marker
    pixels = list(img.getdata())
    
    new_pixels = []
    binary_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if binary_index < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_index])
            binary_index += 1
        
        new_pixels.append((r, g, b))
    
    img.putdata(new_pixels)
    img.save(output_path)
    print(f"Message hidden successfully in {output_path}")

# User Input
image_path = input("Enter the path of the image: ")
output_path = input("Enter the output image path: ")
secret_message = input("Enter the message to hide: ")
password = input("Enter the password: ")

hide_text(image_path, output_path, secret_message, password)