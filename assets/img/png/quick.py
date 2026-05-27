import os

i = 16
for file in sorted(os.listdir('.')):
  if file.endswith(".jpg"):
        os.rename(file, f"Clicked - {i}.jpg")
        i += 1


