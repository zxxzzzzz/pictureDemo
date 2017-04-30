import math
class OneBMPPicture:
    __width=0   ##图长(pix)
    __height=0  ##图高(pix)
    __byteArray=[] ##图所有数据
    __bitCount=0  ##位深（1，4，8，24）
    __bfSize=0   ##文件大小（位）
    __imageSize=0 ##图像数据大小（位）
    __lineBitSize=0  ##一行像素数据大小（位）
    __cover=0
   # __imageData=[]  ##图像数据
   # __header=[]    ##文件头
    #__tagRGBQuad=[] ##调色盘
    def __init__(self,pathOrData=0):
        if  isinstance(pathOrData,str):
            with open(pathOrData,'rb') as f:
                self.__byteArray=bytearray(f.read())
                f.close()
                self.__initAttr()
        else:
            self.__byteArray=pathOrData
            self.__initAttr()
    def __initAttr(self):
        self.__width=self.__byteArray[18]+self.__byteArray[19]*256+self.__byteArray[20]*65536
        self.__height=self.__byteArray[22]+self.__byteArray[23]*256+self.__byteArray[24]*65536
        self.__bitCount=self.__byteArray[28]
        self.__bfSize=self.__byteArray[2]+self.__byteArray[3]*256+self.__byteArray[4]*65536+self.__byteArray[4]*16777216
        self.__imageSize=self.__byteArray[34]+self.__byteArray[35]*256+self.__byteArray[36]*65536+self.__byteArray[37]*16777216
        self.__lineBitSize=self.__imageSize/self.__height
        self.__cover=self.__lineBitSize-(self.__bitCount/8*self.__width)
    def __getbfSize(self,bitCount,width,height):
        if bitCount==24:
            if 4-(width*3)%4!=0:
                widthSize=(4-(width*3)%4)+width*3 #计算添加填充字符后字节大小
                return widthSize*height+54 ##不包含颜色表
            else:
                widthSize=width*3 #计算添加填充字符后字节大小
                return widthSize*height+54 ##不包含颜色表
        else:
            if width%4!=0:
                widthSize=width+4-(width%4)
            else:
                widthSize=width#计算添加填充字符后字节大小
        return widthSize*height+54+math.pow(2,bitCount)*4  #包含颜色表
    def getbfSize(self):
        return self.__bfSize
    def __getImageSize(self,bitCount,width,height):
        if bitCount==24:
            return self.__getbfSize(bitCount,width,height)-54
        else:
            return self.__getbfSize(bitCount,width,height)-54-math.pow(2,bitCount)*4
    def getWidth(self):
        return self.__width
    def getHeight(self):
        return self.__height
    def pix(self,x,y): ##x,y越界输出width,height
        if self.__bitCount==24:
            if self.__width<x:
                return self.pix(self.__width,y)
            if self.__height<y:
                return self.pix(x,self.__height)
            if x<0:
                return self.pix(0,y)
            if y<0:
                return self.pix(x,0)
            return int(y*self.__lineBitSize+x*3+54)
        else:
            if self.__width<x:
                return self.pix(self.__width,y)
            if self.__height<y:
                return self.pix(x,self.__height)
            if x<0:
                return self.pix(0,y)
            if y<0:
                return self.pix(x,0)
            return int(y*self.__lineBitSize+x+54+4*256)
    def rect(self,x,y,width,height):
        b=[0,0]
        for j in range(y,y+height):
            for i in range(x,x+width):
                b[0]=i
                b[1]=j
                yield b
    def circle(self,x,y,r):
        b=[0,0]
        for j in range(y-r,y+r+1):
            for i in range(x-r,x+r+1):
                b[0]=i
                b[1]=j
                yield b
    def createBMPFile(self,path,data=0):
        with open(path,'wb') as f:
            if data==0:
                f.write(self.__byteArray)
                f.close()
                return
            f.write(data)
            f.close()
    def gaussianBlurFilter(self,x,y,width,height,R,variance): #variance方差
        gaussianBlurWeight=[]
        for i in self.circle(0,0,R):
            gaussianBlurWeight.append(math.exp(-(i[0]*i[0]+i[1]*i[1])/(2*variance*variance))/(2*math.pi*variance*variance))
        total=0
        for i in gaussianBlurWeight:
            total=total+i
        for i in range(len(gaussianBlurWeight)):
            gaussianBlurWeight[i]=gaussianBlurWeight[i]/total   ##生成高斯权值
        for i in self.rect(x,y,width,height):
            r=0
            g=0
            b=0
            cout=0
            for j in self.circle(i[0],i[1],R):
                r=r+self.__byteArray[self.pix(j[0],j[1])]*gaussianBlurWeight[cout]
                g=g+self.__byteArray[self.pix(j[0],j[1])+1]*gaussianBlurWeight[cout]
                b=b+self.__byteArray[self.pix(j[0],j[1])+2]*gaussianBlurWeight[cout]
                cout=cout+1
            self.__byteArray[self.pix(i[0],i[1])]=int(r)
            self.__byteArray[self.pix(i[0],i[1])+1]=int(g)
            self.__byteArray[self.pix(i[0],i[1])+2]=int(b)

        
    def mosaicFilter(self,x,y,width,height,n): #马赛克化
        for i in self.rect(x,y,width,height):
            if (i[0]-x)%n!=0:
                continue
            if (i[1]-y)%n!=0:
                continue
            r=0
            g=0
            b=0
            for j in self.rect(i[0],i[1],n,n):
                r=r+self.__byteArray[self.pix(j[0],j[1])]
                g=g+self.__byteArray[self.pix(j[0],j[1])+1]
                b=b+self.__byteArray[self.pix(j[0],j[1])+2]
            r=int(r/(n*n))
            b=int(b/(n*n))
            g=int(g/(n*n))
            for j in self.rect(i[0],i[1],n,n):
                self.__byteArray[self.pix(j[0],j[1])]=r
                self.__byteArray[self.pix(j[0],j[1])+1]=g
                self.__byteArray[self.pix(j[0],j[1])+2]=b
   
        for y in range(1,self.__height-n+1,n):
            for x in range(1,self.__width-n+1,n):
                r=0
                g=0
                b=0
                for i in range(n):
                    for j in range(n):
                        r=r+self.__byteArray[self.pix(x+i,y+j)]
                        g=g+self.__byteArray[self.pix(x+i,y+j)+1]
                        b=b+self.__byteArray[self.pix(x+i,y+j)+2]
                r=int(r/(n*n))
                g=int(g/(n*n))
                b=int(b/(n*n))
                for i in range(n):
                    for j in range(n):
                        self.__byteArray[self.pix(x+j,y+i)]=r
                        self.__byteArray[self.pix(x+j,y+i)+1]=g
                        self.__byteArray[self.pix(x+j,y+i)+2]=b
    def averageBlurFilter(self,x,y,width,height,R):
        weight=1/(2*R+1)/(2*R+1)
        for i in self.rect(x,y,width,height):
            r=0
            g=0
            b=0
            cout=0
            for j in self.circle(i[0],i[1],R):
                r=r+self.__byteArray[self.pix(j[0],j[1])]*weight
                g=g+self.__byteArray[self.pix(j[0],j[1])+1]*weight
                b=b+self.__byteArray[self.pix(j[0],j[1])+2]*weight
            self.__byteArray[self.pix(i[0],i[1])]=int(r)
            self.__byteArray[self.pix(i[0],i[1])+1]=int(g)
            self.__byteArray[self.pix(i[0],i[1])+2]=int(b)
    def __LONGconvertToDWORD(self,total):
        b=0
        for i in range(4,0,-1):
            b=int(total/math.pow(256,i-1))
            total=total%math.pow(256,i-1)
            yield b
    
    def __getHeader(self,bitCount,width,height):
        if bitCount==1:
            if width%8!=0:
                width=width+8-(width%8)
        #############tagBitMapFileHeader
        #bftype
        byteArray=[]
        for i in range(54):
            byteArray.append(0)
        byteArray[0]=66
        byteArray[1]=77
        #bfsize 2-5
        cout=5
        for i in self.__LONGconvertToDWORD(self.__getbfSize(bitCount,width,height)):
            byteArray[cout]=i
            cout=cout-1
        #bfReserved
        byteArray[6]=0
        byteArray[7]=0
        byteArray[8]=0
        byteArray[9]=0
        #bfOffBits 10-13
        cout=13
        if bitCount==24:##24位没调色板
            for i in self.__LONGconvertToDWORD(54):
                byteArray[cout]=i
                cout=cout-1
        for i in self.__LONGconvertToDWORD(54+math.pow(2,bitCount)*4):
            byteArray[cout]=i
            cout=cout-1
        ###########tagBitMapInfoHeader
        #biSize 本结构所占用字节数（15-18字节）
        byteArray[14]=40
        byteArray[15]=0
        byteArray[16]=0
        byteArray[17]=0
        #biWidth 18-21
        cout=21
        for i in self.__LONGconvertToDWORD(width):
            byteArray[cout]=i
            cout=cout-1
        #biHeight 22-25
        cout=25
        for i in self.__LONGconvertToDWORD(height):
            byteArray[cout]=i
            cout=cout-1
        #biPlanes
        byteArray[26]=1
        byteArray[27]=0
        #biBitCount
        byteArray[28]=bitCount
        byteArray[29]=0
        #biCompression
        byteArray[30]=0
        byteArray[31]=0
        byteArray[32]=0
        byteArray[33]=0
        #biSizeImage 34-37
        cout=37
        for i in self.__LONGconvertToDWORD(self.__getImageSize(bitCount,width,height)):
            byteArray[cout]=i
            cout=cout-1
        #biXpelsPerMeter
        byteArray[38]=19
        byteArray[39]=11
        byteArray[40]=0
        byteArray[41]=0
        #biXpelsPerMeter
        byteArray[42]=19
        byteArray[43]=11
        byteArray[44]=0
        byteArray[45]=0
        #biClrUsed
        byteArray[46]=0
        byteArray[47]=0
        byteArray[48]=0
        byteArray[49]=0
        #biClrImportant
        byteArray[50]=0
        byteArray[51]=0
        byteArray[52]=0
        byteArray[53]=0
        return byteArray
   
    def __getTagRGBQuad(self,bitCount):
        if bitCount==24:
            return
        tagRGBQuad=[]
        unit=255/(math.pow(2,bitCount)-1)
        for i in range(int(math.pow(2,bitCount))):
            tagRGBQuad.append(int(unit*i))      #b
            tagRGBQuad.append(int(unit*i))      #g
            tagRGBQuad.append(int(unit*i))      #r
            tagRGBQuad.append(0)
        return tagRGBQuad
    def __getBlankImageData(self,bitCount,width,height):
        image=[]
        for i in range(int(self.__getImageSize(bitCount,width,height))):
            image.append(255)
        return image
    def getBlank(self,bitCount,width,height):
        if bitCount==24:
           return bytearray(self.__getHeader(bitCount,width,height)+self.__getBlankImageData(bitCount,width,height))
        return bytearray(self.__getHeader(bitCount,width,height)+self.__getTagRGBQuad(bitCount)+self.__getBlankImageData(bitCount,width,height))
    def drawLine(self,x,y,length):
        for i in self.rect(x,y,1,length):
            self.__byteArray[self.pix(i[0],i[1])]=0
    def drawFillRect(self,x,y,width,height):
        for i in self.rect(x,y,width,height):
            self.__byteArray[self.pix(i[0],i[1])]=0
    def getHistogram(self):#直方图
        t=[]
        for i in range(256):
            t.append(0)
        for i in self.rect(0,0,self.__width,self.__height):
            t[self.__byteArray[self.pix(i[0],i[1])]]=t[self.__byteArray[self.pix(i[0],i[1])]]+1
        for i in range(len(t)):
            t[i]=int(t[i]/10)
        p=OneBMPPicture(self.getBlank(8,266,max(t)))
        for i in range(len(t)):
            p.drawLine(5+i,0,t[i])
        return p.__byteArray
    def getEverythingToBMP(self,path):
        with open(path,'rb') as f:
            p=bytearray(f.read())
            head=self.__getHeader(24,400,400)
            #col=self.__getTagRGBQuad(8)
            data=[]
            for i in range(160000*3):
                data.append(p[i])
            return bytearray(head+data)
    def bite24ToBite8(self):
        image=[]
        y=0
        cover=self.__getImageSize(8,self.__width,1)-self.__width
        for i in self.rect(0,0,self.__width,self.__height):
            if i[1]>y:
                for j in range(int(cover)):
                    image.append(0)
                y=i[1]
            image.append(int(self.__byteArray[self.pix(i[0],i[1])]*0.299+self.__byteArray[self.pix(i[0],i[1])+1]*0.587+self.__byteArray[self.pix(i[0],i[1])+2]*0.114))
        for j in range(int(cover)):
                    image.append(0)
        head=self.__getHeader(8,self.__width,self.__height)
        color=self.__getTagRGBQuad(8)
        self.__byteArray=bytearray(head+color+image)
        self.__initAttr()
p=OneBMPPicture('12o.bmp')
# p.drawLine(20,0,150)
# p.createBMPFile('eer.bmp')
# for i in range(2):
#     for j in range(5):
#         p.gaussianBlurFilter(j*100,i*100,100,100,i*j,1)
# p.bite24ToBite8()
# p.createBMPFile('12o.bmp')
#p.drawFillRect(0,0,20,100)
p.createBMPFile('12ooo.bmp',p.getEverythingToBMP('89.bmp'))



