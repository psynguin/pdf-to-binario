import numpy as np
from PIL import Image
from pdf2image import convert_from_path


def create_block_map(pdf_path, output_path, block_size=5, threshold=0.1):
    images = convert_from_path(pdf_path, dpi=300)
#    print(images)
#    print(enumerate(images))
    for i, img in enumerate(images):
        gray = np.array(img.convert('L'))
        h, w = gray.shape
        gray_img = Image.fromarray(gray)
        gray_img.show()
        # Calculate number of blocks
        h_blocks = h // block_size
        w_blocks = w // block_size

        # Create empty map
        block_map = np.zeros((h_blocks, w_blocks))

        # Process each block
        for y in range(h_blocks):
            for x in range(w_blocks):
                block = gray[y * block_size:(y + 1) * block_size,
                        x * block_size:(x + 1) * block_size]
                black_ratio = np.mean(block <= 30)  # 30 = black threshold
                block_map[y, x] = 1 if black_ratio >= threshold else 0

        # Save and visualize
        np.savetxt(f"{output_path}_page_{i + 1}.txt", block_map, fmt='%d')
        visual = Image.fromarray((block_map * 255).astype(np.uint8))
        visual = visual.resize((w, h), Image.NEAREST)
        visual.save(f"{output_path}_page_{i + 1}_visual.png")


# Example usage
create_block_map("pdf2.pdf", "output_map2", block_size= 2, threshold= 0.1)