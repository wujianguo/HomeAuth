#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://blog.csdn.net/rcfalcon/article/details/7718436
#http://blog.csdn.net/lanphaday/article/details/2325027
try:
    import cv2.cv as cv
except:
    cv = None
    try:
        import Image
    except:
        Image = None
class HandlePics():
    def __init__(self):
        pass
    def runCmd(self,cmd):
        pass
    def similarity(self,pic1,pic2):
        if cv:
            return self.imgcompare(pic1,pic2)
        if Image:           
            return self.calc_similar_by_path(pic1,pic2)
        return -1
    def make_regalur_image(self,img, size = (256, 256)):
        return img.resize(size).convert('RGB')
    def split_image(self,img, part_size = (64, 64)):
        w, h = img.size
        pw, ph = part_size
        assert w % pw == h % ph == 0
        return [img.crop((i, j, i+pw, j+ph)).copy() \
                    for i in xrange(0, w, pw) \
                    for j in xrange(0, h, ph)]
    def hist_similar(self,lh, rh):
        assert len(lh) == len(rh)
        return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)
    def calc_similar(self,li, ri):
#	return hist_similar(li.histogram(), ri.histogram())
        return sum(self.hist_similar(l.histogram(), r.histogram()) for l, r in zip(self.split_image(li), self.split_image(ri))) / 16.0
    def calc_similar_by_path(self,lf, rf):
        li, ri = self.make_regalur_image(Image.open(lf)), self.make_regalur_image(Image.open(rf))
        return self.calc_similar(li, ri)

    def createHist(self,img):  
    #cv.CvtColor(img,img,cv.CV_BGR2HSV)  
        b_plane = cv.CreateImage((img.width,img.height), 8, 1)  
        g_plane = cv.CreateImage((img.width,img.height), 8, 1)  
        r_plane = cv.CreateImage((img.width,img.height), 8, 1)  
        cv.Split(img,b_plane,g_plane,r_plane,None)  
        planes = [b_plane, g_plane, r_plane]  
      
        bins = 4  
        b_bins = bins  
        g_bins = bins  
        r_bins = bins  
  
        hist_size = [b_bins,g_bins,r_bins]  
        b_range = [0,255]  
        g_range = [0,255]  
        r_range = [0,255]  
  
        ranges = [b_range,g_range,r_range]  
        hist = cv.CreateHist(hist_size, cv.CV_HIST_ARRAY, ranges, 1)  
        cv.CalcHist([cv.GetImage(i) for i in planes], hist)  
        cv.NormalizeHist(hist,1)  
        return hist  
  
    def imgcompare(self,image1,image2):  
        img1 = cv.LoadImage(image1)  
        hist1 = self.createHist(img1)  
        img2 = cv.LoadImage(image2)  
        hist2 = self.createHist(img2)  
        return cv.CompareHist(hist1,hist2,cv.CV_COMP_CORREL) 
        
    def detect_object(self,infile):
        if not cv:
            return []
        image = cv.LoadImage(infile);
        if image:
            faces = detect_object(image)
        grayscale = cv.CreateImage((image.width, image.height), 8, 1)
        cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

        cascade = cv.Load(os.path.join(ROOT_DIR,"haarcascade_frontalface_alt_tree.xml"))
        rect = cv.HaarDetectObjects(grayscale, cascade, cv.CreateMemStorage(), 1.1, 3,
            cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))

        result = []
        for r in rect:
            result.append((r[0][0], r[0][1], r[0][0]+r[0][2], r[0][1]+r[0][3]))

        return result
