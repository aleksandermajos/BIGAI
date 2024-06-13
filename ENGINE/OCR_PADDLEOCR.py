from paddleocr import PaddleOCR,draw_ocr

ocr = PaddleOCR(lang='en') # need to run only once to download and load model into memory
img_path = ''
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)


# draw result
from PIL import Image
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
'''
for t in txts:
    print(t)
    output_path = 'oko.wav'
    model_melo.tts_to_file(t, speaker_ids['JP'], output_path, speed=speed)
    playsound('oko.wav')
'''
file_path = ''
with open(file_path, 'w') as file:
    # Iterate over each string in the list
    for line in txts:
        # Write the string to the file followed by a newline character
        file.write(line + '\n')


'''
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='ppocr_img/fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
'''