# Steganography_Tool
Designed to allow users to seamlessly conceal text or files within images. Leveraging manipulation of the least significant bits of each pixel's RGB value, this tool ensures a covert and secure method for information embedding.

## How to run:
**Install dependencies:**

* pip install -r requirements.txt

**Run:**

* python stego.py encode \<file to hide\> -t \<image to store hidden file\>

* python stego.py decode \<image with hidden file within\> -k \<key\>

* stego.py encode --help

* stego.py decode --help

## How It's Made:

**Tech used:** Python, Cryptography, Pillow

The Steganography Tool is written entirely in Python, a language chosen for its flexibility and extensive support for data manipulation. The tool employs an algorithm that operates on the least significant bits of each pixel's RGB value, facilitating the seamless embedding of text or files within images. Arguments can be provided that allow users to fine-tune the steganographic process by specifying the number of bits used in each RGB color value, tailoring the tool to diverse concealment requirements. The tool incorporates a distribution mechanism to strategically disperse altered bits across the image, improving its ability to evade detection.

## Lessons Learned:

The development of this tool brought forth invaluable insights into the intricate interplay of data security, algorithm design, and user experience. Crafting a user-friendly tool necessitated a delicate balance between customization and simplicity, emphasizing the importance of user control without overwhelming complexity. Additionally, the project underscored the significance of strategic thinking in data concealment, with the distribution mechanism proving crucial in achieving effective covert operations.

Surprisingly, the development of this tool revealed the remarkable resilience of images to concealment, as a significant number of altered bits in the RGB values went unnoticed, showcasing the subtle yet potent nature of steganography in preserving the integrity of cover images. This unexpected capacity to manipulate numerous bits while maintaining imperceptibility highlighted the intricate balance between effective data hiding and visual fidelity.

**White image containing encrypted text**

![image](https://github.com/wizard-adamkay/Steganography_Tool/assets/37917852/b60b0919-c3a3-474d-aa87-fa3226180ee6)

## Limitations:

•	PNG images are the only accepted images to act as cover.
