import os

# <option value="/Visualization/files/L9xx12xx-TL2068.1b.pdf">L9xx12xx-TL2068.1b</option>

inputDirectoryPath = "./visualization/documents/scans/"

# for every file in the directory which ends with .txt
for file in os.listdir(inputDirectoryPath):
    filename = os.fsdecode(file)
    if filename.endswith(".pdf"):
        # print(inputDirectoryPath.replace(".", "") + filename)

        print('<option value="' + filename + '">' + filename.replace(".pdf", "") + "</option>")
