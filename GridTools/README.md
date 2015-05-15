# GridTools

To download file
Scripts to search for and download production and raw datasets from grid storage.

Should be used in two phases:

 * Run ./production_list or ./raw_list to create list of files to grab
 * Run ./grabber to download files from the lists

Script (uploader) to upload data to the GRID
Requires a text file say what type of data it is or base directory
(user,sw,snotflow,production_testing,production,nearline)
then the file path on the GRID and then the file path on your local
macheine including the file. The file on the GRID will have the same
name as the one on the local macheine. They should be seperated by 
a ,. The default text filename is in_text.txt

example of text file
<base_directory>,<GRID_file_path>,<loacal_file_path>


./uploader

Script (deleter) to delete files from the GRID
It requires a text file in the same formate as the uploader. 
The default name is delete_files.txt.
