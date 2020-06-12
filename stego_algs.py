# -*- coding: utf8 -*-
import sys
import array

class Algorithm(object):
    """
        Lsb Algorithm Abstract class
    """
    def __init__(self,image,channels='rgb',bits=[0],vertical=False):
        self.image=image
        self.channels=channels
        self.bits=bits
        self.vertical=vertical
    def open(self):
        pass
    def read(self,xinit=0,yinit=0,xend=sys.maxint,yend=sys.maxint):
        pass    
    def write(self,filetoembed,xinit=0,yinit=0,xend=sys.maxint,yend=sys.maxint):
        pass
    def getImage(self):
        return self.image
        
class Classic(Algorithm):
    """
        Classic LSB: stego on bit 0 of the rgb channel with END bit in blue channel  
        | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
        | 765   432   10- | 765   432   10- | 765   432   10END |
    """
    def __init__(self,image,channels='rgb',bits=[0],vertical=False):
        super(Classic, self).__init__(image,channels,bits,vertical)
        
    def write(self,filetoembed,xinit=0,yinit=0,xend=sys.maxint,yend=sys.maxint):
        image = self.image
        bits = self.bits
        vertical = self.vertical
        m = image.load()
        sz = image.size 
        bindex=7
        bitnum = bits[0]%7
        char = filetoembed.read(1) 
        if char == '': 
            return image
        if xinit > xend or yinit > yend:
            return image
        F = min(sz[0],xend)
        f = xinit
        S = min(sz[1],yend)
        s = yinit
        if vertical == True:
            F = min(sz[1],yend)
            f = yinit
            S = min(sz[0],xend)
            s = xinit
        for x in range(f,F,1):
            for y in range(s,S,1):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                if bindex > 1 :
                    r = ( r & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                    g = ( g & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                    b = ( b & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                elif bindex == 1 : 
                    r = ( r & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                    g = ( g & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    b = ( b & (0xfe << bitnum ) ) | 0x00 
                    bindex=7
                    char = filetoembed.read(1) 
                    if char == '': 
                        b = ( b & (0xfe << bitnum ) ) | 0xff    # mark the end of embeddings
                        if vertical == True:
                            m[(y,x)] = r,g,b,a
                        else:
                            m[(x,y)] = r,g,b,a
                        return image
                if vertical == True:
                    m[(y,x)] = r,g,b,a
                else:
                    m[(x,y)] = r,g,b,a
        return image
   
    def read (self,xinit=0,yinit=0,xend=sys.maxint,yend=sys.maxint):
        image = self.image
        bitnum = self.bits[0]
        vertical = self.vertical
        by = array.array('B')
        m = image.load()
        sz = image.size 
        mask =  0x01 << (bitnum%7)
        index=0
        by.append(0)
        bindex=7
        if xinit > xend or yinit > yend:
            return by
        F = min(sz[0],xend)
        f = xinit
        S = min(sz[1],yend)
        s = yinit
        if vertical == True:
            F = min(sz[1],yend)
            f = yinit
            S = min(sz[0],xend)
            s = xinit
        for x in range(f,F,1):
            for y in range(s,S,1):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                # | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
                # | 765   432   10- | 765   432   10- | 765   432   10E |
                if bindex > 1 :
                    by[index]|= ((r & mask)>>bitnum )<< bindex
                    bindex-=1
                    by[index]|= ((g & mask)>>bitnum ) << bindex
                    bindex-=1
                    by[index]|= ((b & mask)>>bitnum ) << bindex
                    bindex-=1
                else:
                    if bindex == 1 : 
                        by[index]|= ((r & mask)>>bitnum ) << bindex
                        bindex-=1
                        by[index]|= ((g & mask)>>bitnum ) << bindex
                        if b&mask==1:
                            return by
                        else:
                            by.append(0)
                            index+=1
                            bindex=7
                    
        return by

class Lsb(Algorithm):
    """
        Raw Lsb algorithm.
        | rgba | rgba | rgba | rgba | ...
        | 7654   3210 | 7654   3210 | ...
        | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb |
        | 765   432   107 | 654   321   076 | 543   210   765 | 432   107 |
        | rg | rg | rg | rg | rg  ...
        | 76   54   32   10 | 76  ...
        | r | r | r | r ...
        | 7   6   5   4 ...
	"""
    def __init__(self,image,channels='rgb',bits=[0],vertical=False):
        super(Lsb, self).__init__(image,channels,bits,vertical)
         
    def write(self,filetoembed,xinit=0,yinit=0,xend=sys.maxint,yend=sys.maxint):
        image = self.image
        channels = self.channels
        bits = self.bits
        vertical = self.vertical
        m = image.load()
        sz = image.size
        bindex=7
        char = filetoembed.read(1) 
        if char == '': 
            return image
        if xinit > xend or yinit > yend:
            return image
        F = min(sz[0],xend)
        f = xinit
        S = min(sz[1],yend)
        s = yinit
        if vertical == True:
            F = min(sz[1],yend)
            f = yinit
            S = min(sz[0],xend)
            s = xinit
        for x in range(f,F,1):
            for y in range(s,S,1):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                for bit in bits:
                    bitnum = bit % 7
                    for chan in channels:
                        if 'r'==chan :
                            r = ( r & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if bindex<0:
                                bindex=7
                                char = filetoembed.read(1) 
                                if char=='': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                        if 'g'==chan:
                            g = ( g & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if bindex<0:
                                bindex=7
                                char = filetoembed.read(1) 
                                if char == '': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                        if 'b'==chan:
                            b = ( b & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if bindex<0:
                                bindex=7
                                char = filetoembed.read(1) 
                                if char=='': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                        if 'a'==chan:
                            a = ( a & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if bindex<0:
                                bindex=7
                                char = filetoembed.read(1) 
                                if char == '': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                if vertical == True:
                    m[(y,x)] = r,g,b,a
                else:
                    m[(x,y)] = r,g,b,a
        return image
    
    def read(self,xinit=0,yinit=0,xend=sys.maxint,yend=sys.maxint):
        image = self.image
        channels = self.channels
        bits = self.bits
        vertical = self.vertical
        by = array.array('B')
        m = image.load()
        sz = image.size
        index=0
        by.append(0)
        bindex=7
        if xinit > xend or yinit > yend:
            return by
        F = min(sz[0],xend)
        f = xinit
        S = min(sz[1],yend)
        s = yinit
        if vertical==True:
            F = min(sz[1],yend)
            f = yinit
            S = min(sz[0],xend)
            s = xinit
        for x in range(f,F,1):
            for y in range(s,S,1):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                for bit in bits:
                    bitnum = bit % 7
                    mask = 0x01 << bitnum
                    for chan in channels:
                        if 'r'==chan:
                            by[index]|= ((r & mask)>>bitnum )<< bindex
                            bindex-=1
                            if bindex<0:
                                by.append(0)
                                index+=1
                                bindex=7
                        if 'g'==chan:
                            by[index]|= ((g & mask)>>bitnum ) << bindex
                            bindex-=1
                            if bindex<0:
                                by.append(0)
                                index+=1
                                bindex=7
                        if 'b'==chan:
                            by[index]|= ((b & mask)>>bitnum ) << bindex
                            bindex-=1
                            if bindex<0:
                                by.append(0)
                                index+=1
                                bindex=7
                        if 'a'==chan:
                            by[index]|= ((a & mask)>>bitnum ) << bindex
                            bindex-=1
                            if bindex<0:
                                by.append(0)
                                index+=1
                                bindex=7
        return by
