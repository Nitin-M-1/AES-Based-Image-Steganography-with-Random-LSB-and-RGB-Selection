# AES-Based Image Steganography with Random LSB and RGB Selection

This project demonstrates an advanced steganography technique using AES encryption and random selection of RGB channels and LSB (Least Significant Bits) to hide encrypted messages within images. The method ensures enhanced security and unpredictability, making it ideal for research and educational purposes.

---

## Features

1. **AES Encryption**: Messages are securely encrypted using AES (Advanced Encryption Standard) before embedding.
2. **Random LSB Selection**: Data is hidden in randomly selected LSB layers (1st, 2nd, or 3rd LSB) for added unpredictability.
3. **Random RGB Channel Selection**: Each bit of data is embedded into a randomly selected RGB channel (Red, Green, or Blue).
4. **End Marker for Data**: The end of the hidden data is marked with a unique binary sequence (`1111111111111110`) to ensure accurate extraction.

---

## How It Works

### 1. **Encryption**
- **AES Encryption**: The plaintext message is encrypted using AES in CBC mode. A random 16-byte key is generated for each session, ensuring secure encryption.

### 2. **Data Embedding**
- The encrypted message is converted into binary form.
- A random RGB channel and LSB layer are selected for each bit of the binary data.
- The selected bit in the selected channel is modified to embed the binary data while clamping pixel values within the valid range (0-255).

### 3. **Data Extraction**
- The same random choices (RGB channel and LSB layer) used during embedding are stored and reused during extraction.
- The embedded binary data is reconstructed bit by bit and converted back to encrypted bytes.
- The AES key is used to decrypt the bytes, recovering the original message.

---

## Usage

### Prerequisites

- Python 3.8 or higher
- OpenCV
- PyCryptodome

Install the required libraries:
```bash
pip install opencv-python pycryptodome
```

### Running the Script

1. **Hiding a Message**
   - Run the script and select the `hide` mode.
   - Provide the path to the cover image and the message to hide.
   - The program will:
     1. Encrypt the message.
     2. Embed it into the image using random LSB and RGB selection.
     3. Save the stego-image and the random choices used.
     4. Display the AES key (store this securely for extraction).

2. **Extracting a Message**
   - Run the script and select the `extract` mode.
   - Provide the path to the stego-image and the AES key.
   - The program will:
     1. Extract the binary data using the saved random choices.
     2. Decrypt the extracted data using the provided key.
     3. Display the hidden message.

---

## Code Overview

### Main Functions

- **`encrypt_payload(payload, key)`**: Encrypts the message using AES.
- **`decrypt_payload(encrypted_payload, key)`**: Decrypts the message using AES.
- **`to_binary(data)`**: Converts data to binary form.
- **`embed_data(image, binary_data, num_layers=3)`**: Embeds binary data into the image by randomly selecting RGB channels and LSB layers.
- **`extract_data(image, random_choices, num_layers=3)`**: Extracts binary data from the image using stored random choices.

### Randomization
- **RGB Channel Selection**: Randomly selects one of the three color channels (Red, Green, Blue) for each bit.
- **LSB Layer Selection**: Randomly selects one of the last three bits (1st, 2nd, 3rd LSB) in the pixel.

### End Marker
- An end marker (`1111111111111110`) is added to indicate the end of the embedded data, ensuring accurate extraction.

---

## Security Notes

1. **Random Choices**: The randomization of RGB channels and LSB layers makes it difficult to predict where the data is hidden.
2. **Encryption Key**: Ensure the AES key is securely stored, as it is required to decrypt the message.
3. **Random Choices File**: The `random_choices.txt` file must be protected, as it is needed for data extraction.

---

## Example

### Hiding Data
```bash
python steganography.py
Enter 'hide' to embed data or 'extract' to retrieve data: hide
Enter the path to the image: input_image.png
Enter the message to hide: Secret Message!

Data hidden successfully. Key (store securely): 2b7e151628aed2a6abf7158809cf4f3c
Stego image saved as stego_image.png
```

### Extracting Data
```bash
python steganography.py
Enter 'hide' to embed data or 'extract' to retrieve data: extract
Enter the path to the image: stego_image.png
Enter the 32-character hex key: 2b7e151628aed2a6abf7158809cf4f3c

Hidden Message: Secret Message!
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- PyCryptodome for AES encryption.
- OpenCV for image processing.
- Inspiration from cryptography and steganography research.
