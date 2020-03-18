from PIL import Image as pilImage
from datetime import datetime
from werkzeug.utils import secure_filename
from app import app
import os
import requests
from io import BytesIO,StringIO
import io

#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class Image():

    def __init__(self,imagedata):
        #self.image = imagedata
        self.imgur_url = ''
        self.imagedata = imagedata

        self.upload_to_imgur_link()
        '''
        #Check to see if user passed a FileFromLocal/Link/None
        if not imagedata.image_source_file or imagedata.image_source_link:
            set_image_default()
        if imagedata.image_source_file:
            upload_to_imgur_file()
        if imagedata.image_source_link:
            upload_to_imgur_link()
        '''    

            
        




    def upload_to_imgur_file(self):
        if self.allowed_file(self.imagedata.filename):
            imageBinary = self.imageResize()
            self.upload(imageBinary)
    
    def upload_to_imgur_link(self):
        imageBinary = self.imageResize()
        self.upload(imageBinary)

    def imageResize(self):
        if type(self.imagedata) == str:
            img_response = requests.get(self.imagedata)
            img = pilImage.open(BytesIO(img_response.content))
            img_width, img_height = img.size
            crop = min(img.size)
            square_img = img.crop(((img_width - crop) // 2,(img_height - crop) // 2,(img_width + crop) // 2,(img_height + crop) // 2))

            imgByteArr = io.BytesIO()
            square_img.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            return imgByteArr
        else:
            img = pilImage.open(self.imagedata)
            img_width, img_height = img.size
            crop = min(img.size)
            square_img = img.crop(((img_width - crop) // 2,(img_height - crop) // 2,(img_width + crop) // 2,(img_height + crop) // 2))
            
            return imageBinary


    def upload(self,imageBinary):
        payload = {'image': imageBinary}
        files = []
        headers = {'Authorization': 'Client-ID fe0cf2054c6fbed'}
        response = requests.request("POST", app.config['IMGUR_UPLOAD_ULR'], headers=headers, data = payload, files = files)
        imgur_upload_success = response.json()
        self.imgur_url = imgur_upload_success["data"]["link"]


    def allowed_file(self,filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def download_from_link(self,link):
        pass