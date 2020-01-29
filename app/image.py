from PIL import Image as pilImage
from datetime import datetime
from werkzeug.utils import secure_filename
from app import app
import os

#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class image():

    def __init__(self,imagedata):
        #self.image = imagedata
        self.imageValidation(imagedata)




    def imageValidation(self,imagedata):
        if imagedata and self.allowed_file(imagedata.filename):
            filename = secure_filename(str(datetime.now()) + imagedata.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            self.imageResize(path,imagedata)

        else:
            filename = secure_filename("image-placeholder.png")
        self.filename = filename

    def imageResize(self,path,imagedata):
        img = pilImage.open(imagedata)
        img_width, img_height = img.size
        crop = min(img.size)
        square_img = img.crop(((img_width - crop) // 2,
                         (img_height - crop) // 2,
                         (img_width + crop) // 2,
                         (img_height + crop) // 2))
        self.imageSave(square_img,path)

    
    def imageSave(self,square_img,path):
        square_img.save(path)


    def allowed_file(self,filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']