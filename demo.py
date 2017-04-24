# def pix(x,y):
#     return 

# with open('1.bmp','rb') as f:
#     b=bytearray(f.read())
#     for i in range(56):
#         print(b[i],' ',i+1)
#     print(b[56])
#     width=b[19]*256+b[18]
#     print(width)
class OneBMPPicture:
    __width=0
    __height=0
    byteArray=[]
    def __init__(self,path):
        with open(path,'rb') as f:
            self.byteArray=bytearray(f.read())
            self.width=self.byteArray[18]+self.byteArray[19]*256+self.byteArray[20]*65536
            self.height=self.byteArray[22]+self.byteArray[23]*256+self.byteArray[24]*65536
            f.close()
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def pix(self,x,y):
        cover=4-self.width*3%4
        if cover==4:
            return (y-1)*self.width*3+(x-1)*3+54
        else:
            return (y-1)*self.width*3+(x-1)*3+54+(y-1)*cover
    def createPicture(self,path):
        with open(path,'wb') as f:
            f.write(self.byteArray)
            f.close()
    def gaussianBlur(self,n):
        gaussianBlurWeight=[0.09,0.12,0.09,0.12,0.14,0.12,0.09,0.12,0.09]
        for y in range(2,self.height-n+1,n):
            for x in range(2,self.width-n+1,n):
                r=0
                g=0
                b=0
                cout=0
                for i in range(-1,2):
                    for j in range(-1,2):
                        r=r+self.byteArray[self.pix(x+j,y+i)]*gaussianBlurWeight[cout]
                        g=g+self.byteArray[self.pix(x+j,y+i)+1]*gaussianBlurWeight[cout]
                        b=b+self.byteArray[self.pix(x+j,y+i)+2]*gaussianBlurWeight[cout]
                        cout=cout+1
                for i in range(n):
                    for j in range(n):
                        self.byteArray[self.pix(x+j,y+i)]=int(r)
                        self.byteArray[self.pix(x+j,y+i)+1]=int(g)
                        self.byteArray[self.pix(x+j,y+i)+2]=int(b)

    def bitPciture(self,n):  ##马赛克图片
        for y in range(1,self.height-n+1,n):
            for x in range(1,self.width-n+1,n):
                r=0
                g=0
                b=0
                for i in range(n):
                    for j in range(n):
                        r=r+self.byteArray[self.pix(x+i,y+j)]
                        g=g+self.byteArray[self.pix(x+i,y+j)+1]
                        b=b+self.byteArray[self.pix(x+i,y+j)+2]
                r=int(r/(n*n))
                g=int(g/(n*n))
                b=int(b/(n*n))
                for i in range(n):
                    for j in range(n):
                        self.byteArray[self.pix(x+j,y+i)]=r
                        self.byteArray[self.pix(x+j,y+i)+1]=g
                        self.byteArray[self.pix(x+j,y+i)+2]=b
    # def createBlankBMP(self,width,height,path):
    #     self.byteArray=[
    #     42 4D 96 32 0D 00 00 00 00 00 36 00 00 00 28 00
    #     00 00 D3 01 00 00 68 02 00 00 01 00 18 00 00 00
    #     00 00 60 32 0D 00 13 0B 00 00 13 0B 00 00 00 00
    #     00 00 00 00 00 00]

    #     self.byteArray[1]=77
    #     with open(path,'wb') as f:
    #         f.write(self.byteArray)
    #         f.close()
p=OneBMPPicture('1.bmp')
#p.byteArray[18]=1
#p.bitPciture(3)
p.gaussianBlur(1)
p.createPicture('wwe.bmp')
