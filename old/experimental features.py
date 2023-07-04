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

#from old.threadsafecounter import ThreadSafeCounter
#counter = Counter() if you want a thread safe counter, currently no need
#
# print(f"\t\t---------------------------\n"
#       f"\t\tFile with name: {file_name}\n"
#       f"\t\t---------------------------\n"
#       f"{prepped_text}\n\n\n")


# def og_file_len(self):  # TODO: Fix so it works with video as well (cv2)
#
#
#     # def with_opencv(filename):
#     #     import cv2
#     #     video = cv2.VideoCapture(filename)
#     #
#     #     duration = video.get(cv2.CAP_PROP_POS_MSEC)
#     #     frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
#     #
#     #     return duration, frame_count
# print(f"Thread: {thread} Thread != threading.current_thread(): {thread != threading.current_thread()} Thread.daemon: {thread.daemon} Not thread.daemon: {not thread.daemon}")
