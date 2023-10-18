# Code snippet is using the ConvertAPI Python Client: https://github.com/ConvertAPI/convertapi-python
import convertapi
 
convertapi.api_secret = 'GNduWrTfINgsUyO4'

result = convertapi.convert('txt', { 'File': 'data\\amzn.pdf' })

# save to file
result.file.save('data\output.txt')



"""import PyPDF2

# Replace 'input.pdf' with the path to your PDF file
pdf_file_path = 'data\\amzn.pdf'

# Replace 'output.txt' with the path for the output text file
text_file_path = 'data\\output.txt'

def pdf_to_text(pdf_path, text_path):
    try:
        # Open the PDF file
        pdf_file = open(pdf_path, 'rb')

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Create a text file to write the extracted text
        text_file = open(text_path, 'w')

        # Loop through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            text_file.write(text)

        # Close the files
        pdf_file.close()
        text_file.close()

        print(f"Text extracted and saved to {text_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Convert the PDF to text
pdf_to_text(pdf_file_path, text_file_path)"""