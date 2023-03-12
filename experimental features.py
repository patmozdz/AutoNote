# import deskew

#TODO: update cudNN to 8.8 (currently 8700, as seen through print(torch.backends.cudnn.version()) virtual environment not inheriting PATH variables?
#TODO: Upgrade to Python 3.11.1 when Whisper becomes available on it
#
# in run_pytess(file_name):
# Experimental:
# img = img.rotate(deskew.determine_skew(img)) #This deskews the image. Can you pass a PIL.Image object into here?
# img = ImageEnhance.Contrast(img).enhance(1.5) #Enhance image contast
# img = img.convert('L') #Convert to grayscale

# import torch
#
# Check if CUDA is available and working:
# test_data = str(torch.cuda.is_available()) + " " + str(torch.version.cuda) + " " + str(torch.cuda.current_device()) + " " + str(torch.backends.cudnn.version()) #CUDA available
