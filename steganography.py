import cv2
import numpy as np
import os
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_payload(payload, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(payload.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_payload(encrypted_payload, key):
    iv = encrypted_payload[:AES.block_size]
    ciphertext = encrypted_payload[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

def to_binary(data):
    return ''.join([format(byte, '08b') for byte in data])

def embed_data(image, binary_data, num_layers=3):
    data_index = 0
    binary_data += '1111111111111110'  
    random_choices = []  

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            channel = random.randint(0, 2)
            bit_layer = random.randint(0, 2)

            random_choices.append((channel, bit_layer))  

            if data_index < len(binary_data):
                pixel = int(image[i, j, channel])  
                pixel = (pixel & ~(1 << bit_layer)) | (int(binary_data[data_index]) << bit_layer)
                pixel = max(0, min(255, pixel)) 
                image[i, j, channel] = pixel
                data_index += 1
            else:
                return image, random_choices  

    return image, random_choices

def extract_data(image, random_choices, num_layers=3):
    binary_data = ''
    data_index = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if data_index < len(random_choices):
                channel, bit_layer = random_choices[data_index]  
                bit = (image[i, j, channel] >> bit_layer) & 1
                binary_data += str(bit)
                data_index += 1
            else:
                break

    stop_index = binary_data.find('1111111111111110') 
    return binary_data[:stop_index]

def main():
    mode = input("Enter 'hide' to embed data or 'extract' to retrieve data: ").strip().lower()
    image_path = input("Enter the path to the image: ").strip()
    image = cv2.imread(image_path)

    if image is None:
        print("Image not found!")
        return

    if mode == 'hide':
        key = os.urandom(16)  
        message = input("Enter the message to hide: ")
        encrypted_message = encrypt_payload(message, key)
        binary_data = to_binary(encrypted_message)
        stego_image, random_choices = embed_data(image.copy(), binary_data, num_layers=3)

        output_path = "stego_image.png"
        cv2.imwrite(output_path, stego_image)

        np.savetxt("random_choices.txt", random_choices, fmt='%d')

        print(f"Data hidden successfully. Key (store securely): {key.hex()}")
        print(f"Stego image saved as {output_path}")

    elif mode == 'extract':
        key_hex = input("Enter the 32-character hex key: ").strip()
        key = bytes.fromhex(key_hex)

        if not os.path.exists("random_choices.txt"):
            print("Error: Random choices file not found!")
            return

        random_choices = np.loadtxt("random_choices.txt", dtype=int).reshape(-1, 2)

        extracted_binary_data = extract_data(image, random_choices, num_layers=3)
        encrypted_bytes = int(extracted_binary_data, 2).to_bytes((len(extracted_binary_data) + 7) // 8, byteorder='big')

        try:
            decrypted_message = decrypt_payload(encrypted_bytes, key)
            print("Hidden Message:", decrypted_message)
        except ValueError:
            print("Decryption failed: Incorrect key or corrupted data.")
    else:
        print("Invalid mode selected. Please choose 'hide' or 'extract'.")

if __name__ == "__main__":
    main()
